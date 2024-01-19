# general_heatmap.py
import plotly.express as px
from dash import html, dcc, Input, Output
import pandas as pd
import json
import numpy as np

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
                {'label': 'DOT Spend Per Capita', 'value': 'dot'},
                {'label': 'Growth Rate', 'value': 'growth'}
            ],
            value='gdp',  # Default value
            style={'width': '50%', 'margin': '10px'}
        ),
        html.Div(
            dcc.Graph(id='general-heatmap'),
            style={'width': '100vw', 'height': '80vh'}  # Adjust the width and height as needed
        )
    ])


df = pd.read_excel('Demographic info for all 50 states & Canada provinces.xlsx')
gdp = df[['State/Province', 'gdp', 'gdp (bil)']]
pop = df[['State/Province', 'Population']]
inc = df[['State/Province', 'Median Income']]
dot = df[['State/Province', 'DOT Funds Per Capita']]
growth = df[['State/Province', 'GDP Growth Rate']]
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
            df['log_gdp'] = np.log2(df['gdp'])
            df['gdp_rounded'] = df['gdp (bil)'].round()
            # Calculate logarithmic range for color scale
            fig = px.choropleth(
                df,
                geojson=combined_geojson,
                locations='State/Province',
                featureidkey="properties.name",
                color='log_gdp',
                scope="north america",
                color_continuous_scale='blues',
                title='GDP by State',
                hover_data={'State/Province': True, 'gdp_rounded': True}  # Show actual GDP in hover, hide LogData
            )
            fig.update_traces(
                hovertemplate="<b>%{customdata[0]}</b><br>GDP: $%{customdata[1]:,} billion<extra></extra>"
            )
            # Calculate tick values and labels for log base 2 scale
            tickvals = np.linspace(df['log_gdp'].min(), df['log_gdp'].max(), num=5)
            ticktext = [f"${(2 ** val) / 10**9:,.0f} billion" for val in tickvals]
            fig.update_layout(
                coloraxis_colorbar=dict(
                    title='GDP',
                    tickvals=tickvals,
                    ticktext=ticktext
                ),
                font=dict(family='Balto', size=15, color='black'),
                height=1000,
                autosize=True,
                margin=dict(l=35, r=35, t=35, b=35)
            )
            return fig
        elif selected_data == 'population':
            df = pop
            df['log_pop'] = np.log2(df['Population'])
            df['pop_rounded'] = round(df['Population'] / 1000000, 1)
            tickvals = np.linspace(df['log_pop'].min(), df['log_pop'].max(), num=5)
            ticktext = [f"{(2 ** val) / 10 ** 6:,.0f} million" for val in tickvals]
            fig = px.choropleth(
                df,
                geojson=combined_geojson,
                locations='State/Province',
                featureidkey="properties.name",
                color='log_pop',
                scope="north america",
                color_continuous_scale='Blues',
                title='Population by State',
                hover_data={'State/Province': True, 'pop_rounded': True}
            )
            fig.update_traces(
                hovertemplate="<b>%{customdata[0]}</b><br>Population: %{customdata[1]:,} million<extra></extra>"
            )
            fig.update_layout(
                coloraxis_colorbar=dict(
                    title='Population',
                    tickvals=tickvals,
                    ticktext=ticktext
                ),
                font=dict(family='Balto', size=15, color='black'),
                height=1000,
                autosize=True,
                margin=dict(l=35, r=35, t=35, b=35)
            )
            return fig
        elif selected_data == 'income':
            df = inc
            df['rounded'] = round(df['Median Income'])
            fig = px.choropleth(
                df,
                geojson=combined_geojson,
                locations='State/Province',
                featureidkey="properties.name",
                color='Median Income',
                scope="north america",
                color_continuous_scale='Blues',
                title='Median Income by State',
                hover_data={'State/Province': True, 'rounded': True}  # Show actual GDP in hover, hide LogData
            )
            fig.update_traces(
                hovertemplate="<b>%{customdata[0]}</b><br>Median income: $%{customdata[1]:,}<extra></extra>"
            )
            fig.update_layout(
                font=dict(family='Balto', size=15, color='black'),
                height=1000,
                autosize=True,
                margin=dict(l=35, r=35, t=35, b=35)
            )
            return fig
        elif selected_data == 'dot':
            df = dot
            df['log_dot'] = np.log10(df['DOT Funds Per Capita'])
            df['dot_rounded'] = round(df['DOT Funds Per Capita'], 1)
            tickvals = np.linspace(df['log_dot'].min(), df['log_dot'].max(), num=5)
            ticktext = [f"${(10 ** val):,.0f} " for val in tickvals]
            fig = px.choropleth(
                df,
                geojson=combined_geojson,
                locations='State/Province',
                featureidkey="properties.name",
                color='log_dot',
                scope="north america",
                color_continuous_scale='Blues',
                title='DOT Spend Per Capita by State',
                hover_data={'State/Province': True, 'dot_rounded': True}  # Show actual GDP in hover, hide LogData
            )
            fig.update_traces(
                hovertemplate="<b>%{customdata[0]}</b><br>DOT Spend Per Capita: $%{customdata[1]:,}<extra></extra>"
            )
            fig.update_layout(
                coloraxis_colorbar=dict(
                    title='DOT Spend Per Capita',
                    tickvals=tickvals,
                    ticktext=ticktext
                ),
                font=dict(family='Balto', size=15, color='black'),
                height=1000,
                autosize=True,
                margin=dict(l=35, r=35, t=35, b=35)
            )
            return fig
        elif selected_data == 'growth':
            df = growth
            df['rounded'] = round(df['GDP Growth Rate'] * 100, 1)
            tickvals = np.linspace(df['rounded'].min(), df['rounded'].max(), num=5)
            ticktext = [f"{(val):,.0f}% " for val in tickvals]
            fig = px.choropleth(
                df,
                geojson=combined_geojson,
                locations='State/Province',
                featureidkey="properties.name",
                color='rounded',
                scope="north america",
                color_continuous_scale='Blues',
                title='Growth Rate by State',
                hover_data={'State/Province': True, 'rounded': True}
            )
            fig.update_traces(
                hovertemplate="<b>%{customdata[0]}</b><br>Growth rate: %{customdata[1]:,}%<extra></extra>"
            )
            fig.update_layout(
                coloraxis_colorbar=dict(
                    title='Growth Rate',
                    tickvals=tickvals,
                    ticktext=ticktext
                ),
                font=dict(family='Balto', size=15, color='black'),
                height=1000,
                autosize=True,
                margin=dict(l=35, r=35, t=35, b=35)
            )
            return fig
