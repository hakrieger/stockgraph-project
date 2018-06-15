from flask import Flask, render_template, request, redirect
import quandl as q
import pandas as pd
from bokeh.models.widgets import TextInput #Select
from bokeh.plotting import figure, show #, output_file
from bokeh.models import Band, ColumnDataSource, Range1d, Title
from bokeh.embed import components

from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
#setting api key to access data from quandl
q.ApiConfig.api_key = "WTAu2SBBZyADGzrpPL-c"

#def get_stock_data(ti):
    #data = q.get_table('WIKI/PRICES', paginate=True,
    #               ticker = ti, date = { 'gte': '2018-01-01', 'lte': '2018-04-01' },
    #               qopts={"columns":["ticker", "date", "close", "low", "high"]})
    #return data

def create_stock_plot(ti):
    #getting stock data from ticker input
    data = q.get_table('WIKI/PRICES', paginate=True,
                   ticker = ti, date = { 'gte': '2018-01-01', 'lte': '2018-04-01' },
                   qopts={"columns":["ticker", "date", "close", "low", "high"]})
    #creating dictionary database to plot
    df = pd.DataFrame(data=dict(x=data.date, y=data.close, low=data.low, high=data.high)).sort_values(by="x")
    source = ColumnDataSource(df.reset_index())

    t1 = "Closing Cost with High/Low Reach Band"
    t2 = "From %s to %s" %('Jan 2018', 'Apr 2018')
    #creating figure
    p = figure(title = t1, plot_width=700, plot_height=500, x_axis_type="datetime")
    p.y_range = Range1d(data.low[data.low.idxmin()]-2, data.high[data.high.idxmax()]+2)
    p.xaxis.axis_label = 'Days'
    p.yaxis.axis_label = 'Value in USD'

    p.line('x', 'y', color = 'firebrick', source = source, line_width=2)

    band = Band(base = 'x', lower='low', upper='high', level='underlay', source = source,
                fill_alpha=0.5, line_width=1, line_color='black', fill_color = 'grey')

    p.add_layout(band)
    p.add_layout(Title(text=t2, align="center"), "below")

    return p

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index1.html')

@app.route('/graph', methods=['POST'])
def graph():
    text = request.form.get('stock-ticker')
    ti = text.upper()

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    plot = create_stock_plot(ti)
    script, div = components(plot)

    html = render_template('graph4.html', stock_ticker=ti, plot_script=script, plot_div=div,
        js_resources=js_resources, css_resources=css_resources)

    if ti:
        return encode_utf8(html)
        #return render_template('graph3.html', stock_ticker=ti, script=script, div=div)
    else:
        return 'Please enter a valid stock ticker', 400

if __name__ == '__main__':
  app.run(debug = True) #port=33507
