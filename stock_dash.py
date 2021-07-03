import pandas as pd
import plotly.graph_objs as go
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output

# -----------------------------------------Reading CSVs------------------------------------------------------------------
df = pd.read_csv('https://raw.githubusercontent.com/AtharvaKatre/Dash-StockAnalyzer/main/assets/datasets/csv_23.csv')
df2 = pd.read_csv('https://raw.githubusercontent.com/AtharvaKatre/Dash-StockAnalyzer/main/assets/datasets/csv1.csv')
df3 = pd.read_csv('https://raw.githubusercontent.com/AtharvaKatre/Dash-StockAnalyzer/main/assets/datasets/csv4.csv')

# -----------------------------------------APP Definition---------------------------------------------------------------
FONT_AWESOME = "https://use.fontawesome.com/releases/v5.7.2/css/all.css"
BOOTSTRAP_ICONS = "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.4.1/font/bootstrap-icons.css"
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MATERIA, FONT_AWESOME, BOOTSTRAP_ICONS],
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}]
                )
app.title = 'Stock Analyzer'
server = app.server


# -----------------------------------------Stock Price Chart------------------------------------------------------------
def candle_chart(df, stock, fontcolor='black'):
    df1 = df[df['stock'] == stock].drop('Date', axis=1)
    df1['Date'] = pd.to_datetime(df[df['stock'] == stock]['Date'])
    fig = go.Figure(data=[go.Candlestick(x=df1['Date'],
                                         open=df1['sma20'],
                                         high=df1['upper'],
                                         low=df1['lower'],
                                         close=df1['close'])])
    fig.update_xaxes(showspikes=True, spikesnap="cursor", spikemode="across")
    fig.update_yaxes(showspikes=True, spikesnap="cursor", spikemode="across")
    fig.update_layout(title='<b>{}'.format(stock),
                      yaxis=dict(side='right', title='Price (USD)'),
                      xaxis_rangeslider_visible=True,
                      hovermode="x",
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      margin=dict(t=40, b=15),
                      font_color=fontcolor,
                      template='plotly_white')
    fig.update_xaxes(rangeslider_bgcolor='#CDCDCD')
    return fig


def price_chart(df, stock, fontcolor='black'):
    dff = df[df['stock'] == stock].drop('Date', axis=1)
    dff['Date'] = pd.to_datetime(df[df['stock'] == stock]['Date'])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dff['Date'], y=dff['close'], name='Close', marker_color='skyblue'))
    fig.add_trace(go.Scatter(x=dff['Date'], y=dff['sma20'], name='SMA20', marker_color='red'))
    fig.add_trace(go.Scatter(x=dff['Date'], y=dff['upper'], name='Upper', marker_color='green'))
    fig.add_trace(go.Scatter(x=dff['Date'], y=dff['lower'], name='Lower', marker_color='gold'))
    # fig.update_xaxes(showspikes=True, spikesnap="cursor", spikemode="across")
    # fig.update_yaxes(showspikes=True, spikesnap="cursor", spikemode="across")
    fig.update_layout(title='<b>{}'.format(stock),
                      yaxis=dict(title='Price (USD)'),
                      xaxis_rangeslider_visible=True,
                      hovermode="x",
                      margin=dict(t=40, b=15),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      font_color=fontcolor,
                      template='plotly_white')
    fig.update_xaxes(rangeslider_bgcolor='#CDCDCD')
    return fig


def row2tabledata(stock_name, candle):
    dff = df3[(df3['stock'] == stock_name) & (df3['window'] == '100day') & (df3['candle'] == candle)].drop(
        ['stock', 'window', 'candle'], axis=1).reset_index(drop=True)
    dff.loc[len(dff.index)] = ['Total', round(dff['buyClose'].sum(), 2), round(dff['sellOpen'].sum(), 2)]
    return dff


def row3tabledata(stock_name, window):
    dff = df3[(df3['stock'] == stock_name) & (df3['window'] == window) & (df3['candle'] == 'day')].drop(
        ['stock', 'window', 'candle'], axis=1).reset_index(drop=True)
    dff.loc[len(dff.index)] = ['Total', round(dff['buyClose'].sum(), 2), round(dff['sellOpen'].sum(), 2)]
    return dff


# ------------------------------------------APP Components---------------------------------------------------------------
# theme switcher
theme_switch = dbc.Checklist(
    options=[{"label": "🌙", "value": 1, }],
    value=[],
    id="theme switch",
    labelStyle={'font-size': 'large', },
    switch=True,
)

# dropdown
stock_dropdown = dcc.Dropdown(
    id='stock-dropdown',
    options=[{'label': i, 'value': i} for i in df['stock'].unique()],
    value='ACC',
    placeholder='Select Stock',
    searchable=True,
    clearable=True,
)


# row 3 candle dropdown
def get_windowdropdown(id):
    window_dropdown = dcc.Dropdown(
        id=id,
        options=[{'label': i, 'value': i} for i in df3['window'].unique()],
        placeholder='Select Window',
        clearable=True,
    )
    return window_dropdown


# top banner
top_block = dbc.Row([
    dbc.Col(html.H2([html.B('Stock Analyzer ', id='app-title'),
                     html.B(className="fas fa-chart-line", style={'color': 'orange'})],
                    className='mt-2'), width=4, xs=9, lg=10),
    dbc.Col(theme_switch, className='mt-3', xs=1),
    # dbc.Col(html.H4(id='moon',className='fas fa-moon mt-3 ml-1')),
    # dbc.Col(dbc.Row([theme_switch,html.H4(id='moon',className='fas fa-moon')],justify='right'),width={'offset':5},className='mt-3', xs=3),
])

# chart card
card_style = {}
price_card1 = dbc.Card([
    dcc.Loading(dcc.Graph(
        id='price-chart1',
        style={'height': 250},
        config={'displayModeBar': False, 'displaylogo': False}
    ), color='orange')
], style=card_style, className='border border-dark')
price_card2 = dbc.Card([
    dcc.Loading(dcc.Graph(
        id='price-chart2',
        style={'height': 250},
        config={'displayModeBar': False, 'displaylogo': False}
    ), color='orange')
], style=card_style, className='border border-dark')

# Row 1 Table
table1 = dash_table.DataTable(
    id='row1-table1',
    data=[],
    columns=[{"name": i, "id": i} for i in ['Metric', 'Value']],
    style_header={
        'border': '1px solid black',
        'backgroundColor': 'cornflowerblue',
        'fontWeight': 'bold',
        'whiteSpace': 'normal',
        'textAlign': 'left'
    },
    style_cell={
        'font_size': '15px',
        'color': 'black',
        'border': '1px solid grey',
        'textAlign': 'left',
        'text-transform': 'uppercase',
        'maxWidth': 10,
    },
    style_data_conditional=[
        {
            'if': {'row_index': 'even'},
            'backgroundColor': 'lavender'
        },
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'ghostwhite'
        },
    ],
    style_table={'height': '250px', 'overflowY': 'auto'}
)


# Row 2  & Row 3 Tables
def row2_3tables(id):
    table = dash_table.DataTable(
        id=id,
        data=[],
        columns=[{"name": i, "id": i} for i in ['day', 'buyClose', 'sellOpen']],
        style_header={
            'border': '1px solid black',
            'backgroundColor': 'cornflowerblue',
            'fontWeight': 'bold',
            'whiteSpace': 'normal',
            'textAlign': 'center'
        },
        style_cell={
            'font_size': '12px',
            'color': 'black',
            'border': '1px solid black',
            'textAlign': 'center',
            'text-transform': 'uppercase',
            'maxWidth': 2,
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'even'},
                'backgroundColor': 'lavender'
            },
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'ghostwhite'
            },
            {
                'if': {
                    'filter_query': '{buyClose} < 0',
                    'column_id': 'buyClose'
                },
                'backgroundColor': 'tomato',
                'color': 'white'
            },
            {
                'if': {
                    'filter_query': '{sellOpen} < 0',
                    'column_id': 'sellOpen'
                },
                'backgroundColor': 'tomato',
                'color': 'white'
            },
            {
                'if': {
                    'filter_query': '{buyClose} > 0',
                    'column_id': 'buyClose'
                },
                'backgroundColor': 'seagreen',
                'color': 'white'
            },
            {
                'if': {
                    'filter_query': '{sellOpen} > 0',
                    'column_id': 'sellOpen'
                },
                'backgroundColor': 'seagreen',
                'color': 'white'
            },
            {
                'if': {
                    'filter_query': '{day} = "Total"'
                },
                'fontWeight': 'bold',
                'font_size': '14px',
            },
        ],
        style_table={'height': '250px', 'overflowY': 'auto'}
    )
    return table


# ------------------------------------------APP Layout-------------------------------------------------------------------
app.layout = dbc.Container([
    top_block,
    dbc.Row(dbc.Col(stock_dropdown, width=2, className='mt-3', xs=5, lg=2)),
    html.Div(id="blank_output"),
    dcc.Loading([
        dbc.Row([
            dbc.Col([table1], className='mt-3', xs=11, lg=3),
            dbc.Col([price_card1], className='mt-3', xs=12, lg=5),
            dbc.Col([price_card2], className='mt-3', xs=12, lg=4),
        ], justify='center'),
        html.Br(),
        dbc.Row([
            html.H5(className='rectangle ml-2', style={'width': '10px', 'backgroundColor': 'darkslateblue'}),
            dbc.Col(html.H5(html.B('100 Day Window'), id='row2-title'), xs=12, lg=3,
                    style={'padding': 10})
        ], className='mt-4'),
        dbc.Row([
            dbc.Col([dbc.Row(html.P(html.B('1 Day'), className='text-center'), justify='center'),
                     dbc.Row(dbc.Col(row2_3tables(id='row2-table1'), lg=12))], xs=6, lg=3),
            dbc.Col([dbc.Row(html.P(html.B('3 min'), className='text-center'), justify='center'),
                     dbc.Row(dbc.Col(row2_3tables(id='row2-table2'), lg=12))], xs=6, lg=3),
            dbc.Col([dbc.Row(html.P(html.B('5 min'), className='text-center'), justify='center'),
                     dbc.Row(dbc.Col(row2_3tables(id='row2-table3'), lg=12))], xs=6, lg=3),
            dbc.Col([dbc.Row(html.P(html.B('15 min'), className='text-center'), justify='center'),
                     dbc.Row(dbc.Col(row2_3tables(id='row2-table4'), lg=12))], xs=6, lg=3),
        ]),
        dbc.Row([
            html.H5(className='rectangle ml-2', style={'width': '10px', 'backgroundColor': 'darkslateblue'}),
            dbc.Col(html.H5(html.B('Compare Window'), id='row3-title'), xs=12, lg=3,
                    style={'padding': 10})
        ], className='mt-4 mb-2'),
        dbc.Row([
            dbc.Col([dbc.Row(dbc.Col(get_windowdropdown(id='window-filter1'), lg=12), justify='center'),
                     dbc.Row(dbc.Col(row2_3tables(id='row3-table1'), lg=12), className='mt-1')], xs=6, lg=3),
            dbc.Col([dbc.Row(dbc.Col(get_windowdropdown(id='window-filter2'), lg=12), justify='center'),
                     dbc.Row(dbc.Col(row2_3tables(id='row3-table2'), lg=12), className='mt-1')], xs=6, lg=3),
            dbc.Col([dbc.Row(dbc.Col(get_windowdropdown(id='window-filter3'), lg=12), justify='center'),
                     dbc.Row(dbc.Col(row2_3tables(id='row3-table3'), lg=12), className='mt-1')], xs=6, lg=3),
            dbc.Col([dbc.Row(dbc.Col(get_windowdropdown(id='window-filter4'), lg=12), justify='center'),
                     dbc.Row(dbc.Col(row2_3tables(id='row3-table4'), lg=12), className='mt-1')], xs=6, lg=3),
        ], className='mb-2'),
    ], color='orange'),
], fluid=True)


# -------------------------------------------APP Callbacks----------------------------------------------------------------
@app.callback(
    Output('price-chart1', 'figure'),
    Output('price-chart2', 'figure'),
    Output('row1-table1', 'data'),
    Output('row2-table1', 'data'),
    Output('row2-table2', 'data'),
    Output('row2-table3', 'data'),
    Output('row2-table4', 'data'),
    Output('row3-table1', 'data'),
    Output('row3-table2', 'data'),
    Output('row3-table3', 'data'),
    Output('row3-table4', 'data'),
    Input('stock-dropdown', 'value'),
    Input('window-filter1', 'value'),
    Input('window-filter2', 'value'),
    Input('window-filter3', 'value'),
    Input('window-filter4', 'value'),
    Input("theme switch", "value")
)
def update_graph(stock_name, window1, window2, window3, window4, theme):
    if theme == [1]:
        fontcolor = 'white'
    else:
        fontcolor = 'black'

    if stock_name is not None:
        t_df1 = df2[df2['stock'] == stock_name].T.reset_index()
        t_df1.columns = ["Metric", "Value"]

        return (
        candle_chart(df, stock_name, fontcolor), price_chart(df, stock_name, fontcolor), t_df1.to_dict('records'),
        # row 2 tables
        row2tabledata(stock_name, 'day').to_dict('records'),
        row2tabledata(stock_name, '3minute').to_dict('records'),
        row2tabledata(stock_name, '5minute').to_dict('records'),
        row2tabledata(stock_name, '15minute').to_dict('records'),
        # row 3 tables
        row3tabledata(stock_name, window1).to_dict('records'),
        row3tabledata(stock_name, window2).to_dict('records'),
        row3tabledata(stock_name, window3).to_dict('records'),
        row3tabledata(stock_name, window4).to_dict('records'),
        )
    else:
        t_df1 = df2[df2['stock'] == 'ACC'].T.reset_index()
        t_df1.columns = ["Metric", "Value"]
        t_df1['Value'] = '--'

        return {'layout': {'title': 'No stock selected', 'plot_bgcolor': 'rgba(0,0,0,0)',
                           'paper_bgcolor': 'rgba(0,0,0,0)'}}, {
                   'layout': {'title': 'No stock selected', 'plot_bgcolor': 'rgba(0,0,0,0)',
                              'paper_bgcolor': 'rgba(0,0,0,0)'}}, t_df1.to_dict(
            'records'), [], [], [], [], [], [], [], []


# window filter update dropdown values
@app.callback(
    Output('window-filter1', 'options'),
    Output('window-filter2', 'options'),
    Output('window-filter3', 'options'),
    Output('window-filter4', 'options'),
    Input('window-filter1', 'value'),
    Input('window-filter2', 'value'),
    Input('window-filter3', 'value'),
    Input('window-filter4', 'value'),
)
def update_dropdown(w1, w2, w3, w4):
    option1 = df3['window'].unique().tolist()
    selected = []
    if w2 is not None:
        selected.append(w2)
    if w3 is not None:
        selected.append(w3)
    if w4 is not None:
        selected.append(w4)
    for i in selected:
        option1.remove(i)

    option2 = df3['window'].unique().tolist()
    selected = []
    if w1 is not None:
        selected.append(w1)
    if w3 is not None:
        selected.append(w3)
    if w4 is not None:
        selected.append(w4)
    for i in selected:
        option2.remove(i)

    option3 = df3['window'].unique().tolist()
    selected = []
    if w1 is not None:
        selected.append(w1)
    if w2 is not None:
        selected.append(w2)
    if w4 is not None:
        selected.append(w4)
    for i in selected:
        option3.remove(i)

    option4 = df3['window'].unique().tolist()
    selected = []
    if w1 is not None:
        selected.append(w1)
    if w2 is not None:
        selected.append(w2)
    if w3 is not None:
        selected.append(w3)
    for i in selected:
        option4.remove(i)

    return [{'label': i, 'value': i} for i in option1], [{'label': i, 'value': i} for i in option2], [
        {'label': i, 'value': i} for i in option3], [{'label': i, 'value': i} for i in option4]


# theme switcher
app.clientside_callback(
    """
    function(selected) {

        let url = "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/materia/bootstrap.min.css"
        if (selected.length > 0) {
            url= "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/slate/bootstrap.min.css"
        }

        // Select the theme stylesheets .
        var stylesheets = document.querySelectorAll('link[rel=stylesheet][href^="https://stackpath"]')
        // Update the url of the main stylesheet.
        stylesheets[stylesheets.length - 1].href = url
        // Delay update of the url of the buffer stylesheet.
        setTimeout(function() {stylesheets[0].href = url;}, 100);
    }
    """,
    Output("blank_output", "children"),
    Input("theme switch", "value"),
)


@app.callback(
    Output("app-title", "style"),
    Output("row2-title", "style"),
    Output("row3-title", "style"),
    Input("theme switch", "value")
)
def change_color(value):
    if value == [1]:
        text_color = {'color': 'white'}
        rowtitle_style = {'text-decoration': 'underline', 'color': 'white'}
        return text_color, rowtitle_style, rowtitle_style
    else:
        text_color = {'color': 'black'}
        rowtitle_style = {'text-decoration': 'underline', 'color': 'black'}
        return text_color, rowtitle_style, rowtitle_style


if __name__ == '__main__':
    app.run_server(debug=False, port=8008)
