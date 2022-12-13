# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 11:34:07 2022

@author: nverm
"""

# =============================================================================
# !pip install yfinance
# !pip install plotly
# =============================================================================

import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import gann
import math

#%%
pio.renderers.default = 'browser'


#%%

adorfo = yf.Ticker('AXISCADES.NS')
date = "2021-03-21"
hist = adorfo.history(start=date)

maxDate = np.datetime64(max(hist.index).date()) + np.timedelta64(365, 'D') # change here for future date

range_ = max(hist['High']) - min(hist['Low'])

maximum = max(hist['High']) * 1.15 # change here for maximum price
minimum = min(hist['Low']) * 0.85 # change here for minimum price


gannSquare = gann.GannSquare(1001, np.datetime64(date))

mul = 1

if hist['Close'][0] < 100:
    mul = 10

if hist['Close'][0] < 10:
    mul = 100

if hist['Close'][0] < 1:
    mul = 1000

multiplier = mul # change here   

hist['Close'] = hist['Close'] * multiplier
hist['Open'] = hist['Open'] * multiplier
hist['High'] = hist['High'] * multiplier
hist['Low'] = hist['Low'] * multiplier

#%%

hist['diff'] = hist['Close'] - hist['Open']
hist.loc[hist['diff']>=0, 'color'] = 'green'
hist.loc[hist['diff']<0, 'color'] = 'red'

#%%

# fig = go.Figure(data=go.Scatter(x=hist.index, y=hist['Close'], mode='lines+markers'))
# fig.show()

# fig2 = make_subplots(specs=[[{'secondary_y':True}]])
# fig2.add_trace(go.Scatter(x=hist.index, y=hist['Close'], name='Price'), secondary_y=False)
# fig2.add_trace(go.Bar(x=hist.index, y=hist['Volume'], name='Volume'), secondary_y=True)

# fig2.show()

fig3 = make_subplots(specs=[[{'secondary_y':True}]])

indexx = [i.date() for i in hist.index]

fig3.add_trace(go.Candlestick(x=indexx,
                              open=hist['Open'],
                              high=hist['High'],
                              low=hist['Low'],
                              close=hist['Close'],
                              name='Price')
                              )

#fig3.add_trace(go.Scatter(x=hist.index, y=hist['Close'].rolling(window=20).mean(), marker_color='blue', name='20 DMA'))

#fig3.add_trace(go.Bar(x=hist.index, y=hist['Volume'], marker={'color':hist['color']}), secondary_y=True)

fig3.update_layout(title={'text':'ADORFO.BO', 'x':0.5})
fig3.update_yaxes(range=[minimum, maximum])
fig3.update_layout(xaxis_rangeslider_visible=False)
fig3.update_yaxes(visible=False, secondary_y=True)
# =============================================================================
# fig3.update_xaxes(rangebreaks= [dict(bounds=['sat', 'mon'])])
# =============================================================================


angle_0, date_angle_0 = gannSquare.get_0()
angle_45, date_angle_45 = gannSquare.get_45()
angle_90, date_angle_90 = gannSquare.get_90()
angle_135, date_angle_135 = gannSquare.get_135()
angle_180, date_angle_180 = gannSquare.get_180()
angle_225, date_angle_225 = gannSquare.get_225()
angle_270, date_angle_270 = gannSquare.get_270()
angle_315, date_angle_315 = gannSquare.get_315()

dateCount = 0

def calcLevel(price):
    intsqrt = int(math.sqrt(price))
    
    if intsqrt % 2 == 1:
        if intsqrt ** 2 == price:
            return int(intsqrt/2)
        else:
            return int(intsqrt/2 + 1)
    else:
        return int(intsqrt/2 + 1)

for i in range(len(angle_0)):
    if angle_0[i] < maximum and angle_0[i] > minimum:
        l = calcLevel(angle_0[i])
        fig3.add_hline(y=angle_0[i], line_color='black', line_width=1.5, annotation_text=str(l) + ": 0")

for i in range(len(date_angle_0)):
    if date_angle_0[i] < maxDate:
        xx = (date_angle_0[i] - np.datetime64('1970-01-01'))/ np.timedelta64(1, 's')
        fig3.add_vline(x=xx * 1000, line_color='black', line_width=1.5, annotation_text="0, " + str(date_angle_0[i]))
    

for i in range(len(angle_45)):
    if angle_45[i] < maximum and angle_45[i] > minimum:
        l = calcLevel(angle_45[i])
        fig3.add_hline(y=angle_45[i], line_color='blue', line_width=0.75, annotation_text=str(l) + ": 45")
    
for i in range(len(date_angle_45)):
    if date_angle_45[i] < maxDate:
        xx = (date_angle_45[i] - np.datetime64('1970-01-01'))/ np.timedelta64(1, 's')
        fig3.add_vline(x=xx * 1000, line_color='blue', line_width=0.75, annotation_text="45, " + str(date_angle_45[i]))
    

for i in range(len(angle_90)):
    if angle_90[i] < maximum and angle_90[i] > minimum:
        l = calcLevel(angle_90[i])
        fig3.add_hline(y=angle_90[i], line_color='black', line_width=0.75, annotation_text=str(l) + ": 90")

for i in range(len(date_angle_90)):
    if date_angle_90[i] < maxDate:
        xx = (date_angle_90[i] - np.datetime64('1970-01-01'))/ np.timedelta64(1, 's')
        fig3.add_vline(x=xx * 1000, line_color='black', line_width=0.75, annotation_text="90, " + str(date_angle_90[i]))
    

for i in range(len(angle_135)):
    if angle_135[i] < maximum and angle_135[i] > minimum:
        l = calcLevel(angle_135[i])
        fig3.add_hline(y=angle_135[i], line_color='blue', line_width=0.75, annotation_text=str(l) + ": 135")

for i in range(len(date_angle_135)):        
    if date_angle_135[i] < maxDate:
        xx = (date_angle_135[i] - np.datetime64('1970-01-01'))/ np.timedelta64(1, 's')
        fig3.add_vline(x=xx * 1000, line_color='blue', line_width=0.75, annotation_text="135, " + str(date_angle_135[i]))
    

for i in range(len(angle_180)):
    if angle_180[i] < maximum and angle_180[i] > minimum:
        l = calcLevel(angle_180[i])
        fig3.add_hline(y=angle_180[i], line_color='black', line_width=1.5, annotation_text=str(l) + ": 180")

for i in range(len(date_angle_180)):    
    if date_angle_180[i] < maxDate:
        xx = (date_angle_180[i] - np.datetime64('1970-01-01'))/ np.timedelta64(1, 's')
        fig3.add_vline(x=xx * 1000, line_color='black', line_width=1.5, annotation_text="180, " + str(date_angle_180[i]))
    

for i in range(len(angle_225)):
    if angle_225[i] < maximum and angle_225[i] > minimum:
        l = calcLevel(angle_225[i])
        fig3.add_hline(y=angle_225[i], line_color='blue', line_width=0.75, annotation_text=str(l) + ": 225")

for i in range(len(date_angle_225)):        
    if date_angle_225[i] < maxDate:
        xx = (date_angle_225[i] - np.datetime64('1970-01-01'))/ np.timedelta64(1, 's')
        fig3.add_vline(x=xx * 1000, line_color='blue', line_width=0.75, annotation_text="225, " + str(date_angle_225[i]))
    

for i in range(len(angle_270)):
    if angle_270[i] < maximum and angle_270[i] > minimum:
        l = calcLevel(angle_270[i])
        fig3.add_hline(y=angle_270[i], line_color='black', line_width=0.75, annotation_text=str(l) + ": 270")

for i in range(len(date_angle_270)):    
    if date_angle_270[i] < maxDate:
        xx = (date_angle_270[i] - np.datetime64('1970-01-01'))/ np.timedelta64(1, 's')
        fig3.add_vline(x=xx * 1000, line_color='black', line_width=0.75, annotation_text="270, " + str(date_angle_270[i]))
    

for i in range(len(angle_315)):
    if angle_315[i] < maximum and angle_315[i] > minimum:
        l = calcLevel(angle_315[i])
        fig3.add_hline(y=angle_315[i], line_color='blue', line_width=0.75, annotation_text=str(l) + ": 315")

for i in range(len(date_angle_315)):    
    if date_angle_315[i] < maxDate:
        xx = (date_angle_315[i] - np.datetime64('1970-01-01'))/ np.timedelta64(1, 's')
        fig3.add_vline(x=xx * 1000, line_color='blue', line_width=0.75, annotation_text="315, " + str(date_angle_315[i]))

fig3.show(config={'scrollZoom': True, 'displayModeBar': False})
