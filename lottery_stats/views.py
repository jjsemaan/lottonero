from django.shortcuts import render
import plotly.express as px
import pandas as pd
from scraping.models import EuroMillionsResult

def plot_numbers_frequencies(df, columns, title):
    """
    Create a frequency histogram of EuroMillions numbers using the provided DataFrame.
    """
    # Melt the DataFrame so each row represents a single number draw
    melted_df = df.melt(value_vars=columns)
    number_counts = melted_df['value'].value_counts().sort_index()

    # Create a bar plot using Plotly Express
    fig = px.bar(
        x=number_counts.index,
        y=number_counts.values,
        labels={'x': 'Number', 'y': 'Frequency'},
        title=title
    )

    fig_config = {
        'displayModeBar': False  # This disables the mode bar entirely
    }

    # Convert the figure to HTML for web embedding
    return fig.to_html(full_html=False, config=fig_config)

def stats_view(request):
    """
    Generate a view that displays frequency histograms for both the main EuroMillions balls
    and the lucky stars on a single page.
    """
    # Fetch all results from the database
    data = EuroMillionsResult.objects.all()

    # Convert the queryset to DataFrames for each set of balls
    df_main_balls = pd.DataFrame(list(data.values('ball_1', 'ball_2', 'ball_3', 'ball_4', 'ball_5')))
    df_lucky_stars = pd.DataFrame(list(data.values('lucky_star_1', 'lucky_star_2')))

    # Use the plotting function to get the graph HTML for main balls and lucky stars
    graph_main_balls = plot_numbers_frequencies(df_main_balls, ['ball_1', 'ball_2', 'ball_3', 'ball_4', 'ball_5'], 'Frequency of Main EuroMillions Balls')
    graph_lucky_stars = plot_numbers_frequencies(df_lucky_stars, ['lucky_star_1', 'lucky_star_2'], 'Frequency of EuroMillions Lucky Stars')

    # Render the HTML page with both graphs
    return render(request, 'lottery_stats/stats.html', {
        'graph_main_balls': graph_main_balls,
        'graph_lucky_stars': graph_lucky_stars
    })
