from django.shortcuts import render
import plotly.express as px
import pandas as pd
from scraping.models import EuroMillionsResult  # Ensure this import path is correct

def plot_numbers_frequencies(df, columns, title):
    melted_df = df.melt(value_vars=columns)
    number_counts = melted_df['value'].value_counts().sort_index()
    fig = px.bar(
        x=number_counts.index,
        y=number_counts.values,
        labels={'x': 'Number', 'y': 'Frequency'},
        title=title
    )
    fig_config = {'displayModeBar': False}
    return fig.to_html(full_html=False, config=fig_config)

def prepare_data(df):
    numbers_range = range(1, 51)
    column_names = [f'number_{i}' for i in numbers_range]
    occurrences = pd.DataFrame(0, index=df.index, columns=column_names)
    for index, row in df.iterrows():
        for col in ['ball_1', 'ball_2', 'ball_3', 'ball_4', 'ball_5']:
            number_key = f'number_{row[col]}'
            occurrences.at[index, number_key] = 1
    return occurrences

def plot_correlation(df, title):
    correlation = df.corr()
    fig = px.imshow(correlation, text_auto=True, color_continuous_scale='Blues',
                    labels={'x': 'Numbers', 'y': 'Numbers', 'color': 'Correlation Coefficient'},
                    title=title, aspect='auto')
    num_labels = [f'{i}' for i in range(1, 51)]
    fig.update_xaxes(side="bottom", tickvals=list(range(50)), ticktext=num_labels)
    fig.update_yaxes(tickvals=list(range(50)), ticktext=num_labels)
    
    # Configure Plotly tools for the correlation graph
    fig_config = {'displayModeBar': True, 'scrollZoom': False, 'doubleClick': False, 'dragmode': False, 'displaylogo': False,
                  'modeBarButtonsToRemove': ['pan2d']}
    # Remove download plot option
    # fig_config['modeBarButtonsToAdd'] = ['drawrect', 'drawopenpath', 'drawclosedpath', 'drawcircle', 'drawline', 'drawlines', 'drawmarker', 'eraseshape']
    
    return fig.to_html(full_html=False, config=fig_config)


def stats_view(request):
    # Fetch all results from the database
    data = EuroMillionsResult.objects.all()
    df_main_balls = pd.DataFrame(list(data.values('ball_1', 'ball_2', 'ball_3', 'ball_4', 'ball_5')))
    df_lucky_stars = pd.DataFrame(list(data.values('lucky_star_1', 'lucky_star_2')))
    
    # Prepare data for correlation
    prepared_df = prepare_data(df_main_balls)
    
    # Use the plotting function to get the graph HTML
    graph_main_balls = plot_numbers_frequencies(df_main_balls, ['ball_1', 'ball_2', 'ball_3', 'ball_4', 'ball_5'], 'Frequency of Main EuroMillions Balls')
    graph_lucky_stars = plot_numbers_frequencies(df_lucky_stars, ['lucky_star_1', 'lucky_star_2'], 'Frequency of EuroMillions Lucky Stars')
    graph_correlation = plot_correlation(prepared_df, 'Correlation Between Main Balls')
    
    # Render the HTML page with all graphs
    return render(request, 'lottery_stats/stats.html', {
        'graph_main_balls': graph_main_balls,
        'graph_lucky_stars': graph_lucky_stars,
        'graph_correlation': graph_correlation
    })
