import pandas as pd
import json
import plotly.express as px


def plot_map(years, months, visitor_type, day_type):
    with open("palmas_coords.geojson") as geo_file:
        palmas_districts_map = json.load(geo_file)

    merged_df = pd.read_csv("gender_age_inc_visitors.csv", index_col=0)
    merged_df["district"] = merged_df["district"].apply(str)
    merged_df["district"] = merged_df["district"].str[:5]

    merged_cond = merged_df.loc[(merged_df["year"].isin(years)) & (merged_df["month"].isin(months)) & (
        merged_df["visitor_type"].isin(visitor_type)) & (merged_df["day_type"].isin(day_type))]

    grouped_data = merged_cond.groupby("district", as_index=False).sum()

    grouped_data.iloc[:, 4:-1] = (
                grouped_data.iloc[:, 4:-1].div(grouped_data["total_visitors"], axis=0) * 100).apply(
        lambda x: round(x))
    for col in grouped_data.iloc[:, 4:-1].columns:
        grouped_data[col] = (grouped_data[col].apply(str)) + "%"

    fig = px.choropleth_mapbox(grouped_data, geojson=palmas_districts_map, featureidkey="properties.CODIGO_INE",
                               locations='district',
                               color="total_visitors",
                               color_continuous_scale="portland",
                               range_color=(0, grouped_data["total_visitors"].max()),
                               mapbox_style="open-street-map", zoom=10,
                               opacity=0.4,
                               hover_data=list(grouped_data.iloc[:, 4:-1].columns),
                               center={"lat": 27.955, "lon": -15.58}
                               )
    fig.update_layout(width=1100, height=750, margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

