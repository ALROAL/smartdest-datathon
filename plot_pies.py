import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def plot_by_district_col(district, years, months, visitor_type, day_type):

    age_visitors = pd.read_csv("age_visitors.csv", index_col=0)
    gender_visitors = pd.read_csv("gender_visitors.csv", index_col=0)
    income_visitors = pd.read_csv("income_visitors.csv", index_col=0)

    districts_keys = pd.read_csv("districts.csv")

    df_gender = gender_visitors[(gender_visitors["district"] == district) & (gender_visitors["year"].isin(years)) & (
        gender_visitors["month"].isin(months))
                                & (gender_visitors["visitor_type"].isin(visitor_type)) & (
                                    gender_visitors["day_type"].isin(day_type))]
    df_age = age_visitors[(age_visitors["district"] == district) & (age_visitors["year"].isin(years)) & (
        age_visitors["month"].isin(months))
                          & (age_visitors["visitor_type"].isin(visitor_type)) & (
                              age_visitors["day_type"].isin(day_type))]
    df_income = income_visitors[(income_visitors["district"] == district) & (income_visitors["year"].isin(years)) & (
        income_visitors["month"].isin(months))
                                & (income_visitors["visitor_type"].isin(visitor_type)) & (
                                    income_visitors["day_type"].isin(day_type))]

    fig = make_subplots(rows=2, cols=2, specs=[[{"type": "domain"}, {"type": "domain"}],
                                               [{"type": "domain"}, {"type": "domain"}]])

    fig.add_trace(
        go.Pie(title="Visitors type",
               values=df_age.groupby("visitor_type", as_index=False).sum().sort_values("visitor_type")["visitors"],
               labels=df_age.groupby("visitor_type", as_index=False).sum().sort_values("visitor_type")["visitor_type"],
               sort=False,
               textinfo='percent+label',
               marker=dict(colors=px.colors.sequential.amp[::2], line=dict(color='#000000', width=1))
               ),
        row=1, col=1
    )

    fig.add_trace(
        go.Pie(title="Visitors gender",
               values=df_gender.groupby("gender", as_index=False).sum().sort_values("gender")["visitors"],
               labels=df_gender.groupby("gender", as_index=False).sum().sort_values("gender")["gender"],
               sort=False,
               textinfo='percent+label',
               marker=dict(colors=px.colors.sequential.Burg[::2], line=dict(color='#000000', width=1))
               ),
        row=1, col=2
    )

    fig.add_trace(
        go.Pie(title="Visitors age groups",
               values=df_age.groupby("age_group", as_index=False).sum().sort_values("age_group")["visitors"],
               labels=df_age.groupby("age_group", as_index=False).sum().sort_values("age_group")["age_group"],
               sort=False,
               textinfo='percent+label',
               marker=dict(colors=px.colors.sequential.Sunset[::2], line=dict(color='#000000', width=1))
               ),
        row=2, col=1
    )

    fig.add_trace(
        go.Pie(title=go.pie.Title(text="Visitors income levels", position="top center"),
               values=df_income.groupby("income_level", as_index=False).sum().sort_values("income_level")["visitors"],
               labels=df_income.groupby("income_level", as_index=False).sum().sort_values("income_level")[
                   "income_level"],
               sort=False,
               textinfo='percent+label',
               marker=dict(colors=px.colors.sequential.Bluyl[::2], line=dict(color='#000000', width=1))
               ),
        row=2, col=2
    )

    title = districts_keys[districts_keys.key == district]["name"].iloc[0]
    fig.update_layout(title_text=title, width=1200, height=1000, paper_bgcolor='#e3e3e3', title_y=0.95)
    fig.layout.font.size = 18
    return fig
