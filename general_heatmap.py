# general_heatmap.py
import plotly.express as px
from dash import html, dcc, Input, Output
import pandas as pd
import json

with open('combined-us-canada-with-states-provinces_793.geojson') as f:
    combined_geojson = json.load(f)


# Define the layout for the General heatmap
def layout():
    return html.Div([
        dcc.Dropdown(
            id='general-data-selection',
            options=[
                {'label': 'GDP', 'value': 'gdp'},
                {'label': 'Population', 'value': 'population'},
                {'label': 'Median Income', 'value': 'income'},
                {'label': 'DOT Spend Per Capita', 'value': 'dot'}
            ],
            value='gdp',  # Default value
            style={'width': '50%', 'margin': '10px'}
        ),
        dcc.Graph(id='general-heatmap')
    ])


df = pd.read_excel('Demographic info for all 50 states & Canada provinces.xlsx')
gdp = df[['State/Province', 'GDP']]
pop = df[['State/Province', 'Population']]
inc = df[['State/Province', 'Median Income']]
dot = df[['State/Province', 'DOT Funds Per Capita']]

def generate_sample_data():
    # Sample data for Canadian provinces
    sample_data = {
        'State/Province': ['Ontario', 'Quebec', 'British Columbia', 'Alberta', 'Manitoba', 'California'],
        'Data': [1000, 800, 600, 400, 200, 500]  # Sample data values
    }
    return pd.DataFrame(sample_data)

# Register callbacks for the General heatmap
def register_callbacks(app):
    @app.callback(
        Output('general-heatmap', 'figure'),
        [Input('general-data-selection', 'value')]
    )

    def update_general_heatmap(selected_data):
        if selected_data == 'gdp':
            df = gdp
            fig = px.choropleth(
                df,
                geojson=combined_geojson,
                locations='State/Province',
                featureidkey="properties.name",
                color='GDP',
                scope="north america",
                color_continuous_scale='Blues',
                title='GDP by State'
            )
            return fig
        elif selected_data == 'population':
            df = pop
            fig = px.choropleth(
                df,
                geojson=combined_geojson,
                locations='State/Province',
                featureidkey="properties.name",
                color='Population',
                scope="north america",
                color_continuous_scale='Blues',
                title='Population by State'
            )
            return fig
        elif selected_data == 'income':
            df = inc
            fig = px.choropleth(
                df,
                geojson=combined_geojson,
                locations='State/Province',
                featureidkey="properties.name",
                color='Median Income',
                scope="north america",
                color_continuous_scale='Blues',
                title='Population by State'
            )
            return fig
        elif selected_data == 'dot':
            df = dot
            fig = px.choropleth(
                df,
                geojson=combined_geojson,
                locations='State/Province',
                featureidkey="properties.name",
                color='DOT Funds Per Capita',
                scope="north america",
                color_continuous_scale='Blues',
                title='Population by State'
            )
            return fig
