from django.shortcuts import render
import pandas as pd
import plotly.express as px
import networkx as nx
import plotly.graph_objs as go
from scraping.models import EuroMillionsResult  # Ensure this import path is correct
import itertools

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
    return fig.to_html(full_html=False, config={'displayModeBar': True})

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

    x_edges = []
    y_edges = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]][0], pos[edge[0]][1]
        x1, y1 = pos[edge[1]][0], pos[edge[1]][1]
        x_edges.extend([x0, x1, None])
        y_edges.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=x_edges,
        y=y_edges,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    x_nodes = []
    y_nodes = []
    node_text = []
    node_color = []
    for node in G.nodes():
        x_nodes.append(pos[node][0])
        y_nodes.append(pos[node][1])
        adjacencies = G.adj[node]
        node_color.append(len(adjacencies))
        node_text.append('Number ' + str(node))

    node_trace = go.Scatter(
        x=x_nodes,
        y=y_nodes,
        text=node_text,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=10,
            color=node_color,
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

def calculate_pairs_and_triplets_frequency(df, columns):
    pairs_frequency = {}
    triplets_frequency = {}

    # Calculate pairs frequency
    for index, row in df.iterrows():
        pairs = itertools.combinations(row[columns], 2)
        for pair in pairs:
            if pair in pairs_frequency:
                pairs_frequency[pair] += 1
            else:
                pairs_frequency[pair] = 1

    # Calculate triplets frequency
    for index, row in df.iterrows():
        triplets = itertools.combinations(row[columns], 3)
        for triplet in triplets:
            if triplet in triplets_frequency:
                triplets_frequency[triplet] += 1
            else:
                triplets_frequency[triplet] = 1

    return pairs_frequency, triplets_frequency


def plot_network(frequency, title, mode='pairs'):
    G = nx.Graph()
    for combo, freq in frequency.items():
        elements = itertools.combinations(combo, 2) if mode == 'pairs' else itertools.combinations(combo, 3)
        for pair in elements:
            if G.has_edge(pair[0], pair[1]):
                G[pair[0]][pair[1]]['weight'] += freq
            else:
                G.add_edge(pair[0], pair[1], weight=freq)
    
    # Layout and plotting remain the same
    pos = nx.spring_layout(G, k=0.5, iterations=20)
    
    # Updated part
    edge_trace = go.Scatter(
        x=[pos[edge[0]][0] for edge in G.edges()] + [None],
        y=[pos[edge[0]][1] for edge in G.edges()] + [None],
        line=dict(width=1.0, color='#888'),  # Adjust the width as needed
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
            colorbar=dict(thickness=15, title='Node Connections')))

    fig = go.Figure(data=[edge_trace, node_trace], layout=go.Layout(
        title=title, showlegend=False, hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    
    return fig.to_html(full_html=False, config={'displayModeBar': False})



def stats_view(request):
    data = EuroMillionsResult.objects.all()
    df_main_balls = pd.DataFrame(list(data.values('ball_1', 'ball_2', 'ball_3', 'ball_4', 'ball_5')))
    df_lucky_stars = pd.DataFrame(list(data.values('lucky_star_1', 'lucky_star_2')))
    
    # Calculate frequencies for pairs and triplets
    pairs_freq, triplets_freq = calculate_pairs_and_triplets_frequency(df_main_balls, ['ball_1', 'ball_2', 'ball_3', 'ball_4', 'ball_5'])
    
    # Generate graphs
    graph_pairs = plot_network(pairs_freq, 'Network Graph of Frequent Number Pairs', mode='pairs')
    graph_triplets = plot_network(triplets_freq, 'Network Graph of Frequent Number Triplets', mode='triplets')
    
    # Existing graphs
    graph_main_balls = plot_numbers_frequencies(df_main_balls, ['ball_1', 'ball_2', 'ball_3', 'ball_4', 'ball_5'], 'Frequency of Main EuroMillions Balls')
    graph_lucky_stars = plot_numbers_frequencies(df_lucky_stars, ['lucky_star_1', 'lucky_star_2'], 'Frequency of EuroMillions Lucky Stars')

    # Calculate combinations frequency
    frequency = calculate_combinations_frequency(df_main_balls, ['ball_1', 'ball_2', 'ball_3', 'ball_4', 'ball_5'])
    
    # Generate combination network graph
    graph_combinations = plot_combination_network(frequency, 'Network Graph of Winning Combinations Frequency')
    
    # Assuming prepare_data is defined earlier in your code
    prepared_df = prepare_data(df_main_balls)  # Call prepare_data to generate prepared_df

    # Now you can use prepared_df in plot_correlation function
    graph_correlation = plot_correlation(prepared_df, 'Correlation Between Main Balls')

    
    return render(request, 'lottery_stats/stats.html', {
        'graph_main_balls': graph_main_balls,
        'graph_lucky_stars': graph_lucky_stars,
        'graph_correlation': graph_correlation,
        'graph_combinations': graph_combinations,
        'graph_pairs': graph_pairs,
        'graph_triplets': graph_triplets
    })


