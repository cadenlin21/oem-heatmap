import dash
from dash import html, dcc, Input, Output, State
import oem_heatmap
import general_heatmap

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Define the correct password
CORRECT_PASSWORD = 'edi'

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='password-page', children=[
        dcc.Input(id='password-input', type='password', placeholder='Enter password', n_submit=0),
        html.Button('Submit', id='submit-val', n_clicks=0),
        html.Div(id='error-message', children='Incorrect password', style={'display': 'none', 'color': 'red'})
    ]),
    html.Div(id='content', style={'display': 'none'}, children=[
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
])

@app.callback(
    Output('content', 'style'),
    Output('password-page', 'style'),
    Output('error-message', 'style'),
    [Input('submit-val', 'n_clicks'), Input('password-input', 'n_submit')],
    [State('password-input', 'value')]
)
def validate_password(n_clicks, n_submit, input_value):
    ctx = dash.callback_context

    if not ctx.triggered:
        return {'display': 'none'}, {'display': 'block'}, {'display': 'none'}

    if input_value == CORRECT_PASSWORD:
        return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}
    else:
        return {'display': 'none'}, {'display': 'block'}, {'display': 'block'}



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

