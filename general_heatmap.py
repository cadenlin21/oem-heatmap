# general_heatmap.py
import plotly.express as px
from dash import html, dcc, Input, Output
import pandas as pd

# Define the layout for the General heatmap
def layout():
    return html.Div([
        dcc.Dropdown(
            id='general-data-selection',
            options=[
                {'label': 'GDP', 'value': 'gdp'},
                {'label': 'Population', 'value': 'population'},
                {'label': 'Growth Rate', 'value': 'growth_rate'},
                {'label': 'Median Income', 'value': 'median_income'},
                {'label': 'Number of Signalized Intersections', 'value': 'signalized_intersections'}
            ],
            value='gdp',  # Default value
            style={'width': '50%', 'margin': '10px'}
        ),
        dcc.Graph(id='general-heatmap')
    ])


# Function to generate sample GDP data
def generate_sample_gdp_data():
    # Sample GDP data for US states
    sample_data = {
        'State': ['CA', 'TX', 'NY', 'FL', 'IL'],
        'GDP': [3000000, 1800000, 1500000, 1000000, 800000]  # Sample GDP values
    }
    return pd.DataFrame(sample_data)

def generate_population_data():
    # Sample GDP data for US states
    sample_data = {
        'State': ['CA', 'TX', 'NY', 'FL', 'IL'],
        'Population': [3000000, 1800000, 1500000, 1000000, 800000]  # Sample GDP values
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
            df = generate_sample_gdp_data()
            fig = px.choropleth(
                df,
                locations='State',
                locationmode='USA-states',
                color='GDP',
                scope="usa",
                color_continuous_scale='Blues',
                title='US GDP by State'
            )
            return fig
        elif selected_data == 'population':
            df = generate_population_data()
            fig = px.choropleth(
                df,
                locations='State',
                locationmode='USA-states',
                color='Population',
                scope="usa",
                color_continuous_scale='Blues',
                title='US Population by State'
            )
            return fig
        elif selected_data == 'growth_rate':
            return px.choropleth()
        elif selected_data == 'median_income':
            return px.choropleth()
        elif selected_data == 'signalized_intersections':
            return px.choropleth()
