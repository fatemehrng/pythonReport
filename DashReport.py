import dash
import dash_html_components as html
import dash_core_components as dcc
import pypyodbc
import pandas as pd
import dash_table
from collections import deque
from datetime import datetime
from dash.dependencies import Input, Output
import plotly.graph_objects as go
# import matplotlib.pyplot as plt
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
sql_conn = pypyodbc.connect('Driver={SQL Server};Server=192.168.4.32\EPPADDBSERVER;Database=GetLastData_InsuranceKPI;UID=ETLUser;PWD=123456q!;')


cursor = sql_conn.cursor()
admin_conn = pypyodbc.connect(
    'Driver={SQL Server};Server=185.120.221.118,1433;Database=TransportInsuranceServerAdminDb;;UID=nima;PWD=123456q!')


app = dash.Dash(__name__
                , external_stylesheets=external_stylesheets
                )
app.layout = html.Div([
    #  Dropdown
    html.Div([
        dcc.Dropdown(
            id='corporate',
            options=[{'label': i, 'value': i} for i in {'ایران','آسیا'}],
            value='ایران'
        )
    ], style={'width': '10%', 'display': 'inline-block','padding': '0px 0px 0px 0px'}),
    # calender
    html.Div([
        dcc.DatePickerRange(
            id='CalenderRange',
            min_date_allowed=datetime(2000, 1, 1),
            max_date_allowed=datetime(2030, 1, 1),
            initial_visible_month=datetime.today(),
            end_date=datetime.today(),
        ),
        html.Div(id='outputRange')
    ], style={'width': '48%', 'float': 'right', 'display': 'inline-block', 'padding': '0px 0px 0px 0px'}),
    # be tafkik
    html.Div([
         html.Label(id='label2',
                    style={'display': 'inline-block', 'margin': '10'} ),
         dcc.Graph(id='graph1'), # this is the graph we add
    ], style={'width': '48%', 'display': 'inline-block','padding': '0px 0px 0px 0px'}),
    # hardo
    html.Div([
        html.Label(id='label3',
                   style={'display': 'inline-block', 'margin': '10'}),
        dcc.Graph(id='graph2'),  # this is the graph we add
    ], style={'width': '48%', 'float':'right', 'display': 'inline-block','padding': '0px 0px 0px 0px'}),
    # ByDatasender
    html.Div([
        html.Label(id='label4',
                   style={'display': 'inline-block', 'margin': '10'}),
        dcc.Graph(id='graph3'),  # this is the graph we add
    ], style={'width': '48%', 'float': 'right', 'display': 'inline-block', 'padding': '0px 0px 0px 0px'}),
    # speed
    html.Div([
        html.Label(id='label5',
                   style={'display': 'inline-block', 'margin': '10'}),
        dcc.Graph(id='graph4'),  # this is the graph we add
    ], style={'width': '48%', 'float': 'right', 'display': 'inline-block', 'padding': '0px 0px 0px 0px'}),

    #  DropdownContract
    html.Div([
        dcc.Dropdown(
            id='Contract',
            options=[{'label': i, 'value': i} for i in {'ایران', 'آسیا'}],
            value='ایران'
        )
    ], style={'width': '10%', 'display': 'inline-block', 'padding': '0px 0px 0px 0px'}),
    #  DropdownSenderID
    html.Div([
        dcc.Dropdown(
            id='SenderID',
            options=[{'label': i, 'value': i} for i in {'ایران', 'آسیا'}],
            value='ایران'
        )
    ], style={'width': '10%', 'display': 'inline-block', 'padding': '0px 0px 0px 0px'}),

    # baraye har gharardad
    html.Div([
        html.Label(id='label25',
                   style={'display': 'inline-block', 'margin': '10'}),
        dcc.Graph(id='graph5'),  # this is the graph we add
    ], style={'width': '48%', 'display': 'inline-block', 'padding': '0px 0px 0px 0px'}),


])
@app.callback([Output(component_id='graph1', component_property='figure')
              ,Output(component_id='graph2', component_property='figure')
              ,Output(component_id='graph3', component_property='figure')
              ,Output(component_id='graph4', component_property='figure')
              # ,Output(component_id='graph5', component_property='figure')
               ],
            [Input(component_id='corporate', component_property='value')
            ,Input(component_id='CalenderRange', component_property='start_date')
            ,Input(component_id='CalenderRange', component_property='end_date')
            # ,Input(component_id='table', component_property='options')
             ])
def update_graph1(corporate,start_date,end_date):
    dataSQL = []  # set an empty list
    X = deque(maxlen=10)
    Y = deque(maxlen=10)
    cursor.execute(
        'SELECT  COUNT(*) cont, billExportDate, sum (CASE WHEN Corporate.CorporateID = 11 THEN 1 ELSE 0 END ) iran,sum (CASE WHEN Corporate.CorporateID = 12 THEN 1 ELSE 0 END ) asia  '
        ' FROM [GetLastData_InsuranceKPI].[dbo].[TransportOrderALL]  '
        'JOIN dbo.Corporate ON Corporate.CorporateID = TransportOrderALL.corporateID WHERE billExportDateTime BETWEEN GETDATE()-30 AND GETDATE()'
        ' GROUP BY billExportDate  ORDER BY billExportDate')
    rows = cursor.fetchall()
    for row in rows:
        dataSQL.append(list(row))
        labels = ['num', 'date', 'iran','asia']
        df = pd.DataFrame.from_records(dataSQL, columns=labels)
        X = df['date']
        Y = df['iran'] if corporate == 'ایران' else df['asia']
        # iran = df['iran']
        # asia = df['asia']
    figure1 = {
        'data': [
            {'x':X, 'y':Y, 'type':'bar' },
        ],
        'layout': {
            'title': 'آمار روزانه به تفکیک بیمه'
        }
    }
    if start_date is  None:
        start_date = '2020-01-01'
    if end_date is  None:
        end_date = '2020-02-01'
    start_date = start_date[0:10]
    end_date = end_date[0:10]
    dataSQL = []  # set an empty list
    X = deque(maxlen=10)
    cursor.execute(
        'SELECT  COUNT(*) cont, billExportDate, sum (CASE WHEN Corporate.CorporateID = 11 THEN 1 ELSE 0 END ) iran,sum (CASE WHEN Corporate.CorporateID = 12 THEN 1 ELSE 0 END ) asia  '
        ' FROM [GetLastData_InsuranceKPI].[dbo].[TransportOrderALL]  '
        'JOIN dbo.Corporate ON Corporate.CorporateID = TransportOrderALL.corporateID WHERE billExportDateTime between ? and ? GROUP BY billExportDate  ORDER BY billExportDate',
        [start_date,end_date])
    rows = cursor.fetchall()
    for row in rows:
        dataSQL.append(list(row))
        labels = ['num', 'date', 'iran', 'asia']
        df = pd.DataFrame.from_records(dataSQL, columns=labels)
        X = df['date']
        iran = df['iran']
        asia = df['asia']
    figure2 = {
        'data': [
            # {'x': X, 'y': iran, 'type': 'bar'},
            {'x':X, 'y':iran, 'type':'bar' , 'name': 'ایران'},
            {'x':X, 'y':asia, 'type':'bar', 'name': 'آسیا'}
        ],
        'layout': {
            'title': 'آمار مقایسه ای بیمه ها'
        }
    }
    cursor.execute(
        'SELECT  CorporateName,dataSenderID , COUNT(*) cont  FROM [GetLastData_InsuranceKPI].[dbo].[TransportOrderALL]   JOIN dbo.Corporate ON Corporate.CorporateID = TransportOrderALL.corporateID  '
        'WHERE    billExportDateTime > DATEADD(HOUR, -1, GETDATE()) AND Corporate.CorporateID = 11 GROUP BY CorporateName,dataSenderID ORDER BY 2,1  ',
        [start_date,end_date])
    rows = cursor.fetchall()
    cursor.execute(
        'SELECT  CorporateName,dataSenderID , COUNT(*) cont  FROM [GetLastData_InsuranceKPI].[dbo].[TransportOrderALL]   JOIN dbo.Corporate ON Corporate.CorporateID = TransportOrderALL.corporateID  '
        'WHERE    billExportDateTime > DATEADD(HOUR, -1, GETDATE()) AND Corporate.CorporateID = 12 GROUP BY CorporateName,dataSenderID ORDER BY 2,1  ',
        [start_date,end_date])
    rows1 = cursor.fetchall()
    dataSQL = []  # set an empty list
    for row in rows:
        dataSQL.append(list(row))
        labels = ['corpratename', 'datasenderid', 'cont']
        df = pd.DataFrame.from_records(dataSQL, columns=labels)
        sender = df['datasenderid']
        cont = df['cont']
    for row in rows1:
        dataSQL.append(list(row))
        labels = ['corpratename', 'datasenderid', 'cont']
        df = pd.DataFrame.from_records(dataSQL, columns=labels)
        sender1 = df['datasenderid']
        cont1 = df['cont']
    figure3 = {
        'data': [
            {'x':sender, 'y':cont, 'type':'bar' , 'name': 'ایران'},
            {'x': sender1, 'y': cont1, 'type': 'bar', 'name': 'آسیا'},
        ],
        'layout': {
            'title': 'ارسال بارنامه ساعت اخیر به تفکیک datasender'
        }
    }
    cursor.execute(
        'SELECT   COUNT(*) cont  FROM [GetLastData_InsuranceKPI].[dbo].[TransportOrderALL]   JOIN dbo.Corporate ON Corporate.CorporateID = TransportOrderALL.corporateID  WHERE    billExportDateTime > DATEADD(HOUR, -1, GETDATE()) ')
    value = cursor.fetchall()
    # print(value[0][0])
    figure4 = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=value[0][0],
        mode="gauge+number",
        title={'text': "تعداد دریافت بارنامه در ساعت"},
        gauge={'axis': {'range': [None, 5000]},
               'steps': [
                   {'range': [0, 1000], 'color': "gray"},
                   {'range': [1000, 2000], 'color': "lightgray"}]
             ,
               'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 500}
               }))

    # Number 5

    dff = pd.read_sql_query(
        "SELECT   COUNT(*) count,ContractNumber  ContractNumber1,dataSenderID,sendDate FROM [GetLastData_InsuranceKPI]. [dbo].[TransportOrderALL] "
        "where ContractNumber is not null and sendDatetime > getdate() -90  GROUP by ContractNumber,ContractNumber,dataSenderID,sendDate",
        sql_conn)
    df2 = pd.read_sql_query(
        "select cr.ContractNumber ContractNumber2,b.Name BranchName,b.BranchID BranchID from dbo.Branch b "
        "join Corporate c on c.CorporateID = b.CorporateID join Agent a on a.BranchID = b.BranchID join Company co on co.agentid = a.AgentID "
        "join Contract cr on cr.companyid = co.companyid where   cr.ContractNumber is not null and b.BranchID= 43 ",
        admin_conn)
    dff.columns = dff.columns.str.strip()
    df2.columns = df2.columns.str.strip()
    result = dff.merge(df2, left_on='contractnumber1', right_on='contractnumber2', how='inner')

    # dates = result.loc[result['BranchID'] == 310]

    dates = result.loc[(result['branchid'] == 43) & (result['datasenderid'] == 0)]
    date1 = dates[['count', 'senddate', 'datasenderid']]
    G5 = (date1.groupby(['senddate', 'datasenderid']).sum())
    #
    # print(G5)
    # G5.plot.bar()
    # plt.show()

    # X = df['senddate']
    # Y = df['datasenderid']
    #
    #     if corporate == 'ایران' else df['asia']
    #     # iran = df['iran']
    #     # asia = df['asia']
    # figure1 = {
    #     'data': [
    #         {'x':X, 'y':Y, 'type':'bar' },
    #     ],
    #     'layout': {
    #         'title': 'آمار روزانه به تفکیک بیمه'
    #     }
    # }



    return figure1,figure2,figure3,figure4\
        # ,figure5

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)