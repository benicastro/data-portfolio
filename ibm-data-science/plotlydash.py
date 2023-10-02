# Import needed modules/libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the csv data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Extract the unique launch sites
launch_sites = [{"label": "All Sites", "value": "All Sites"}]
unique_launch_sites = spacex_df["Launch Site"].unique().tolist()
for site in unique_launch_sites:
    launch_sites.append({"label": site, "value": site})

# Get max and min payload mass
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40},
        ),
        # TASK 1: Add a Launch Site Drop-down Input Component
        # We have four different launch sites and we would like to first see
        # which one has the largest success count. Then, we would like to select
        # one specific site and check its detailed success rate (class=0 vs. class=1).
        dcc.Dropdown(
            id="site-dropdown",
            options=launch_sites,
            placeholder="Select a Launch Site Here",
            value="All Sites",
            searchable=True,
        ),
        html.Br(),
        # TASK 2.1: Add a Pie Chart Showing the Successful Launches for All Sites
        html.Div(dcc.Graph(id="success-pie-chart")),
        html.Br(),
        html.P("Payload Range (kg):"),
        # TASK 3: Add a Range Slider to Select Payload
        dcc.RangeSlider(
            id="payload-slider",
            min=0,
            max=10000,
            step=1000,
            marks={x: f"{x} kg" for x in range(0, 10001, 1000)},
            value=[min_payload, max_payload],
        ),
        # TASK 4.1: Add a Scatter Plot to Show the Correlation Between Payload and Launch Success
        html.Div(dcc.Graph(id="success-payload-scatter-chart")),
    ]
)


# TASK 2.2: Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value"),
)
def get_pie_chart(launch_site):
    if launch_site == "All Sites":
        df = spacex_df[spacex_df["class"] == 1]
        fig = px.pie(
            df,
            names="Launch Site",
            hole=0.3,
            title="Total Success Launches By all sites",
        )
    else:
        df = spacex_df.loc[spacex_df["Launch Site"] == launch_site]
        fig = px.pie(
            df,
            names="class",
            hole=0.3,
            title="Total Success Launches for site " + launch_site,
        )
    return fig


# TASK 4.2: Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    [
        Input(component_id="site-dropdown", component_property="value"),
        Input(component_id="payload-slider", component_property="value"),
    ],
)
def get_payload_chart(launch_site, payload_mass):
    if launch_site == "All Sites":
        fig = px.scatter(
            spacex_df[
                spacex_df["Payload Mass (kg)"].between(payload_mass[0], payload_mass[1])
            ],
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            hover_data=["Launch Site"],
            title="Correlation Between Payload and Success for All Sites",
        )
    else:
        df = spacex_df[spacex_df["Launch Site"] == str(launch_site)]
        fig = px.scatter(
            df[df["Payload Mass (kg)"].between(payload_mass[0], payload_mass[1])],
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            hover_data=["Launch Site"],
            title="Correlation Between Payload and Success for Site {}".format(
                launch_site
            ),
        )
    return fig


# Run the app
if __name__ == "__main__":
    app.run_server()
