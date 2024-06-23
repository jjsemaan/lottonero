from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
from scipy.stats import gaussian_kde
from scraping.models import EuroMillionsResult
from orders.models import Subscription
from django.db.models import Q
import itertools
import networkx as nx


def get_filtered_data(time_range):
    """
    Retrieves a specified number of recent EuroMillions draw results based on a given time range.

    This function filters EuroMillions draw results to return a limited set of entries corresponding
    to the time range specified by the user. The number of results returned varies by the time range:
    - '1m' returns the last 8 draws (approximately 1 month).
    - '6m' returns the last 48 draws (approximately 6 months).
    - '12m' returns the last 96 draws (approximately 12 months).
    - Any other input defaults to the last 24 draws (approximately 3 months).

    Args:
        time_range (str): A string identifier for the time range (e.g., '1m', '6m', '12m').

    Returns:
        QuerySet: A Django QuerySet containing the filtered list of EuroMillions draw results, ordered
                  from the most recent draw to the oldest within the specified range.
    """
    if time_range == "1m":
        num_rows = 8  # 1 month = 8 draws
    elif time_range == "6m":
        num_rows = 48  # 6 months = 48 draws
    elif time_range == "12m":
        num_rows = 96  # 12 months = 96 draws
    else:  # default to 3 months
        num_rows = 24  # 3 months = 24 draws

    # Fetch the last num_rows entries
    return EuroMillionsResult.objects.all().order_by("-draw_date")[:num_rows]


def plot_numbers_frequencies(df, columns, title):
    """
    Generates an interactive bar chart of number frequencies with a KDE curve and median line.

    This function takes a DataFrame and column list, melts the DataFrame to long format for
    those columns, and computes the value counts. It plots these frequencies as bars, color-coded
    based on whether each value is above or below the median. It also overlays a KDE to show
    the distribution's density and a median line for reference.

    Args:
        df (DataFrame): The pandas DataFrame containing the data.
        columns (list): A list of columns in the DataFrame that contain the number data.
        title (str): The title of the plot.

    Returns:
        str: An HTML string containing a plotly interactive figure.

    The plot is styled with transparent backgrounds, custom color themes for bars and KDE, and includes
    annotations for the median. It can be embedded directly into web pages.
    """
    melted_df = df.melt(value_vars=columns)
    number_counts = melted_df["value"].value_counts().sort_index()

    # Compute median
    median_value = number_counts.median()

    # Compute KDE
    kde = gaussian_kde(number_counts.values)
    x_range = np.linspace(
        number_counts.index.min(), number_counts.index.max(), 100
    )
    kde_values = kde(x_range)

    # Determine bar colors based on whether they are above the median
    bar_colors = [
        "rgba(245, 208, 39, 0.8)" if value > median_value else "blue"
        for value in number_counts.values
    ]

    fig = go.Figure(
        data=[
            go.Bar(
                x=number_counts.index,
                y=number_counts.values,
                marker=dict(color=bar_colors),
                name="Frequency",
            )
        ]
    )

    # Update layout to control svg-container style and add median line
    fig.update_layout(
        xaxis_title="Ball Numbers",
        yaxis_title="Frequency",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="black", size=10),
        showlegend=True,
        legend=dict(
            orientation="h", yanchor="top", y=1.02, xanchor="center", x=0.5
        ),
        title=dict(text="", x=0.5),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        margin=dict(l=20, r=20, t=30, b=20),
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
        font=dict(color="red", size=12),
    )

    # Add KDE curve with shading
    fig.add_trace(
        go.Scatter(
            x=x_range,
            y=kde_values * number_counts.values.sum() / kde_values.sum(),
            mode="lines",
            name="KDE",
            line=dict(color="darkgrey"),
            fill="tozeroy",
            fillcolor="rgba(0, 0, 255, 0.2)",
        )
    )

    fig_config = {"displayModeBar": False}
    return fig.to_html(full_html=False, config=fig_config)


@login_required
def frequency_view(request):
    """
    Renders lottery frequency graphs for EuroMillions based on a user-selected time range.

    Args:
        request (HttpRequest): The HTTP request object containing request metadata.

    Returns:
        HttpResponse: Renders the 'lottery_stats/frequencies.html' with frequency graphs or
                      redirects to 'pricing_page' if the user lacks necessary subscriptions.

    Uses:
        - `get_filtered_data`: Fetches lottery data for the specified time.
        - `plot_numbers_frequencies`: Generates interactive Plotly graphs for the data.

    Templates:
        - Renders 'lottery_stats/frequencies.html' to display the frequency analysis.
    """
    if not Subscription.objects.filter(
        Q(
            user=request.user,
            active=True,
            product_name="Lotto Statistics for EuroMillions",
        )
        | Q(user=request.user, active=True, product_name="Premium Full Access")
    ).exists():
        messages.error(
            request,
            "Access denied. You are not subscribed to Lotto Statistics or Premium Full Access.",
        )
        return redirect("pricing_page")

    messages.warning(
        request, 
        "This page is not suitable for viewing on mobile devices due the size of the statistical graphs within and is better visualised on desktops and laptops."
        )
    time_range = request.GET.get("time_range", "3m")
    data = get_filtered_data(time_range)

    df_main_balls = pd.DataFrame(
        list(data.values("ball_1", "ball_2", "ball_3", "ball_4", "ball_5"))
    )
    df_lucky_stars = pd.DataFrame(
        list(data.values("lucky_star_1", "lucky_star_2"))
    )

    graph_main_balls = plot_numbers_frequencies(
        df_main_balls,
        ["ball_1", "ball_2", "ball_3", "ball_4", "ball_5"],
        "Frequency of Main EuroMillions Balls",
    )
    graph_lucky_stars = plot_numbers_frequencies(
        df_lucky_stars,
        ["lucky_star_1", "lucky_star_2"],
        "Frequency of EuroMillions Lucky Stars",
    )

    return render(
        request,
        "lottery_stats/frequencies.html",
        {
            "graph_main_balls": graph_main_balls,
            "graph_lucky_stars": graph_lucky_stars,
            "selected_time_range": time_range,
        },
    )


def prepare_data(df):
    """
    Prepares a DataFrame by encoding lottery numbers as binary occurrences.

    Args:
        df (DataFrame): A pandas DataFrame containing the lottery draw data with columns
                        for each ball drawn.

    Returns:
        DataFrame: A new DataFrame of the same length as `df` with 50 columns ('number_1' to 'number_50'),
                   each representing a binary occurrence of the lottery numbers in the draws.
    """
    numbers_range = range(1, 51)
    column_names = [f"number_{i}" for i in numbers_range]
    occurrences = pd.DataFrame(0, index=df.index, columns=column_names)
    for index, row in df.iterrows():
        for col in ["ball_1", "ball_2", "ball_3", "ball_4", "ball_5"]:
            number_key = f"number_{row[col]}"
            occurrences.at[index, number_key] = 1
    return occurrences


def plot_correlation(df, title):
    """
    Generates a heatmap plot representing the correlation matrix of lottery numbers.

    Args:
        df (DataFrame): A pandas DataFrame where each column represents a lottery number and
                        each row indicates the presence (1) or absence (0) of that number in a specific draw.
        title (str): The title of the generated heatmap plot.

    Returns:
        str: An HTML string containing a Plotly heatmap visualization of the correlation matrix,
             which can be embedded directly into web pages.
    """
    correlation = df.corr()
    fig = px.imshow(
        correlation,
        text_auto=True,
        color_continuous_scale=["#ffff99", "#FF0000"],
        title=title,
        aspect="auto"
    )

    # Assuming original height is 400, doubling to 800
    fig.update_layout(
        height=800,
        font=dict(color="black", size=9),
        xaxis=dict(
            side="bottom",
            tickvals=list(range(50)),
            ticktext=[f"{i}" for i in range(1, 51)]
        ),
        yaxis=dict(
            tickvals=list(range(50)),
            ticktext=[f"{i}" for i in range(1, 51)]
        )
    )

    return fig.to_html(full_html=False, config={"displayModeBar": True})


@login_required
def correlations_view(request):
    """
    View function to display the correlation heatmap between lottery numbers.

    Args:
        request (HttpRequest): The HttpRequest object that carries metadata about the request.

    Returns:
        HttpResponse: Renders the 'lottery_stats/correlations.html' template with the correlation
                      heatmap or redirects to the 'pricing_page' if the user lacks necessary subscriptions.

    Templates:
        - Renders 'lottery_stats/correlations.html' to display the correlation heatmap.
    """
    if not Subscription.objects.filter(
        Q(
            user=request.user,
            active=True,
            product_name="Lotto Statistics for EuroMillions",
        )
        | Q(user=request.user, active=True, product_name="Premium Full Access")
    ).exists():
        messages.error(
            request,
            "Access denied. You are not subscribed to Lotto Statistics or Premium Full Access.",
        )
        return redirect("pricing_page")

    messages.warning(
        request, 
        "This page is not suitable for viewing on mobile devices due the size of the statistical graphs within and is better visualised on desktops and laptops."
        )
    data = EuroMillionsResult.objects.all()
    df_main_balls = pd.DataFrame(
        list(data.values("ball_1", "ball_2", "ball_3", "ball_4", "ball_5"))
    )
    prepared_df = prepare_data(df_main_balls)
    graph_correlation = plot_correlation(
        prepared_df, ""
    )

    return render(
        request,
        "lottery_stats/correlations.html",
        {"graph_correlation": graph_correlation},
    )


def calculate_combinations_frequency(df, columns):
    """
    Calculates the frequency of unique combinations of values across specified columns in a DataFrame.

    Args:
        df (DataFrame): The pandas DataFrame containing the data to analyze.
        columns (list): A list of column names to include in the combinations.

    Returns:
        Series: A pandas Series where the index is the unique combinations (as tuples) and the values are
                the frequencies of these combinations in the DataFrame.
    """
    combinations = df[columns].apply(lambda row: tuple(sorted(row)), axis=1)
    frequency = combinations.value_counts()
    return frequency


def plot_combination_network(frequency, title):
    """
    Generates an interactive network plot of number combinations based on their frequency.

    Args:
        frequency (dict): A dictionary where keys are tuples representing combinations of numbers (e.g., (1, 2, 3))
                          and values are the frequencies of these combinations.
        title (str): The title of the plot, displayed at the top of the visualization.

    Returns:
        str: An HTML string containing a Plotly interactive graph which can be embedded in web pages. The graph
             shows the connections between numbers with edges weighted by frequency and nodes sized by connectivity.
    """
    G = nx.Graph()
    for combo, freq in frequency.items():
        for pair in itertools.combinations(combo, 2):
            if G.has_edge(pair[0], pair[1]):
                G[pair[0]][pair[1]]["weight"] += freq
            else:
                G.add_edge(pair[0], pair[1], weight=freq)
    pos = nx.spring_layout(G, k=0.5, iterations=20)
    edge_trace = go.Scatter(
        x=[pos[edge[0]][0] for edge in G.edges()] + [None],
        y=[pos[edge[1]][1] for edge in G.edges()] + [None],
        line=dict(width=0.5, color="#888"),
        hoverinfo="none",
        mode="lines",
    )

    node_trace = go.Scatter(
        x=[pos[node][0] for node in G.nodes()],
        y=[pos[node][1] for node in G.nodes()],
        text=[f"Number {node}" for node in G.nodes()],
        mode="markers",
        hoverinfo="text",
        marker=dict(
            showscale=True,
            colorscale="YlGnBu",
            size=10,
            color=[len(G.adj[node]) for node in G.nodes()],
            colorbar=dict(
                thickness=15,
                title="Node Connections",
                xanchor="left",
                titleside="right",
            ),
            line=dict(width=2),
        ),
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title=title,
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ),
    )

    return fig.to_html(full_html=False, config={"displayModeBar": False})


def calculate_combinations_frequency_over_time(df, columns, num_draws=96):
    """
    Calculates the cumulative frequency of combinations over time from a given DataFrame.

    Args:
        df (DataFrame): A pandas DataFrame containing the lottery draw results.
        columns (list): List of column names to include in the combination analysis.
        num_draws (int, optional): The number of most recent draws to consider. Defaults to 96.

    Returns:
        DataFrame: A DataFrame indexed by 'draw_date' with columns for each combination showing the
                   cumulative frequency over time.
    """

    df["combination"] = df[columns].apply(
        lambda row: tuple(sorted(row)), axis=1
    )
    grouped = (
        df.groupby(["draw_date", "combination"])
        .size()
        .unstack(fill_value=0)
        .cumsum()
    )

    if num_draws < len(grouped):
        grouped = grouped.tail(num_draws)
    return grouped


def plot_stacked_area_chart(frequency, title):
    """
    Creates a stacked area chart to visualize the cumulative frequency of combinations over time.

    Args:
        frequency (DataFrame): A DataFrame containing cumulative frequencies of combinations over time,
                               indexed by date.
        title (str): The title of the plot.

    Returns:
        str: An HTML string containing a Plotly interactive stacked area chart, which can be embedded
             directly into web pages.
    """
    fig = go.Figure()
    for combo in frequency.columns:
        fig.add_trace(
            go.Scatter(
                x=frequency.index,
                y=frequency[combo],
                mode="lines",
                name=str(combo),
                stackgroup="one",
            )
        )
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Cumulative Frequency",
        hovermode="x",
    )
    return fig.to_html(full_html=False, config={"displayModeBar": True})


@login_required
def combinations_time_view(request):
    """
    Displays a view for analyzing the cumulative frequency of winning lottery combinations over time.

    This view checks if the user has the required subscription to access detailed statistics. If not,
    the user is redirected to the pricing page with an error message. For authorized users, it retrieves
    lottery results and calculates the cumulative frequency of winning combinations for a specified number
    of recent draws, then displays these statistics in a stacked area chart.

    Args:
        request (HttpRequest): The HttpRequest object containing metadata about the request.

    Returns:
        HttpResponse: Renders a template with the stacked area chart of winning combinations if authorized, or
                      redirects to the 'pricing_page' if the user lacks necessary subscriptions.
    """

    if not Subscription.objects.filter(
        Q(
            user=request.user,
            active=True,
            product_name="Lotto Statistics for EuroMillions",
        )
        | Q(user=request.user, active=True, product_name="Premium Full Access")
    ).exists():
        messages.error(
            request,
            "Access denied. You are not subscribed to Lotto Statistics or Premium Full Access.",
        )
        return redirect("pricing_page")

    messages.warning(
        request, 
        "This page is not suitable for viewing on mobile devices due the size of the statistical graphs within and is better visualised on desktops and laptops."
        )

    num_draws = request.GET.get("num_draws", 96)
    try:
        num_draws = int(num_draws)
    except ValueError:
        num_draws = 96

    data = EuroMillionsResult.objects.all().values(
        "draw_date", "ball_1", "ball_2", "ball_3", "ball_4", "ball_5"
    )
    df_main_balls = pd.DataFrame(list(data))
    frequency = calculate_combinations_frequency_over_time(
        df_main_balls,
        ["ball_1", "ball_2", "ball_3", "ball_4", "ball_5"],
        num_draws,
    )
    graph_combinations = plot_stacked_area_chart(
        frequency, ""
    )

    return render(
        request,
        "lottery_stats/combinations.html",
        {
            "graph_combinations": graph_combinations,
            "selected_draws": num_draws,
        },
    )
