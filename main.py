import pandas as pd
import plotly.express as px
import json
import urllib.request
import dash
from dash import html, dcc, Input, Output


data = pd.read_csv('Heatmap data.csv')

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

    fig.update_geos(
        center=dict(lat=39.8283, lon=-98.5795),
        lataxis_range=[15, 50],  # Adjust as needed
        lonaxis_range=[-125, -75]  # Adjust as needed
    )

    # fig.update_layout(height=300)  # Adjust the height as needed

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
    app.run_server(debug=True)