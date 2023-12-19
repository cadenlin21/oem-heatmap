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
    'McCain': pd.DataFrame({
        'lat': [33.4242, 30.0933, 34.0536, 30.5066, 33.1580, 32.9545, 42.6511, 42.8867, 34.1397, 41.1670, 37.7790, 39.7392, 32.7531, 32.8140, 38.9012, 33.4709, 33.4151, 33.1433, 30.2805, 44.9374, 35.4495, 33.7554, 41.5638, 34.3207, 29.8572, 42.3602, 33.7205, 36.0652, 37.3347, 36.3955, 36.1881, 47.1853, 34.9323],
        'lon': [-111.9280, -95.9886, -118.2427, -97.8303, -117.3505, -97.0150, -73.7549, -78.8783, -118.0353, -73.2048, -122.4199, -104.9848, -97.3327, -96.9488, -77.2652, -81.9748, -111.8314, -117.1661, -97.7389, -123.0272, -97.3967, -84.3883, -93.7593, -95.3930, -71.0582, -116.2155, -119.0167, -112.0741, -122.0090, 97.8783, -94.5404, -122.2928, -95.7697],
        'name': ['Arizona State University, AZ', 'Prairie View A&M University, TX', 'Los Angeles, CA', 'Cedar Park, TX', 'Carlsbad, CA', 'Coppell, TX', 'Albany, NY', 'Buffalo, NY', 'Arcadia, CA', 'Bridgeport, CT', 'San Francisco, CA', 'Denver, CO', 'Fort Worth, TX', 'Irving, TX', 'Vienna, VA', 'Augusta, GA', 'Mesa, AZ', 'San Marcos, CA', 'Texas DOT, TX', 'Oregon DOT, OR', 'Midwest City, OK', 'Georgia DOT, GA', 'West Des Moines, IA', 'Harris County, TX', 'Massachusetts DOT, MA', 'Indio, CA', 'Porterville, CA', 'Phoenix, AZ', 'Apple Campus, Cupertino, CA', 'Enid, OK', 'Siloam Springs, AR', 'Puyallup, WA', 'McAlester, OK']
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
    time_basis = " (June 2021 - April 2023)"  # Time basis string

    if selected_company == 'Total Coverage':
        title = 'Total Coverage' + time_basis
        fig = px.choropleth(data,
                            geojson=states_geojson,
                            locations='State',
                            featureidkey="properties.name",
                            color='Total Coverage',
                            scope="usa",
                            color_continuous_scale='Blues',
                            title=title)
    else:
        title = selected_company + time_basis
        filtered_data = data[['State', selected_company]].copy()
        filtered_data['Presence'] = filtered_data[selected_company].apply(lambda x: 'Present' if x == 1 else 'Absent')
        fig = px.choropleth(filtered_data,
                            geojson=states_geojson,
                            locations='State',
                            featureidkey="properties.name",
                            color='Presence',
                            color_discrete_map={'Present': 'blue', 'Absent': 'grey'},
                            scope="usa",
                            title=title)

    fig.update_geos(
        center=dict(lat=39.8283, lon=-98.5795),
        lataxis_range=[15, 50],  # Adjust as needed
        lonaxis_range=[-125, -75]  # Adjust as needed
    )

    if selected_company in company_locations:
        locations = company_locations[selected_company]
        fig.add_scattergeo(
            lon=locations['lon'],
            lat=locations['lat'],
            hoverinfo='text',
            hovertext=locations['name'],
            marker=dict(size=10, symbol='circle', color='red'),
            mode='markers+text',
            textposition='bottom center'
        )

    fig.write_html('heatmap.html')
    return fig


if __name__ == '__main__':
    app.run_server(debug=False)