from django.shortcuts import render
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from scraping.models import EuroMillionsResult

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

def frequency_view(request):
    data = EuroMillionsResult.objects.all()
    df_main_balls = pd.DataFrame(list(data.values('ball_1', 'ball_2', 'ball_3', 'ball_4', 'ball_5')))
    df_lucky_stars = pd.DataFrame(list(data.values('lucky_star_1', 'lucky_star_2')))

    graph_main_balls = plot_numbers_frequencies(df_main_balls, ['ball_1', 'ball_2', 'ball_3', 'ball_4', 'ball_5'], 'Frequency of Main EuroMillions Balls')
    graph_lucky_stars = plot_numbers_frequencies(df_lucky_stars, ['lucky_star_1', 'lucky_star_2'], 'Frequency of EuroMillions Lucky Stars')

    return render(request, 'lottery_stats/frequencies.html', {
        'graph_main_balls': graph_main_balls,
        'graph_lucky_stars': graph_lucky_stars
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
            name=str(combo),  # Convert combo tuple to string for legend
            stackgroup='one'  # define stack group
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

