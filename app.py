import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import yfinance as yf
import datetime
import pandas as pd
import numpy as np
import plotly.express as px
from pypfopt import risk_models, expected_returns
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import plotting
import pyfolio as pf
import warnings 
import scipy.stats as stats
import matplotlib.pyplot as plt
import math 
warnings.filterwarnings("ignore")


TasaInteres= pd.read_csv("tasainteres.csv")
Inflacion=pd.read_csv("inflacion.csv")
PIB=pd.read_csv("PIB.csv")

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


app.title="Dashboard"

app.layout = html.Div([
    html.H1("Indicadores Económicos"),
    
    dcc.Dropdown(
        id='variablesdd',
        options=[
            {'label': 'PIB', 'value': 'PIB'},
            {'label': 'Tasa de Interés', 'value': 'Tasa de Interés'},
            {'label': 'Inflación', 'value': 'Inflación'}
        ],
        value='PIB',  
        clearable=False  
    ),
    
    # Gráfica 
    dcc.Graph(id='grafica-indicador'),
    
    # Tabla con Dash 
    dash_table.DataTable(id='tabla_detalles'),
    
    html.Button("descargar csv",id="Descargar",n_clicks=0),
    dcc.Download(id="Descargar csv")
])



@app.callback(
    [Output('grafica-indicador', 'figure'),
     Output('tabla_detalles', 'data')],
    [Input('variablesdd', 'value')]
)
def update_data(selected_data):
    fig = None
    tabla_detalles = []

    if selected_data == 'PIB':
        fig = px.line(PIB, x='Año', y='PIB', title='PIB',markers=True)
        tabla_detalles = PIB.to_dict('records')
        
    elif selected_data == 'Tasa de Interés':
        fig = px.box(TasaInteres, x='Mes', y='TasaInteres', title='Tasa de Interés')
       
    elif selected_data == 'Inflación':
        fig = px.histogram(Inflacion, x='inflacion', title='Inflacion' ,nbins=15,template="simple_white",text_auto=True)
       

    return fig, tabla_detalles


@app.callback(
    Output('Descargar csv',"data"),
    [Input("Descargar","n_clicks")],
    prevent_initial_call=True
)
def descargar_csv(n_clicks):
    if n_clicks > 0:
        df = pd.DataFrame(tabla_detalles)
        csv_string = df.to_csv(index=False, encoding='utf-8-sig')
        csv_string = "data:text/csv;charset=utf-8-sig," + csv_string
        csv_string = csv_string.encode('utf-8-sig')
        return dict(content=csv_string, filename="data.csv")


if __name__ == '__main__':
    app.run_server(debug=False,host='0.0.0.0', port=10000)        
