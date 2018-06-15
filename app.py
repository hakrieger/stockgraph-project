#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 11:53:46 2018

@author: hk
"""
#import os
#os.chdir('/Users/hk/hkhub/TDI-Flask-Demo')


#import requests as req
#import simplejson as json

#import numpy as np
#from datetime import  datetime, timedelta
from flask import Flask, render_template, request
import quandl as q
import pandas as pd
from bokeh.models.widgets import TextInput #Select
from bokeh.plotting import figure #, output_file, show
from bokeh.models import Band, ColumnDataSource, Range1d, Title
#from bokeh.layouts import widgetbox

app = Flask(__name__)

#Creating selection dropdowns
ti = TextInput(title="Stock Ticker:")

#setting api key to access data from quandl
q.ApiConfig.api_key = "WTAu2SBBZyADGzrpPL-c"


#Getting data from inputs
def get_stock_data(ti):
    data = q.get_table('WIKI/PRICES', paginate=True,
                   ticker = 'AA', date = { 'gte': '2018-01-01', 'lte': '2018-04-01' },
                   qopts={"columns":["ticker", "date", "close", "low", "high"]})
    return data


#Graph of: Closing cost with high/low band
def create_stock_plot(ti, data):
    #creating dictionary database to plot
    df = pd.DataFrame(data=dict(x=data.date, y=data.close, low=data.low, high=data.high)).sort_values(by="x")

    #output_file("highlowclose.html")

    #TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
    source = ColumnDataSource(df.reset_index())

    t1 = "Closing Cost with High/Low Reach Band for Stock: '%s'" %(ti)
    t2 = "From %s to %s" %('Jan 2018', 'Apr 2018')

    #figure configuration
    p = figure(title = t1, plot_width=500, plot_height=500,
               x_axis_type="datetime")
    p.y_range = Range1d(
            data.low[data.low.idxmin()]-2, data.high[data.high.idxmax()]+2)
    p.xaxis.axis_label = 'Days'
    p.yaxis.axis_label = 'Value in USD'

    p.line('x', 'y', color = 'firebrick', source = source, line_width=2)

    band = Band(base = 'x', lower='low', upper='high', level='underlay', source = source,
                fill_alpha=0.5, line_width=1, line_color='black', fill_color = 'grey')

    p.add_layout(band)
    p.add_layout(Title(text=t2, align="center"), "below")

    return p

#Index page
@app.rout('/')
def index():
    #Gettting the selected inputs
    ti = request.args.get("stock_ticker")
    if ti == None:
        ti = 'A'

    #Pulling data:
    data = get_stock_data(ti)

    #Plotting data:
    plot = create_stock_plot(ti, data)

    #Embed plot into html vis Flask Render
    script, div = components(plot)
    return render_template('test.html', script=script, div=div,
		ti=stock_ticker)


# With debug=True, Flask server will auto-reload when there are code changes
if __name__ == '__main__':
	app.run(port=33507, debug=True)


#inputs = widgetbox(ti)

