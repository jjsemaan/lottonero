from django.shortcuts import render
import plotly.express as px
import pandas as pd
from scraping.models import EuroMillionsResult

def stats_view(request):
    data = EuroMillionsResult.objects.all()
    df = pd.DataFrame(list(data.values('ball_1', 'ball_2', 'ball_3', 'ball_4', 'ball_5', 'lucky_star_1', 'lucky_star_2')))
    fig = px.histogram(df, x='ball_1', title='Frequency of Ball 1')
    graph = fig.to_html(full_html=False)
    return render(request, 'lottery_stats/stats.html', {'graph': graph})

