import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import urllib.request
import dash
from dash import html, dcc, Input, Output

company_links = {
    'McCain': 'https://growthcommercial.sharepoint.com/:x:/r/sites/GC/Shared%20Documents/Clients/Synapse%20ITS/Benchmarking/Qualitative%20Companion%20for%20Heatmap.xlsx?d=w70159d8b2ea147cdb8c147f3c3153251&csf=1&web=1&e=ikMnZe&nav=MTVfezU3ODMxQzJDLUE3QUItNEI5Qi1BQTdELTU3QUNFNzk4N0YyNX0',
    'Econolite': 'https://growthcommercial.sharepoint.com/:x:/r/sites/GC/Shared%20Documents/Clients/Synapse%20ITS/Benchmarking/Qualitative%20Companion%20for%20Heatmap.xlsx?d=w70159d8b2ea147cdb8c147f3c3153251&csf=1&web=1&e=IJf7JW&nav=MTVfezU0REFCQ0U2LTc3MDItNEUxMC1CQzNFLUM1MTY3QTI2QUVCM30',
    'Q-Free': 'https://growthcommercial.sharepoint.com/:x:/r/sites/GC/Shared%20Documents/Clients/Synapse%20ITS/Benchmarking/Qualitative%20Companion%20for%20Heatmap.xlsx?d=w70159d8b2ea147cdb8c147f3c3153251&csf=1&web=1&e=QyoK6Z&nav=MTVfezc3NzQxMTY5LTVDRDEtNDlERC1CNEYzLTJGMzFCNjA5QTkxNn0',
    'Cubic': 'https://growthcommercial.sharepoint.com/:x:/r/sites/GC/Shared%20Documents/Clients/Synapse%20ITS/Benchmarking/Qualitative%20Companion%20for%20Heatmap.xlsx?d=w70159d8b2ea147cdb8c147f3c3153251&csf=1&web=1&e=0fjmuN&nav=MTVfe0M2Q0Y1OUFELTQ2RkItNDc3Ny05NzZGLTA2OERFQTg0RUU1MH0',
    'Temple': 'https://growthcommercial.sharepoint.com/:x:/r/sites/GC/Shared%20Documents/Clients/Synapse%20ITS/Benchmarking/Qualitative%20Companion%20for%20Heatmap.xlsx?d=w70159d8b2ea147cdb8c147f3c3153251&csf=1&web=1&e=uD3PcH&nav=MTVfe0M2MDNBQkJBLUVCQkItNDVDOS1BQkExLTk4Nzc3QjFBMDVDRH0',
    'Oriux': 'https://growthcommercial.sharepoint.com/:x:/r/sites/GC/Shared%20Documents/Clients/Synapse%20ITS/Benchmarking/Qualitative%20Companion%20for%20Heatmap.xlsx?d=w70159d8b2ea147cdb8c147f3c3153251&csf=1&web=1&e=H80W4B&nav=MTVfezNBMzgzM0FELUU2OTgtNDc3NS04QzcxLTQ1N0JDQTI4MkQ2MX0',
    'Western Systems': 'https://growthcommercial.sharepoint.com/:x:/r/sites/GC/Shared%20Documents/Clients/Synapse%20ITS/Benchmarking/Qualitative%20Companion%20for%20Heatmap.xlsx?d=w70159d8b2ea147cdb8c147f3c3153251&csf=1&web=1&e=6CNDQo&nav=MTVfezQ1NjYzNEQ1LUU4MjQtNDdBQy05MUM5LTFENkE5QTRBRTFFMn0',
    'Mobotrex': 'https://growthcommercial.sharepoint.com/:x:/r/sites/GC/Shared%20Documents/Clients/Synapse%20ITS/Benchmarking/Qualitative%20Companion%20for%20Heatmap.xlsx?d=w70159d8b2ea147cdb8c147f3c3153251&csf=1&web=1&e=2pwIcr&nav=MTVfe0M1QUIyNEZCLTIyMTctNEZDNS05NEIwLTgxQTMyNzg0OUM3RX0'
}

# Load your data
data = pd.read_excel('heatmap_data.xlsx', sheet_name='Total')
def get_companies_present(row):
    companies_present = [company for company in company_links.keys() if row[company] == 1]
    companies_count = len(companies_present)
    companies_list = ', '.join(companies_present) if companies_present else 'None'
    return companies_count, companies_list

data[['OEMs_count', 'hover_text']] = data.apply(get_companies_present, axis=1, result_type='expand')
url = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"
with urllib.request.urlopen(url) as response:
    states_geojson = json.loads(response.read())

app = dash.Dash(__name__,
           suppress_callback_exceptions=True)

server = app.server
atc_locations = {
    'Western Systems': pd.read_excel('heatmap_data.xlsx', sheet_name='Western Systems'),
    'McCain': pd.read_excel('heatmap_data.xlsx', sheet_name="McCain"),
    'Econolite': pd.read_excel('heatmap_data.xlsx', sheet_name="Econolite"),
    'Q-Free': pd.read_excel('heatmap_data.xlsx', sheet_name="Q-Free"),
    'Cubic': pd.read_excel('heatmap_data.xlsx', sheet_name="Cubic"),
    'Temple': pd.read_excel('heatmap_data.xlsx', sheet_name="Temple"),
    'Oriux': pd.read_excel('heatmap_data.xlsx', sheet_name="Oriux"),
    'Mobotrex': pd.read_excel('heatmap_data.xlsx', sheet_name="Mobotrex"),
}

atc_regions = {
    'Western Systems': pd.read_excel('heatmap_regions.xlsx', sheet_name='Western Systems'),
    'McCain': pd.read_excel('heatmap_regions.xlsx', sheet_name="McCain"),
    'Econolite': pd.read_excel('heatmap_regions.xlsx', sheet_name="Econolite"),
    'Q-Free': pd.read_excel('heatmap_regions.xlsx', sheet_name="Q-Free"),
    'Cubic': pd.read_excel('heatmap_regions.xlsx', sheet_name="Cubic"),
    'Temple': pd.read_excel('heatmap_regions.xlsx', sheet_name="Temple"),
    'Oriux': pd.read_excel('heatmap_regions.xlsx', sheet_name="Oriux"),
    'Mobotrex': pd.read_excel('heatmap_regions.xlsx', sheet_name="Mobotrex"),
}

general_locations = {
    'Western Systems': pd.read_excel('general_cities.xlsx', sheet_name='Western Systems'),
    'McCain': pd.read_excel('general_cities.xlsx', sheet_name="McCain"),
    'Econolite': pd.read_excel('general_cities.xlsx', sheet_name="Econolite"),
    'Q-Free': pd.read_excel('general_cities.xlsx', sheet_name="Q-Free"),
    'Cubic': pd.read_excel('general_cities.xlsx', sheet_name="Cubic"),
    'Temple': pd.read_excel('general_cities.xlsx', sheet_name="Temple"),
    'Oriux': pd.read_excel('general_cities.xlsx', sheet_name="Oriux"),
    'Mobotrex': pd.read_excel('general_cities.xlsx', sheet_name="Mobotrex"),
}

app.layout = html.Div([
    dcc.RadioItems(
        id='coverage-selection',
        options=[
            {'label': 'Total Coverage', 'value': 'total'},
            {'label': 'View All OEMs', 'value': 'all'},
            {'label': 'View Individual OEMs', 'value': 'individual'}
        ],
        value='total',  # Default value
        style={'margin-bottom': '10px'}
    ),
    dcc.Checklist(
        id='show-general-regions',
        options=[
            {'label': 'Show General Regions', 'value': 'show_regions'}
        ],
        value=[],
        style={'display': 'none'}  # Initially hidden
    ),
    dcc.Dropdown(
        id='company-selector',
        options=[{'label': company, 'value': company} for company in data.columns if company not in ['State', 'Total Coverage', 'OEMs_count', 'hover_text']],
        multi=True,
        style={'display': 'none'}  # Initially hidden
    ),
    html.A(
        id='qualitative-link',
        children='Link to Qualitative Companion',
        href='',  # Initially empty
        target='_blank',  # Open link in a new tab
        style={'display': 'block', 'margin-top': '20px', 'text-align': 'center'}
    ),
    html.Div(
        id='maps-container',
        style={'width': '100vw', 'height': '80vh', 'display': 'flex', 'flexDirection': 'column'}
    ),
    html.Div(id='clicked-state-info', style={'fontSize': 20, 'marginTop': 20, 'textAlign': 'left'}),
    html.Div(id='hidden-click-data', style={'display': 'none'})
])

@app.callback(
    Output('show-general-regions', 'style'),
    [Input('coverage-selection', 'value')]
)
def toggle_checklist_visibility(coverage_selection):
    if coverage_selection in ['all', 'individual']:
        return {'display': 'block'}  # Show the checklist
    else:
        return {'display': 'none'}  # Hide the checklist

@app.callback(
    Output('company-selector', 'style'),
    Input('coverage-selection', 'value')
)
def toggle_dropdown(selection):
    if selection == 'individual':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('maps-container', 'children'),
    [Input('coverage-selection', 'value'),
     Input('company-selector', 'value'),
     Input('show-general-regions', 'value')]
)
def update_maps(coverage_selection, selected_companies, show_general_regions):
    maps = []
    if not isinstance(selected_companies, list):
        selected_companies = [selected_companies]
    if coverage_selection == 'total':
        data[['OEMs_count', 'hover_text']] = data.apply(get_companies_present, axis=1, result_type='expand')
        fig = px.choropleth(
            data,
            geojson=states_geojson,
            locations='State',
            featureidkey="properties.name",
            color='Total Coverage',
            hover_data={'State': True, 'OEMs_count': True, 'hover_text': True},
            scope="usa",
            color_continuous_scale='Blues',
            title='Total Coverage'
        )
        fig.update_traces(
            hovertemplate="<b>%{customdata[0]}</b><br>Number of OEMs: %{customdata[1]}<br>OEMs present: %{customdata[2]}<extra></extra>"
        )
        fig.update_geos(
            center=dict(lat=39.8283, lon=-98.5795),
            lataxis_range=[15, 50],  # Adjust as needed
            lonaxis_range=[-125, -75]  # Adjust as needed
        )
        maps.append(fig)
    else:
        if coverage_selection == 'all':
            selected_companies = ['McCain', 'Econolite', 'Cubic', 'Mobotrex', 'Q-Free', 'Western Systems', 'Temple', 'Oriux']
        if not selected_companies or not selected_companies[0]:
            empty_fig = go.Figure(go.Scattergeo())
            empty_fig.update_layout(
                geo=dict(scope='usa', showland=True, landcolor="LightGrey"),
                title='No companies selected'
            )
            return [
                dcc.Graph(figure=empty_fig, id='total-coverage-map')
            ]
        for i, company in enumerate(selected_companies):
            filtered_data = data[['State', company]].copy()
            filtered_data['Key'] = filtered_data[company].apply(lambda x: 'Present' if x == 1 else 'Absent')

            fig = px.choropleth(
                filtered_data,
                geojson=states_geojson,
                locations='State',
                featureidkey="properties.name",
                color='Key',
                category_orders={'Key': ['Present', 'Absent']},
                color_discrete_map={'Present': 'lightblue', 'Absent': 'grey'},
                scope="usa",
                title=f"{company} Coverage"
            )

            locations = atc_locations[company]
            fig.add_trace(
                go.Scattergeo(
                    lon=locations['lon'],
                    lat=locations['lat'],
                    hoverinfo='text',
                    text=locations['name'],
                    marker=dict(size=10, color='red'),
                    name=f"{company} ATC Cities"
                )
            )
            regions = atc_regions[company]
            fig.add_trace(
                go.Scattergeo(
                    lon=regions['lon'],
                    lat=regions['lat'],
                    hoverinfo='text',
                    text=regions['name'],
                    marker=dict(
                        size=17.5,
                        color='orange',
                        opacity=0.5
                    ),
                    name=f"{company} ATC Regions"
                )
            )
            if 'show_regions' in show_general_regions:
                general_region_locations = general_locations[company]
                fig.add_trace(
                    go.Scattergeo(
                        lon=general_region_locations['lon'],
                        lat=general_region_locations['lat'],
                        hoverinfo='text',
                        text=general_region_locations['name'],
                        marker=dict(size=10, color='yellow'),
                        name=f"{company} General Regions"
                    )
                )
            fig.update_geos(
                center=dict(lat=39.8283, lon=-98.5795),
                lataxis_range=[15, 50],  # Adjust as needed
                lonaxis_range=[-125, -75]  # Adjust as needed
            )
            maps.append(fig)

    for fig in maps:
        fig.update_layout(
            font=dict(family='Balto', size=15, color='black'),
            autosize=True,
            margin=dict(l=35, r=35, t=35, b=35)
        )
    if coverage_selection == 'total':
        return [dcc.Graph(figure=fig, id='total-coverage-map') for fig in maps]
    return [dcc.Graph(figure=fig, id='total-coverage-map') for fig in maps]


@app.callback(
    Output('qualitative-link', 'href'),
    [Input('company-selector', 'value')]
)
def update_link(selected_company):
    # Default link if company is not found in the dictionary
    default_link = 'https://growthcommercial.sharepoint.com/:x:/s/GC/EYudFXChLs1HuMFH88MVMlEBJrZadQgTlA27aCspMkW5mA?e=v7cf66&nav=MTVfezU3ODMxQzJDLUE3QUItNEI5Qi1BQTdELTU3QUNFNzk4N0YyNX0'
    return default_link


@app.callback(
    Output('clicked-state-info', 'children'),
    [Input('total-coverage-map', 'clickData'),
     Input('coverage-selection', 'value')],
    prevent_initial_call=True
)
def display_clicked_state_info(clickData, coverage_selection):
    if coverage_selection != 'total' or not clickData:
        return ""

    state_name = clickData['points'][0]['location']
    state_info = data.loc[data['State'] == state_name, 'hover_text'].iloc[0]
    oems_count = data.loc[data['State'] == state_name, 'OEMs_count'].iloc[0]
    return [
        html.Div(f"State: {state_name}"),
        html.Div(f"Number of OEMs: {oems_count}"),
        html.Div(f"OEMs present: {state_info}")
    ]

if __name__ == '__main__':
    app.run_server(debug=True)