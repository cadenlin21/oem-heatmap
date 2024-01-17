# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import json
# import urllib.request
# import dash
# from dash import html, dcc, Input, Output, ALL
#
# # mapping from states to abbreivation
# us_state_to_abbrev = {
#     "Alabama": "AL",
#     "Alaska": "AK",
#     "Arizona": "AZ",
#     "Arkansas": "AR",
#     "California": "CA",
#     "Colorado": "CO",
#     "Connecticut": "CT",
#     "Delaware": "DE",
#     "Florida": "FL",
#     "Georgia": "GA",
#     "Hawaii": "HI",
#     "Idaho": "ID",
#     "Illinois": "IL",
#     "Indiana": "IN",
#     "Iowa": "IA",
#     "Kansas": "KS",
#     "Kentucky": "KY",
#     "Louisiana": "LA",
#     "Maine": "ME",
#     "Maryland": "MD",
#     "Massachusetts": "MA",
#     "Michigan": "MI",
#     "Minnesota": "MN",
#     "Mississippi": "MS",
#     "Missouri": "MO",
#     "Montana": "MT",
#     "Nebraska": "NE",
#     "Nevada": "NV",
#     "New Hampshire": "NH",
#     "New Jersey": "NJ",
#     "New Mexico": "NM",
#     "New York": "NY",
#     "North Carolina": "NC",
#     "North Dakota": "ND",
#     "Ohio": "OH",
#     "Oklahoma": "OK",
#     "Oregon": "OR",
#     "Pennsylvania": "PA",
#     "Rhode Island": "RI",
#     "South Carolina": "SC",
#     "South Dakota": "SD",
#     "Tennessee": "TN",
#     "Texas": "TX",
#     "Utah": "UT",
#     "Vermont": "VT",
#     "Virginia": "VA",
#     "Washington": "WA",
#     "West Virginia": "WV",
#     "Wisconsin": "WI",
#     "Wyoming": "WY",
#     "District of Columbia": "DC",
#     "American Samoa": "AS",
#     "Guam": "GU",
#     "Northern Mariana Islands": "MP",
#     "Puerto Rico": "PR",
#     "United States Minor Outlying Islands": "UM",
#     "U.S. Virgin Islands": "VI",
# }
#
# # mapping from abbreviations to states
# abbrev_to_us_state = dict(map(reversed, us_state_to_abbrev.items()))
#
# atc_locations = {
#     'Western Systems': pd.read_excel('heatmap_data.xlsx', sheet_name='Western Systems'),
#     'McCain': pd.read_excel('heatmap_data.xlsx', sheet_name="McCain"),
#     'Econolite': pd.read_excel('heatmap_data.xlsx', sheet_name="Econolite"),
#     'Q-Free': pd.read_excel('heatmap_data.xlsx', sheet_name="Q-Free"),
#     'Cubic': pd.read_excel('heatmap_data.xlsx', sheet_name="Cubic"),
#     'Temple': pd.read_excel('heatmap_data.xlsx', sheet_name="Temple"),
#     'Oriux': pd.read_excel('heatmap_data.xlsx', sheet_name="Oriux"),
#     'MoboTrex': pd.read_excel('heatmap_data.xlsx', sheet_name="MoboTrex"),
# }
#
# atc_regions = {
#     'Western Systems': pd.read_excel('heatmap_regions.xlsx', sheet_name='Western Systems'),
#     'McCain': pd.read_excel('heatmap_regions.xlsx', sheet_name="McCain"),
#     'Econolite': pd.read_excel('heatmap_regions.xlsx', sheet_name="Econolite"),
#     'Q-Free': pd.read_excel('heatmap_regions.xlsx', sheet_name="Q-Free"),
#     'Cubic': pd.read_excel('heatmap_regions.xlsx', sheet_name="Cubic"),
#     'Temple': pd.read_excel('heatmap_regions.xlsx', sheet_name="Temple"),
#     'Oriux': pd.read_excel('heatmap_regions.xlsx', sheet_name="Oriux"),
#     'MoboTrex': pd.read_excel('heatmap_regions.xlsx', sheet_name="MoboTrex"),
# }
#
# general_locations = {
#     'Western Systems': pd.read_excel('general_cities.xlsx', sheet_name='Western Systems'),
#     'McCain': pd.read_excel('general_cities.xlsx', sheet_name="McCain"),
#     'Econolite': pd.read_excel('general_cities.xlsx', sheet_name="Econolite"),
#     'Q-Free': pd.read_excel('general_cities.xlsx', sheet_name="Q-Free"),
#     'Cubic': pd.read_excel('general_cities.xlsx', sheet_name="Cubic"),
#     'Temple': pd.read_excel('general_cities.xlsx', sheet_name="Temple"),
#     'Oriux': pd.read_excel('general_cities.xlsx', sheet_name="Oriux"),
#     'MoboTrex': pd.read_excel('general_cities.xlsx', sheet_name="MoboTrex"),
# }
#
#
# offices = {
#     'Western Systems': pd.read_excel('heatmap_offices.xlsx', sheet_name='Western Systems'),
#     'McCain': pd.read_excel('heatmap_offices.xlsx', sheet_name="McCain"),
#     'Econolite': pd.read_excel('heatmap_offices.xlsx', sheet_name="Econolite"),
#     'Q-Free': pd.read_excel('heatmap_offices.xlsx', sheet_name="Q-Free"),
#     'Cubic': pd.read_excel('heatmap_offices.xlsx', sheet_name="Cubic"),
#     'Temple': pd.read_excel('heatmap_offices.xlsx', sheet_name="Temple"),
#     'Oriux': pd.read_excel('heatmap_offices.xlsx', sheet_name="Oriux"),
#     'MoboTrex': pd.read_excel('heatmap_offices.xlsx', sheet_name="MoboTrex"),
# }
#
# # Load your data
# data = pd.read_excel('heatmap_data.xlsx', sheet_name='Total')
#
# def get_companies_info(row):
#     companies_present = [company for company in offices.keys() if row[company] == 1]
#     companies_not_present = [company for company in offices.keys() if row[company] != 1]
#
#     companies_present_str = ', '.join(companies_present) if companies_present else 'None'
#     companies_not_present_str = ', '.join(companies_not_present) if companies_not_present else 'None'
#
#     return companies_present_str, companies_not_present_str
#
# data[['hover_text_present', 'hover_text_not_present']] = data.apply(get_companies_info, axis=1, result_type='expand')
# url = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"
# with urllib.request.urlopen(url) as response:
#     states_geojson = json.loads(response.read())
#
# app = dash.Dash(__name__,
#            suppress_callback_exceptions=True)
#
# server = app.server
#
#
# dropdown_options = [{'label': f'{i+1}. {oem}', 'value': oem} for i, oem in enumerate(offices.keys())]
# app.layout = html.Div([
#     dcc.RadioItems(
#         id='coverage-selection',
#         options=[
#             {'label': 'Total Coverage', 'value': 'total'},
#             {'label': 'View All OEMs', 'value': 'all'},
#             {'label': 'View Individual OEMs', 'value': 'individual'}
#         ],
#         value='total',  # Default value
#         style={'margin-bottom': '10px'}
#     ),
#     dcc.Checklist(
#         id='show-general-regions',
#         options=[
#             {'label': 'Show General Regions on Map', 'value': 'show_regions'}
#         ],
#         value=[],
#         style={'display': 'none'}  # Initially hidden
#     ),
#     html.Div(
#     dcc.Dropdown(
#         id='company-selector',
#         options=dropdown_options,
#         multi=True,
#         style={'display': 'none'}  # Remove width setting here
#     ),
#     style={'width': '30%'}  # Set the width on the wrapper div
#     ),
#     html.A(
#         id='qualitative-link',
#         children='Link to Qualitative Companion',
#         href='',  # Initially empty
#         target='_blank',  # Open link in a new tab
#         style={'display': 'block', 'margin-top': '20px', 'text-align': 'center'}
#     ),
#     html.Div(
#         id='maps-container',
#         style={'width': '100vw', 'height': '80vh', 'display': 'flex', 'flexDirection': 'column'}
#     ),
#     html.Div([
#         html.Ul([
#             html.Li([
#                 html.Span(style={'height': '10px', 'width': '10px', 'background-color': 'lightblue', 'border-radius': '0%', 'display': 'inline-block', 'margin-right': '5px'}),
#                 "Presence: Present if the OEM has some sort of presence in the state, such as a regional office or any traffic-related activity."
#             ], style={'list-style-type': 'none'}),
#             html.Li([
#                 html.Span(style={'height': '10px', 'width': '10px', 'background-color': 'red', 'border-radius': '50%', 'display': 'inline-block', 'margin-right': '5px'}),
#                 "ATC city: A specific city where the OEM has recently deployed OEMs."
#             ], style={'list-style-type': 'none'}),
#             html.Li([
#                 html.Span(style={'height': '15px', 'width': '15px', 'background-color': 'red', 'opacity': '50%','border-radius': '50%', 'display': 'inline-block', 'margin-right': '5px'}),
#                 "ATC city: A specific city where the OEM has recently deployed OEMs.""ATC region: A general region where the OEM has recently deployed OEMs."
#             ], style={'list-style-type': 'none'}),
#             html.Li([
#                 html.Span(style={'height': '10px', 'width': '10px', 'background-color': 'orange', 'border-radius': '50%', 'display': 'inline-block', 'margin-right': '5px'}),
#                 "General location: A specific city or general region where the OEM has targeted presence, though not necessarily ATC-related."
#             ], style={'list-style-type': 'none'}),
#     ])
#     ],
#     id='key-div', style={
#         'display': 'none',
#         'position': 'absolute',
#         'top': '10px',
#         'right': '10px',
#         'backgroundColor': 'white',
#         'border': '1px solid black',
#         'padding': '100px',
#         'margin-bottom': '100px',  # Increased space below the key
#         'z-index': '1000'
#     }),
#     html.Div(id='clicked-state-info', style={'fontSize': 20, 'marginTop': 20, 'textAlign': 'left'}),
#     html.Div(id='hidden-click-data', style={'display': 'none'})
# ])
#
#
# @app.callback(
#     Output('key-div', 'style'),
#     [Input('coverage-selection', 'value')]
# )
# def toggle_key_visibility(coverage_selection):
#     if coverage_selection == 'individual' or coverage_selection == 'all':
#         return {'position': 'absolute', 'top': '10px', 'right': '10px', 'backgroundColor': 'white', 'border': '1px solid black', 'padding': '10px', 'z-index': '1000'}
#     else:
#         return {'display': 'none'}
#
#
#
# @app.callback(
#     Output('show-general-regions', 'style'),
#     [Input('coverage-selection', 'value')]
# )
# def toggle_checklist_visibility(coverage_selection):
#     if coverage_selection in ['all', 'individual']:
#         return {'display': 'block'}  # Show the checklist
#     else:
#         return {'display': 'none'}  # Hide the checklist
#
# @app.callback(
#     Output('company-selector', 'style'),
#     Input('coverage-selection', 'value')
# )
# def toggle_dropdown(selection):
#     if selection == 'individual':
#         return {'display': 'block'}
#     else:
#         return {'display': 'none'}
#
#
# @app.callback(
#     Output('maps-container', 'children'),
#     [Input('coverage-selection', 'value'),
#      Input('company-selector', 'value'),
#      Input('show-general-regions', 'value')]
# )
# def update_maps(coverage_selection, selected_companies, show_general_regions):
#     maps = []
#     if not isinstance(selected_companies, list):
#         selected_companies = [selected_companies]
#     if coverage_selection == 'total':
#         data[['hover_text_present', 'hover_text_not_present']] = data.apply(get_companies_info, axis=1, result_type='expand')
#         fig = px.choropleth(
#             data,
#             geojson=states_geojson,
#             locations='State',
#             featureidkey="properties.name",
#             color='Total Coverage',
#             hover_data={'State': True, 'hover_text_present': True, 'hover_text_not_present': True},
#             scope="usa",
#             color_continuous_scale='Blues',
#             title='Total Coverage'
#         )
#         fig.update_traces(
#             hovertemplate="<b>%{customdata[0]}</b><br>OEMs present: %{customdata[1]}<br>OEMs not present: %{customdata[2]}<extra></extra>"
#         )
#         fig.update_geos(
#             center=dict(lat=39.8283, lon=-98.5795),
#             lataxis_range=[15, 50],  # Adjust as needed
#             lonaxis_range=[-125, -75]  # Adjust as needed
#         )
#         # maps.append(fig)
#         return [dcc.Graph(figure=fig, id='total-coverage-map')]
#     else:
#         if coverage_selection == 'all':
#             selected_companies = ['McCain', 'Econolite', 'Cubic', 'MoboTrex', 'Q-Free', 'Western Systems', 'Temple', 'Oriux']
#         if not selected_companies or not selected_companies[0]:
#             empty_fig = go.Figure(go.Scattergeo())
#             empty_fig.update_layout(
#                 geo=dict(scope='usa', showland=True, landcolor="LightGrey"),
#                 title='No companies selected'
#             )
#             return [
#                 dcc.Graph(figure=empty_fig, id='total-coverage-map')
#             ]
#         for i, company in enumerate(selected_companies):
#             filtered_data = data[['State', company]].copy()
#             filtered_data['Presence'] = filtered_data[company].apply(lambda x: 'Present' if x == 1 else 'Absent')
#
#             fig = px.choropleth(
#                 filtered_data,
#                 geojson=states_geojson,
#                 locations='State',
#                 featureidkey="properties.name",
#                 color='Presence',
#                 hover_data={'State': False, 'Presence': True},  # Explicitly set hover data
#                 # category_orders={'Key': ['Present', 'Absent']},
#                 color_discrete_map={'Present': 'lightblue', 'Absent': 'grey'},
#                 scope="usa",
#                 title=f"{company} Coverage"
#             )
#             fig.update_traces(
#                 hovertemplate="<b>%{properties.name}</b> - %{customdata[1]}<extra></extra>"
#             )
#
#             locations = atc_locations[company]
#             locations['city'] = ''
#             locations['state'] = ''
#             for index, row in locations.iterrows():
#                 parts = row['name'].split(', ')
#                 if len(parts) == 2:
#                     city, state = parts
#                     if state in abbrev_to_us_state:
#                         state = abbrev_to_us_state[state]
#                     locations.at[index, 'city'] = city
#                     locations.at[index, 'state'] = state
#                     locations.at[index, 'formatted_location'] = f"{state}: {city}"
#                 elif len(parts) == 1:
#                     city = parts[0]
#                     state = 'Unknown'  # or any default value
#                     locations.at[index, 'city'] = city
#                     locations.at[index, 'state'] = state
#                     locations.at[index, 'formatted_location'] = f"{city}"
#
#             sorted_locations = locations.sort_values(by=['state', 'city'])
#             cities_html_list = html.Ul([html.Li(loc) for loc in sorted_locations['formatted_location']])
#             locations['hover_text'] = locations['name'] + '<br>' + locations['comments']
#             if company == 'McCain':
#                 fig.add_trace(
#                     go.Scattergeo(
#                         lon=locations['lon'],
#                         lat=locations['lat'],
#                         hoverinfo='text',
#                         text=locations['hover_text'],
#                         marker=dict(size=7, color='red'),
#                         name=f"{company} ATC Cities"
#                     )
#                 )
#             else:
#                 fig.add_trace(
#                     go.Scattergeo(
#                         lon=locations['lon'],
#                         lat=locations['lat'],
#                         hoverinfo='text',
#                         text=locations['hover_text'],
#                         marker=dict(size=10, color='red'),
#                         name=f"{company} ATC Cities"
#                     )
#                 )
#
#             regions = atc_regions[company]
#             regions['city'] = ''
#             regions['state'] = ''
#             for index, row in regions.iterrows():
#                 parts = row['name'].split(', ')
#                 if len(parts) == 2:
#                     city, state = parts
#                     if state in abbrev_to_us_state:
#                         state = abbrev_to_us_state[state]
#                     regions.at[index, 'city'] = city
#                     regions.at[index, 'state'] = state
#                     regions.at[index, 'formatted_location'] = f"{state}: {city}"
#                 elif len(parts) == 1:
#                     city = parts[0]
#                     state = 'Unknown'  # or any default value
#                     regions.at[index, 'city'] = city
#                     regions.at[index, 'state'] = state
#                     regions.at[index, 'formatted_location'] = f"{city}"
#
#             sorted_regions = regions.sort_values(by=['state', 'city'])
#             if sorted_regions.empty:
#                 regions_html_list = None
#             else:
#                 regions_html_list = html.Ul([html.Li(loc) for loc in sorted_regions['formatted_location']])
#             regions['hover_text'] = regions['name'] + '<br>' + regions['comments']
#             if company == 'McCain':
#                 fig.add_trace(
#                     go.Scattergeo(
#                         lon=regions['lon'],
#                         lat=regions['lat'],
#                         hoverinfo='text',
#                         text=regions['hover_text'],  # Text labels
#                         marker=dict(
#                             size=13.5,
#                             color='LightCoral',
#                             opacity=0.7
#                         ),
#                         name=f"{company} ATC Regions"
#                     )
#                 )
#             else:
#                 fig.add_trace(
#                     go.Scattergeo(
#                         lon=regions['lon'],
#                         lat=regions['lat'],
#                         hoverinfo='text',
#                         text=regions['hover_text'],  # Text labels
#                         marker=dict(
#                             size=17.5,
#                             color='LightCoral',
#                             opacity=0.7
#                         ),
#                         name=f"{company} ATC Regions"
#                     )
#                 )
#
#
#             general_region_locations = general_locations[company]
#             general_region_locations['city'] = ''
#             general_region_locations['state'] = ''
#             general_region_locations['formatted_location'] = ''
#             for index, row in general_region_locations.iterrows():
#                 parts = row['name'].split(', ')
#                 if len(parts) == 2:
#                     city, state = parts
#                     if state in abbrev_to_us_state:
#                         state = abbrev_to_us_state[state]
#                     general_region_locations.at[index, 'city'] = city
#                     general_region_locations.at[index, 'state'] = state
#                     general_region_locations.at[index, 'formatted_location'] = f"{state}: {city}"
#                 elif len(parts) == 1:
#                     city = parts[0]
#                     state = 'Unknown'  # or any default value
#                     general_region_locations.at[index, 'city'] = city
#                     general_region_locations.at[index, 'state'] = state
#                     general_region_locations.at[index, 'formatted_location'] = f"{city}"
#
#             sorted_general_region_locations = general_region_locations.sort_values(by=['state', 'city'])
#             if not sorted_general_region_locations.empty:
#                 general_regions_html_list = html.Ul([html.Li(loc) for loc in sorted_general_region_locations['formatted_location']])
#             else:
#                 general_regions_html_list = None
#             general_region_locations['hover_text'] = general_region_locations['name'] + '<br>' + general_region_locations['comments']
#
#             if 'show_regions' in show_general_regions:
#                 fig.add_trace(
#                     go.Scattergeo(
#                         lon=general_region_locations['lon'],
#                         lat=general_region_locations['lat'],
#                         hoverinfo='text',
#                         text=general_region_locations['hover_text'],
#                         marker=dict(size=10, color='orange'),
#                         name=f"{company} General Regions"
#                     )
#                 )
#
#             office_locations = offices[company]
#             office_locations['city'] = ''
#             office_locations['state'] = ''
#             office_locations['formatted_location'] = ''
#             for index, row in office_locations.iterrows():
#                 parts = row['name'].split(', ')
#                 if len(parts) == 2:
#                     city, state = parts
#                     if state in abbrev_to_us_state:
#                         state = abbrev_to_us_state[state]
#                     office_locations.at[index, 'city'] = city
#                     office_locations.at[index, 'state'] = state
#                     office_locations.at[index, 'formatted_location'] = f"{state}: {city}"
#                 elif len(parts) == 1:
#                     city = parts[0]
#                     state = 'Unknown'  # or any default value
#                     office_locations.at[index, 'city'] = city
#                     office_locations.at[index, 'state'] = state
#                     office_locations.at[index, 'formatted_location'] = f"{city}"
#
#             sorted_office_locations = office_locations.sort_values(by=['state', 'city'])
#             if not sorted_office_locations.empty:
#                 sorted_office_list = html.Ul(
#                     [html.Li(loc) for loc in sorted_office_locations['formatted_location']])
#             else:
#                 sorted_office_list = None
#             sorted_office_locations['hover_text'] = sorted_office_locations['name'] + '<br>' + \
#                                                     sorted_office_locations['comments']
#             fig.add_trace(
#                 go.Scattergeo(
#                     lon=sorted_office_locations['lon'],
#                     lat=sorted_office_locations['lat'],
#                     hoverinfo='text',
#                     text=sorted_office_locations['hover_text'],  # Text labels
#                     marker=dict(
#                         size=10,
#                         color='Purple',
#                         opacity=1
#                     ),
#                     name=f"{company} Offices"
#                 )
#             )
#
#             fig.update_geos(
#                 center=dict(lat=39.8283, lon=-98.5795),
#                 lataxis_range=[15, 50],  # Adjust as needed
#                 lonaxis_range=[-125, -75]  # Adjust as needed
#             )
#             fig.update_layout(
#                 font=dict(family='Balto', size=15, color='black'),
#                 height=400,
#                 autosize=True,
#                 margin=dict(l=35, r=35, t=35, b=35)
#             )
#             # maps.append(fig)
#
#             map_id = json.dumps({'type': 'dynamic-map', 'index': company})
#             combined_layout = html.Div([
#                 dcc.Graph(figure=fig, id=map_id, style={'flex': '3', 'min-width': '300px'}),  # Map with flexible width
#                 html.Div([
#                     html.H5(f"{company} ATC Cities:"),
#                     cities_html_list,
#                     html.H5(f"{company} ATC Regions:"),
#                     regions_html_list,
#                     html.H5(f"{company} General Locations:"),
#                     general_regions_html_list,
#                     html.H5(f"{company} Offices:"),
#                     sorted_office_list
#                 ], style={'flex': '1', 'min-width': '200px', 'max-height': '400px', 'overflow-y': 'auto'})  # Scroll for long lists
#             ], style={'display': 'flex', 'width': '100%', 'align-items': 'stretch', 'margin-bottom': '20px'})
#
#             maps.append(combined_layout)
#
#     return maps
#
#
# @app.callback(
#     Output('qualitative-link', 'href'),
#     [Input('company-selector', 'value')]
# )
# def update_link(selected_company):
#     default_link = 'https://growthcommercial.sharepoint.com/:x:/s/GC/EYudFXChLs1HuMFH88MVMlEBJrZadQgTlA27aCspMkW5mA?e=v7cf66&nav=MTVfezU3ODMxQzJDLUE3QUItNEI5Qi1BQTdELTU3QUNFNzk4N0YyNX0'
#     return default_link
#
#
# @app.callback(
#     Output('clicked-state-info', 'children'),
#     [Input('total-coverage-map', 'clickData'),
#      Input('coverage-selection', 'value')],
#     prevent_initial_call=True
# )
# def display_clicked_state_info(clickData, coverage_selection):
#     if coverage_selection != 'total' or not clickData:
#         return ""
#
#     state_name = clickData['points'][0]['location']
#     state_info = data.loc[data['State'] == state_name, 'hover_text_present'].iloc[0]
#     not_state_info = data.loc[data['State'] == state_name, 'hover_text_not_present'].iloc[0]
#     return [
#         html.Div(f"State: {state_name}"),
#         html.Div(f"OEMs present: {state_info}"),
#         html.Div(f"OEMs not present: {not_state_info}")
#     ]
#
#
# if __name__ == '__main__':
#     app.run_server(debug=True)

# app.py
import dash
from dash import html, dcc, Input, Output
import oem_heatmap
import general_heatmap

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server
app.layout = html.Div([
    dcc.Dropdown(
        id='heatmap-selection',
        options=[
            {'label': 'OEM Heatmap', 'value': 'oem'},
            {'label': 'Demographic Heatmap', 'value': 'dem'},
        ],
        value='oem',
        style={'width': '50%', 'margin': '10px'}
    ),
    html.Div(id='page-content')
])

@app.callback(
    Output('page-content', 'children'),
    [Input('heatmap-selection', 'value')]
)
def update_page_layout(selected_heatmap):
    if selected_heatmap == 'oem':
        return oem_heatmap.layout()
    elif selected_heatmap == 'dem':
        return general_heatmap.layout()

# Register callbacks for both OEM and General heatmaps
oem_heatmap.register_callbacks(app)
general_heatmap.register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)

