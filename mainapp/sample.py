import yfinance as yf
import datetime
import matplotlib.pyplot as plt
import mplcursors
from bokeh.embed import components
from bokeh.plotting import figure, output_file, show
from mainapp.models import UserStockDetails

def test(symb):
    try:
        tdata = yf.Ticker(symb)
        tinfo = tdata.info
        return True
    except:
        return False

def getstockdetails(symb,purchaseDate):
    tdata = yf.Ticker(symb)
    tinfo = tdata.info
    try:
        website=tinfo['website']
    except:
        website=None
    tem=datetime.datetime.strptime(purchaseDate, '%Y-%m-%d').date()-datetime.timedelta(days=7)
    tdf2 = tdata.history(period='1d',start=(tem).isoformat()[:10],end=purchaseDate)
    costprice = tdf2['Close'].iloc[-1]
    currency = tinfo['currency']
    shortName = tinfo['shortName']
    return website,costprice,currency,shortName


def getmystocks(username):
    retlst=[]
    for c in UserStockDetails.objects.all().filter(user=username):
        symb = c.symbol
        tdata = yf.Ticker(symb)
        shortName = c.shortName
        currency = c.currency
        website = c.website
        quantity = c.quantity
        today = datetime.datetime.today().isoformat()
        tdf = tdata.history(period='1d',start=\
        (datetime.date.today()-datetime.timedelta(days=7)).isoformat()[:10],end=today[:10])
        lastprice = tdf['Close'].iloc[-1]
        costprice = c.costprice
        profit=round(quantity*(lastprice-costprice),2)
        temp=[shortName,symb,quantity,currency,lastprice,profit,website,c.id]
        retlst.append(temp)
    return retlst

def yfinancesymb(symb):
    today = datetime.datetime.today().isoformat()
    days_before = (datetime.date.today()-datetime.timedelta(days=30)).isoformat()
    tdata = yf.Ticker(symb)
    tdf = tdata.history(period='1d',start=days_before[:10],end=today[:10])
    y1=tdf['Open']
    y2=tdf['Close']
    xt=tdf.index
    ind=range(len(xt))
    x=xt.to_series(ind).apply(lambda x: x.date())
    title=str(symb)+" Stock Rates"
    tinfo = tdata.info
    ylabel='Price in '+str(tinfo['currency'])
    plot = figure(title= title ,
        x_axis_label= 'Time',
        y_axis_label= ylabel,
        x_axis_type='datetime',
        plot_width =1200,
        plot_height =400)

    plot.line(x, y1, legend_label= 'Opening Rate', line_width = 2, color="red")
    plot.line(x, y2, legend_label= 'Closeing Rate', line_width = 2, color="blue")
    script, div = components(plot)
    return script, div
