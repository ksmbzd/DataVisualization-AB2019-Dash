import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html

data = pd.read_csv("../DataVisualization_AB_NYC2019/data/AB_NYC_2019.csv")

app = dash.Dash(__name__)

def get_first_chart():
    fig = px.histogram(data, x="price", color="neighbourhood_group", nbins=50, barmode="overlay",
                    title="Distribution of Prices by Neighborhood Group")
    fig.update_layout(xaxis_title="Price", yaxis_title="Count")
    return fig


def get_second_chart():
    fig = px.scatter_mapbox(data, lat="latitude", lon="longitude", color="neighbourhood_group", zoom=10,
                            title="Geographic Distribution by Neighborhood Group")
    fig.update_layout(mapbox_style="carto-positron")
    return fig

def get_third_chart():
    top_reviews = data.sort_values("number_of_reviews", ascending=False).iloc[:10]
    fig = px.bar(top_reviews, x="number_of_reviews", y="name", orientation="h",
                title="Top 10 Most Reviewed Listings")
    fig.update_layout(xaxis_title="Number of Reviews", yaxis_title="Listing Name")
    return fig


def get_fourth_chart():
    fig = px.box(data, x="room_type", y="price", color="neighbourhood_group",
              title="Distribution of Prices by Room Type and Neighborhood Group")
    fig.update_layout(xaxis_title="Room Type", yaxis_title="Price")    
    return fig


def get_fifth_chart():
    data["last_review"] = pd.to_datetime(data["last_review"])
    data["year_month"] = data["last_review"].dt.strftime("%Y-%m")
    avg_reviews = data.groupby("year_month")["reviews_per_month"].mean().reset_index()
    fig = px.line(avg_reviews, x="year_month", y="reviews_per_month",
                    title="Average Number of Reviews per Month Over Time")
    fig.update_layout(xaxis_title="Year-Month", yaxis_title="Average Reviews per Month")
    return fig


# The Layout for the Web APP
app.layout = html.Div([
    html.H1("New York City Air BNB Open Data Visualization", id="main-title"),
    html.H3("Prepared By: Kassem Bou Zeid", id="prepared-by"),
    html.Hr(),
    html.Div([
        dcc.Graph(figure=get_first_chart()),
        dcc.Graph(figure=get_second_chart())
    ], style={'display': 'flex'}),
    html.Hr(),
    html.Div([
        dcc.Graph(figure=get_third_chart()),
        dcc.Graph(figure=get_fourth_chart())
    ], style={'display': 'flex'}),
    html.Hr(),
    dcc.Graph(figure=get_fifth_chart())
])

# run the app
if __name__ == '__main__':
    app.run_server(debug=True)
