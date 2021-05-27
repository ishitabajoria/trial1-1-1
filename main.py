# This is a sample Python script.


from datetime import date
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import datetime as dt
import urllib
import math

#JupyterDash.infer_jupyter_proxy_config()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Create server variable with Flask server object for use with gunicorn
server = app.server

scheme=pd.read_csv('https://raw.githubusercontent.com/ishitabajoria/mf_manager/main/scheme_data.csv').set_index('0')
opts=[]
temp=dict(scheme['Scheme NAV Name'])
for i in list(temp) :
    opt={}
    opt['label']=temp[i]
    opt['value']=i
    opts.append(opt)


def get_nav(date_inp, code):
    row = dict(scheme.loc[code])

    nav_history = pd.DataFrame()
    tp = row['tp']
    mf = row['mf']
    frmdt = date_inp.strftime('%d-%b-%Y')
    todt = date_inp.strftime('%d-%b-%Y')
    # print(frmdt.year,todt)
    days = (dt.datetime.now() - dt.datetime.strptime(frmdt, "%d-%b-%Y")).days
    row['days'] = days
    url = 'http://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?mf=' + str(mf) + '&tp=' + str(
        tp) + '&frmdt=' + frmdt + '&todt=' + todt

    file = urllib.request.urlopen(url)
    lines = []
    for line in file:
        nav_row = {}
        decoded_line = line.decode("utf-8")
        if decoded_line != ' \r\n':
            line = decoded_line.replace('\r\n', '')
            items = line.split(';')
            lines.append(items)
            # if r==7 :
            # print(items[0],int(row['Code']),items[0]==int(row['Code']))
            if items[0] == str(code):
                nav_row['date'] = items[-1]
                nav_row['value'] = items[4]
                nav_history = nav_history.append(nav_row, ignore_index=True)
    try:
        temp = list(nav_history['value'])
        row['current_nav'] = float(temp[-1])
        row['nav_history'] = nav_history
        return float(temp[0])
    except:
        return -2


app.layout = html.Div(
    [

        html.Br(),
        html.H1('Enter Transaction Details'),
        html.Label(
            id='name_input',
            children='Fund Name'),

        html.Div(
            [dcc.Dropdown(
                id='name-state',
                options=opts,
            )]
            , style={'width': 500}
        ),

        html.Div(),
        html.Label(
            id='account_input',
            children='Account'),
        html.Div(
            [dcc.Dropdown(
                id='account',
                options=[
                    {'label': 'MDB', 'value': 'MDB'},
                    {'label': 'KKB', 'value': 'KKB'},
                    {'label': 'Sima', 'value': 'Sima'},
                    {'label': 'Sunita', 'value': 'Sunita'},
                    {'label': 'Yogesh', 'value': 'YB'},
                    {'label': 'Aditya', 'value': 'AB'},
                    {'label': 'VLB', 'value': 'VLB'},
                    {'label': 'Ishita', 'value': 'IB'},
                ])], style={'width': 500}
        ),

        html.Div(),
        html.Label(
            id='type_input',
            children='Position'),
        dcc.RadioItems(
            options=[
                {'label': 'Buy', 'value': 'bought'},
                {'label': 'Sell', 'value': 'sold'},
            ], labelStyle={'display': 'inline-block'}),

        html.Br(),
        html.Label(
            id='date_input',
            children='Date of Transaction'),
        dcc.DatePickerSingle(
            id='tr_date-state',
            min_date_allowed=date(1995, 8, 5),
            max_date_allowed=date.today(),
            initial_visible_month=date.today(),
            date=date.today()
        ),

        html.Br(),
        html.Div(
            [
                html.Label(
                    id='amount_input',
                    children='Amount'),
                dcc.Input(id='amount-state', type="number", min=5000, step=100),

                html.Button(id='submit-button-state', n_clicks=0, children='Get NAV/Units',
                            style={'margin-left': 10, 'backgroundColor': 'LemonChiffon'}),

            ], style={'display': 'inline-block'}),

        html.Br(),
        html.Label(
            id='nav_output',
            children='NAV'),
        html.Div(id='NAV'),

        html.Div(),
        html.Label(
            id='units_input',
            children='Units'),
        dcc.Input(id='units', type="number"),

        html.Br(),
        html.Button(id='data-entry-state', n_clicks=0, children='Save Details',
                    style={'margin-top': 10, 'backgroundColor': 'Khaki'}),

        html.Br(),
        html.Div(id='outp')

    ], style={'margin-left': 50})


@app.callback(
    Output("units", "value"),
    Output("NAV", "children"),
    Input('submit-button-state', 'n_clicks'),
    State("amount-state", "value"),
    State("tr_date-state", "date"),
    State("name-state", "value"),

)
def update_output(n_clicks, amount, tr_date, name):
    # try :
    units = None
    nav = None
    if n_clicks >= 1:
        date = dt.datetime.strptime(tr_date, "%Y-%m-%d")
        temp = int(amount)
        nav = get_nav(date, name)
        # print(nav)
        # nav='NAV at date was : ' +str()
        units = round(temp / nav, 3)
    # except :
    # units=0
    # nav=''
    return units, nav


@app.callback(
    Output("outp", "children"),
    Input('data-entry-state', 'n_clicks'),
    Input("units", "value"),
    State("amount-state", "value"),
    State("tr_date-state", "date"),
    State("name-state", "value"),

)
def update_db(n_clicks, amount, tr_date, name, units):
    outp = None
    if n_clicks >= 1:
        outp = str(amount) + '  ' + str(tr_date) + '  ' + str(name) + '  ' + str(units)
    return outp


if __name__ == "__main__":
    print_hi('PyCharm')
    app.run_server(debug=True)




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
