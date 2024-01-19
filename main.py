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

