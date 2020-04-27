import yfinance as yf
import datetime
import matplotlib.pyplot as plt
import mplcursors
from bokeh.embed import components
from bokeh.plotting import figure, output_file, show
from mainapp.models import UserStockDetails
# from datetime import datetime

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
    # print(purchaseDate)
    tem=datetime.datetime.strptime(purchaseDate, '%Y-%m-%d').date()-datetime.timedelta(days=7)
    # print((tem).isoformat()[:10])
    tdf2 = tdata.history(period='1d',start=(tem).isoformat()[:10],end=purchaseDate)
    costprice = tdf2['Close'].iloc[-1]
    currency = tinfo['currency']
    shortName = tinfo['shortName']
    return website,costprice,currency,shortName


def getmystocks(username):
    # for c in UserStockDetails.objects.raw('SELECT * FROM mainapp_userstockdetails where user=%s',[username]):
    #     print(c)
    retlst=[]
    for c in UserStockDetails.objects.all().filter(user=username):
        symb = c.symbol
        tdata = yf.Ticker(symb)
        shortName = c.shortName
        currency = c.currency
        website = c.website
        quantity = c.quantity
        today = datetime.datetime.today().isoformat()
        tdf = tdata.history(period='1d',start=(datetime.date.today()-datetime.timedelta(days=7)).isoformat()[:10],end=today[:10])
        lastprice = tdf['Close'].iloc[-1]
        # tdf2 = tdata.history(period='1d',start=(c.purchaseDate-datetime.timedelta(days=7)).isoformat()[:10],end=c.purchaseDate.isoformat()[:10])
        # costprice = tdf2['Close'].iloc[-1]
        costprice = c.costprice
        profit=round(quantity*(lastprice-costprice),2)
        temp=[shortName,symb,quantity,currency,lastprice,profit,website,c.id]
        retlst.append(temp)
    return retlst

def yfinancesymb(symb):
    today = datetime.datetime.today().isoformat()
    days_before = (datetime.date.today()-datetime.timedelta(days=30)).isoformat()
    tdata = yf.Ticker(symb)
    # print(days_before[:10])
    tdf = tdata.history(period='1d',start=days_before[:10],end=today[:10])
    # print(tdf)
    y1=tdf['Open']
    y2=tdf['Close']
    xt=tdf.index
    ind=range(len(xt))
    x=xt.to_series(ind).apply(lambda x: x.date())
    title=str(symb)+" Stock Rates"
    # x= [1,3,5,7,9,11,13]
    # y1= [1,2,3,4,5,6,7]
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

    # print(y1)
    # print(type(y1))
    # print(x)
    # print(type(x))
    # print(type(x[0]))
    # plt.plot(x,y1, label = "Opening Rate")
    # plt.plot(x, y2, label = "Closing Rate")
    # plt.xticks(rotation=35)
    # plt.legend(loc="upper left")
    # mplcursors.cursor(hover=True)
    script, div = components(plot)
    # plt.show()
    # tinfo = tdata.info
    # print(tinfo['website'])
    # print(tinfo['shortName'])
    # print(tinfo['currency'])
    return script, div

# orders=Order.objects.all().filter(user=re.user)
# for i in orders:
#     print(i.items)
