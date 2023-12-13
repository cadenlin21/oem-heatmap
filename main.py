import pandas as pd
import plotly.express as px
import json
import urllib.request
import dash
from dash import html, dcc, Input, Output

# Install the required packages by running:
# pip install plotly pandas

# Load your data
data = pd.read_csv('Heatmap data.csv')  # Replace with your data file
# colorscale = ["rgb(128, 128, 128)", "rgb(210, 231, 154)", "rgb(94, 179, 39)", "rgb(67, 136, 33)", "rgb(33, 74, 12)"]
# # Load GeoJSON for US states
# url = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"
# with urllib.request.urlopen(url) as response:
#     states_geojson = json.loads(response.read())
#
# # Create the choropleth map
# fig = px.choropleth(data_frame=data,
#                     geojson=states_geojson,
#                     locations='State',  # Replace with your column name for states
#                     featureidkey="properties.name",  # Path in GeoJSON to the state name
#                     color_continuous_scale=colorscale,
#                     color='OEMs_Present',  # Replace with your column name for the values
#                     scope="usa",
#                     title='OEM Coverage Map')
#
# fig.update_geos(fitbounds="locations", visible=False)
# fig.write_html('heatmap.html')
# fig.show()


url = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"
with urllib.request.urlopen(url) as response:
    states_geojson = json.loads(response.read())

app = dash.Dash(__name__)
server = app.server
company_locations = {
    'Western Systems': pd.DataFrame({
        'lat': [42.3265, 32.7157, 34.0961, 34.3917, 38.7296, 37.6688, 36.6002],
        'lon': [-122.8756, -117.1611, -118.1058, -118.5426, -120.7985, -122.0810, -121.8947],
        'name': ['Medford, OR', 'San Diego, CA', 'San Gabriel, CA', 'Santa Clarita, CA', 'Placerville, CA', 'Hayward, CA', 'Monterey, CA']
    }),

}
# company_locations = {
#     'McCain': pd.DataFrame({
#         'lat': [34.0522, 36.7783, 42.3265],  # Example latitudes
#         'lon': [-118.2437, -119.4179, -122.8756],  # Example longitudes
#         'name': ['Location 1', 'Location 2']  # Names or descriptions of locations
#     }),
#     # Add similar DataFrames for other companies
# }

app.layout = html.Div([
    dcc.Dropdown(
        id='company-selector',
        options=[{'label': company, 'value': company} for company in data.columns if company != 'State'],
        value='Total Coverage'
    ),
    dcc.Graph(
        id='choropleth-map',
        style={'height': '80vh', 'width': '100%'}  # Adjust the height and width as needed
    )
])

@app.callback(
    Output('choropleth-map', 'figure'),
    [Input('company-selector', 'value')]
)
def update_map(selected_company):
    if selected_company == 'Total Coverage':
        # Handle the total number of companies
        fig = px.choropleth(data,
                            geojson=states_geojson,
                            locations='State',
                            featureidkey="properties.name",
                            color='Total Coverage',
                            scope="usa",
                            color_continuous_scale='Blues')
    else:
        # Handle individual companies
        filtered_data = data[['State', selected_company]].copy()
        filtered_data['Presence'] = filtered_data[selected_company].apply(lambda x: 'Present' if x == 1 else 'Absent')
        fig = px.choropleth(filtered_data,
                            geojson=states_geojson,
                            locations='State',
                            featureidkey="properties.name",
                            color='Presence',
                            color_discrete_map={'Present': 'blue', 'Absent': 'grey'},
                            scope="usa")

    fig.update_geos(fitbounds="locations", visible=False)
    if selected_company in company_locations:
        locations = company_locations[selected_company]
        fig.add_scattergeo(
            lon=locations['lon'],
            lat=locations['lat'],
            hoverinfo='text',  # Show only custom text
            hovertext=locations['name'],  # Custom text for each marker
            marker=dict(size=10, symbol='circle', color='red'),
            mode='markers+text',
            textposition='bottom center'
        )

    fig.write_html('heatmap.html')
    return fig

if __name__ == '__main__':
    app.run_server(debug=False)