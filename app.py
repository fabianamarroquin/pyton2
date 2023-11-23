import dash
import dash_bootstrap_components as dbc
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



stocks = ["PG", "TM", "BIMBOA.MX", "ABEV", "OR.PA", "INTC", "UNP", "PEP", "GIS", "JNJ"]
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=365 * 3)

def obtener_datos_accion(symbol, start, end):
    data = yf.download(symbol, start=start, end=end)
    return data["Adj Close"]

# Función para calcular rendimiento acumulado
def calcular_rendimiento_acumulado(datos):
    return (datos / datos.iloc[0] - 1) * 100

# Función para obtener datos de 'PortafolioSharpeMax' y 'PortafolioVolarilidadMin'
def ret_acumulado(start_date, end_date):

    return ret_acumulado_data
precio=yf.download(stocks,start=start,end=end)["Adj Close"]
precio
ret=precio.pct_change()
ret
retorno_medio=ret.mean()
retorno_medio

pesos1=np.array([0.0,0.0172,0.4665,0.0,0.2147,0.0,0.0,0.3015,0.0,0.0])

retorno_port=np.sum(retorno_medio*pesos1)

retorno_port


#retorno acumuladdo por acción a cada una de las fechas 
ret["PortafolioSharpeMax"]=ret.iloc[:,:10].dot(pesos1)

#calcular los retornos acumulados

ret_acumulado_data=(1+ret).cumprod()
ret_acumulado_data

#definir pesos de portafolio volatilidad


pesos2=np.array([0.0308,0.0969,0.0954,0.0191,0.1204,0.0072,0.0686,0.1108,0.1351,0.3156])
retorno_port=np.sum(retorno_medio*pesos2)
retorno_port

#retorno acumuladdo por acción a cada una de las fechas 

ret["PortafolioVolatilidadMin"]=ret.iloc[:,:10].dot(pesos2)
#calcular los retornos acumulados

ret_acumulado_data=(1+ret).cumprod()
ret_acumulado_data

# Creación de la aplicación Dash

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server=app.server

app.title= "Dashboard"

# Diseño del layout de la aplicación
app.layout = html.Div([
    html.H1("Dashboard de Acciones"),

    dcc.Dropdown(
        id='selector-acciones',
        options=[{'label': accion, 'value': accion} for accion in stocks],
        multi=True,
        value=['PG'],  
        style={'width': '50%'}
    ),

    dcc.Dropdown(
        id='selector-precio-o-rendimiento',
        options=[
            {'label': 'Precio', 'value': 'precio'},
            {'label': 'Rendimiento Acumulado', 'value': 'rendimiento'},
            {'label': 'Distribución portafolios', 'value': 'Distribución portafolios'}
        ],
        value='precio',
        style={'width': '50%'}
    ),

   dcc.RangeSlider(
    id='selector-fechas',
    marks={i: start_date + datetime.timedelta(days=i) for i in range(0, 365 * 3, 365)},
    min=0,
    max=365 * 3, 
    step=30,
    value=[0, 365 * 3]
),

    dcc.Graph(id='grafico-lineas'),
])

# Callback para actualizar el gráfico
@app.callback(
    Output('grafico-lineas', 'figure'),
    [Input('selector-acciones', 'value'),
     Input('selector-precio-o-rendimiento', 'value'),
     Input('selector-fechas', 'value')]
)
def actualizar_grafico(acciones_seleccionadas, selector, fechas):
    start_date_range = start_date + datetime.timedelta(days=fechas[0])
    end_date_range = start_date + datetime.timedelta(days=fechas[1])

    if selector == 'Distribución portafolios':
        # Obtén los datos de 'PortafolioSharpeMax' y 'PortafolioVolarilidadMin'
        ret_acumulado_data = ret_acumulado(start_date_range, end_date_range)

        fig = px.histogram(ret_acumulado_data, x=['PortafolioSharpeMax','PortafolioVolatilidadMin'
],
                         labels={'Date': 'Fecha', 'value': 'Valor'},
                         title=f"Distribución del Portafolio",
                         )

    else:
        datos = pd.DataFrame()
        for accion in acciones_seleccionadas:
            datos[accion] = obtener_datos_accion(accion, start_date_range, end_date_range)

        if selector == 'rendimiento':
            datos = calcular_rendimiento_acumulado(datos)

        fig = px.line(datos, x=datos.index, y=acciones_seleccionadas,
                      labels={'index': 'Fecha', 'value': selector},
                      title=f"{', '.join(acciones_seleccionadas)} - {selector}",
                      )

    return fig



if __name__ == '__main__':
    app.run_server(debug=False,host='0.0.0.0', port=10000)
