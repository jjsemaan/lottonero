from django.shortcuts import render
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
from scipy.stats import gaussian_kde
from scraping.models import EuroMillionsResult

def get_filtered_data(time_range):
    if time_range == '1m':
        num_rows = 8  # 1 month = 8 draws
    elif time_range == '6m':
        num_rows = 48  # 6 months = 48 draws
    elif time_range == '12m':
        num_rows = 96  # 12 months = 96 draws
    else:  # default to 3 months
        num_rows = 24  # 3 months = 24 draws
    
    # Fetch the last num_rows entries
    return EuroMillionsResult.objects.all().order_by('-draw_date')[:num_rows]

def plot_numbers_frequencies(df, columns, title):
    melted_df = df.melt(value_vars=columns)
    number_counts = melted_df['value'].value_counts().sort_index()
    
    # Compute median
    median_value = number_counts.median()
    
    # Compute KDE
    kde = gaussian_kde(number_counts.values)
    x_range = np.linspace(number_counts.index.min(), number_counts.index.max(), 100)
    kde_values = kde(x_range)
    
    # Determine bar colors based on whether they are above the median
    bar_colors = ['rgba(245, 208, 39, 0.8)' if value > median_value else 'blue' for value in number_counts.values]
    
    fig = go.Figure(data=[
        go.Bar(
            x=number_counts.index,
            y=number_counts.values,
            marker=dict(color=bar_colors),
            name='Frequency'
        )
    ])
    
    # Update layout to control svg-container style and add median line
    fig.update_layout(
        xaxis_title='Ball Numbers',
        yaxis_title='Frequency',
        paper_bgcolor='rgba(0,0,0,0)',  # transparent background
        plot_bgcolor='rgba(0,0,0,0)',   # transparent plot area
        font=dict(color='black', size=12),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='top',
            y=1.02,
            xanchor='center',
            x=0.5
        ),
        title=dict(text='', x=0.5),  # Hide the title
        xaxis=dict(
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False
        ),
        margin=dict(l=20, r=20, t=30, b=20)  # Adjust margins
    )
    
    # Add a median line
    fig.add_shape(
        type="line",
        x0=number_counts.index.min(),
        y0=median_value,
        x1=number_counts.index.max(),
        y1=median_value,
        line=dict(color="red", width=2, dash="dash"),
    )
    
    # Add annotation for the median line
    fig.add_annotation(
        x=number_counts.index.max(),
        y=median_value,
        text=f"Median: {median_value:.2f}",
        showarrow=False,
        yshift=10,
        font=dict(color="red", size=12)
    )
    
    # Add KDE curve with shading
    fig.add_trace(
        go.Scatter(
            x=x_range,
            y=kde_values * number_counts.values.sum() / kde_values.sum(),  # scale KDE values to match the histogram
            mode='lines',
            name='KDE',
            line=dict(color='darkgrey'),
            fill='tozeroy',  # fill area under the curve
            fillcolor='rgba(0, 0, 255, 0.2)'  # semi-transparent blue
        )
    )
    
    fig_config = {'displayModeBar': False}
    return fig.to_html(full_html=False, config=fig_config)

def frequency_view(request):
    time_range = request.GET.get('time_range', '3m')
    data = get_filtered_data(time_range)
    
    # Convert the queryset to a DataFrame and print its columns for debugging
    df_main_balls = pd.DataFrame(list(data.values('ball_1', 'ball_2', 'ball_3', 'ball_4', 'ball_5')))
    df_lucky_stars = pd.DataFrame(list(data.values('lucky_star_1', 'lucky_star_2')))
    
    graph_main_balls = plot_numbers_frequencies(df_main_balls, ['ball_1', 'ball_2', 'ball_3', 'ball_4', 'ball_5'], 'Frequency of Main EuroMillions Balls')
    graph_lucky_stars = plot_numbers_frequencies(df_lucky_stars, ['lucky_star_1', 'lucky_star_2'], 'Frequency of EuroMillions Lucky Stars')

    return render(request, 'lottery_stats/frequencies.html', {
        'graph_main_balls': graph_main_balls,
        'graph_lucky_stars': graph_lucky_stars,
        'selected_time_range': time_range
    })









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
    return fig.to_html(full_html=False, config={'displayModeBar': True})

def correlations_view(request):
    data = EuroMillionsResult.objects.all()
    df_main_balls = pd.DataFrame(list(data.values('ball_1', 'ball_2', 'ball_3', 'ball_4', 'ball_5')))
    prepared_df = prepare_data(df_main_balls)
    graph_correlation = plot_correlation(prepared_df, 'Correlation Between Main Balls')

    return render(request, 'lottery_stats/correlations.html', {
        'graph_correlation': graph_correlation
    })


import itertools
import networkx as nx

def calculate_combinations_frequency(df, columns):
    combinations = df[columns].apply(lambda row: tuple(sorted(row)), axis=1)
    frequency = combinations.value_counts()
    return frequency

def plot_combination_network(frequency, title):
    G = nx.Graph()
    for combo, freq in frequency.items():
        for pair in itertools.combinations(combo, 2):
            if G.has_edge(pair[0], pair[1]):
                G[pair[0]][pair[1]]['weight'] += freq
            else:
                G.add_edge(pair[0], pair[1], weight=freq)
    pos = nx.spring_layout(G, k=0.5, iterations=20)
    edge_trace = go.Scatter(
        x=[pos[edge[0]][0] for edge in G.edges()] + [None],
        y=[pos[edge[1]][1] for edge in G.edges()] + [None],
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_trace = go.Scatter(
        x=[pos[node][0] for node in G.nodes()],
        y=[pos[node][1] for node in G.nodes()],
        text=[f'Number {node}' for node in G.nodes()],
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=10,
            color=[len(G.adj[node]) for node in G.nodes()],
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)))

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title=title,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    return fig.to_html(full_html=False, config={'displayModeBar': False})


def calculate_combinations_frequency_over_time(df, columns, num_draws=96):
    # Assuming each row in df has a 'draw_date'
    df['combination'] = df[columns].apply(lambda row: tuple(sorted(row)), axis=1)
    grouped = df.groupby(['draw_date', 'combination']).size().unstack(fill_value=0).cumsum()
    # Limit the data to the last num_draws
    if num_draws < len(grouped):
        grouped = grouped.tail(num_draws)
    return grouped

def plot_stacked_area_chart(frequency, title):
    fig = go.Figure()
    for combo in frequency.columns:
        fig.add_trace(go.Scatter(
            x=frequency.index,
            y=frequency[combo],
            mode='lines',
            name=str(combo),
            stackgroup='one'
        ))
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Cumulative Frequency',
        hovermode='x'
    )
    return fig.to_html(full_html=False, config={'displayModeBar': True})

def combinations_time_view(request):
    num_draws = request.GET.get('num_draws', 96)  # Get num_draws from query parameters or default to 96
    try:
        num_draws = int(num_draws)
    except ValueError:
        num_draws = 96  # Default if conversion fails

    data = EuroMillionsResult.objects.all().values('draw_date', 'ball_1', 'ball_2', 'ball_3', 'ball_4', 'ball_5')
    df_main_balls = pd.DataFrame(list(data))
    frequency = calculate_combinations_frequency_over_time(df_main_balls, ['ball_1', 'ball_2', 'ball_3', 'ball_4', 'ball_5'], num_draws)
    graph_combinations = plot_stacked_area_chart(frequency, 'Cumulative Frequency of Winning Combinations Over Time')

    return render(request, 'lottery_stats/combinations.html', {
        'graph_combinations': graph_combinations,
        'selected_draws': num_draws
    })

