#MSDS Spring 2018 
#DATA 602 Advanced Programming Techniques
#Assignment 2 Crypto Trading System
#Jiadi li

import datetime as dt #for date and time data type manipulation
import numpy as np #for scientific computing methods
import pandas as pd #for dataframe structure and relevant manipulation
import pymongo as pm #for MongoDB database connection
import json #for writing dataframe to MongoDB
import requests as rq #for using .json function to use .get() directly
import matplotlib.pyplot as plt #for plotting analytical graphs
import tabulate as tb #for printing dataframe in a pretty and neat way

def read_df_from_Mongo(dbName,collectionName):
    client = pm.MongoClient() #connecting with MongoDB
    db = client[dbName] #getting a database
    collection = db[collectionName].find({},{'_id':False}) #getting a collection, which is similar to a table in SQL Database
    df = pd.DataFrame(list(collection)) #Converting the connection to a dataframe
    return df

def write_df_to_Mongo(dbName,collectionName,dfName):
    client = pm.MongoClient() #connecting with MongoDB
    db = client[dbName] #getting a database
    result = db[collectionName].delete_many({}) #deleting all records in selected collection
    result.deleted_count
    db[collectionName].insert_many(json.loads(dfName.T.to_json()).values()) #converting dataframe into JSON format and insert to MongoDB

#import data from MongoDB to blotter dataframe or initialize the dataframe if no data is available
def get_blotter_df():    
    blotter = read_df_from_Mongo("602A2","blotter")
    if blotter.empty:
        blotter = pd.DataFrame({'side':["Initial status"],'ticker':["None"],'quantity':[0],'executed price':[0],'execution timestamp':["1990-01-01 01:00:00"],'money in/out':[0],'cash':[100000000]})
    return blotter

##import data from MongoDB to p/l dataframe or initialize the dataframe if no data is available
def get_pl_df():    
    pl = read_df_from_Mongo("602A2","P/L")
    if pl.empty:
        pl = pd.DataFrame({'ticker':[],'position':[],'current market price':[],'vmap':[],'unrealized p/l':[],'realized p/l':[],'total p/l':[],'allocation by shares':[],'allocation by dollars':[]})
    return pl

#display a chart showing the price of last 100 days
def display_price_days_chart(ticker,length):
    #storing prices data for given ticker into a dataframe
    print("Please find the summary of price of " + ticker + " for last " + str(length) + " days: \n")
    candle_url = 'https://api.gdax.com/products/' + ticker + '-USD/candles'
    date_end = dt.datetime.today().isoformat()
    date_start = (dt.datetime.today() - dt.timedelta(days = length+1)).isoformat()
    df = pd.DataFrame(rq.get(candle_url,{'start':date_start,'end':date_end,'granularity':86400}).json(),columns=['time','low', 'high', 'open', 'close', 'volume'])
    df['time'] = pd.Series([dt.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d') for timestamp in df['time']])
    #printing description of close price data and plotting a graph
    print(round(df['close'].describe(),2))
    plt.figure(figsize=(10,8))
    plt.plot(df[['close']])
    plt.xlabel('Latest <————————(days)————————> Earliest')
    plt.ylabel('price')
    title = "Price of "+ticker+" over past "+str(length)+" days"
    plt.title(title)
    plt.show()
    
#display basic analytics and visualization for the user to make wise decision
def display_analytics_hours(ticker,length):
    print("Please find some basic analytics of " + ticker + " for last " + str(length) + " hours: ")
    #storing price data for given ticker into a dataframe
    candle_url = 'https://api.gdax.com/products/' + ticker + '-USD/candles'
    date_end = dt.datetime.now().isoformat()
    date_start = (dt.datetime.now() - dt.timedelta(hours = length+1)).isoformat()
    df = pd.DataFrame(rq.get(candle_url,{'start':date_start,'end':date_end,'granularity':3600}).json(),columns=['time','low', 'high', 'open', 'close', 'volume'])
    df['time'] = pd.Series([dt.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M') for timestamp in df['time']])
    #printing basic analytics data and plotting graghs 
    print("\nAverage (close) price: " + str(round(df['close'].mean(),2)))
    print("Minimum price： " +str(min(df['close'])) + "\nMaximum price: " +str(max(df['close'])) + "\nStandard Deviation: " + str(round(df['close'].std(),2)) + "\n")
    plt.figure(figsize=(10,8))
    plt.plot(df[['close']])
    plt.xlabel('Latest <————————(hours)————————> Earliest')
    plt.ylabel('price')
    title = "Price of "+ticker+" over past "+str(length)+" hours"
    plt.title(title)
    plt.show()  

#plotting 20 days moving average graph
def moving_average_graph(ticker,length,period):
    print("Please find the " + str(period) + " days moving average graph for " + ticker + ": ")
    #storing price data for given ticker into a dataframe
    candle_url = 'https://api.gdax.com/products/' + ticker + '-USD/candles'
    date_end = dt.datetime.now().isoformat()
    date_start = (dt.datetime.now() - dt.timedelta(days = length+1)).isoformat()
    df = pd.DataFrame(rq.get(candle_url,{'start':date_start,'end':date_end,'granularity':86400}).json(),columns=['time','low', 'high', 'open', 'close', 'volume'])
    df['time'] = pd.Series([dt.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d') for timestamp in df['time']])
    #Plot the original close price and the newly created 20 day moving average price
    df['moving average'] = df['close'].rolling(period,center=True).mean()
    plt.figure(figsize=(10,8))
    plt.grid(True)
    plt.plot(df['close'],label=ticker)
    plt.plot(df['moving average'],label=('Moving Average '+str(period)+' day'))
    plt.legend()
    plt.show()  

def rolling_historical_volatility_graph(ticker,length,period):
    print("Please find the rolling historical volatility graph for " + ticker + ": ")
    #storing price data for given ticker into a dataframe
    candle_url = 'https://api.gdax.com/products/' + ticker + '-USD/candles'
    date_end = dt.datetime.now().isoformat()
    date_start = (dt.datetime.now() - dt.timedelta(days = length+1)).isoformat()
    df = pd.DataFrame(rq.get(candle_url,{'start':date_start,'end':date_end,'granularity':86400}).json(),columns=['time','low', 'high', 'open', 'close', 'volume'])
    df['time'] = pd.Series([dt.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d') for timestamp in df['time']])
    #Plotting the rolling historical volatility data
    df['change'] = np.log(df['close']/df['close'].shift())
    df['volatility'] = df['change'].rolling(period).std().shift()
    plt.figure(figsize=(10,8))
    plt.grid(True)
    plt.plot(df['volatility'],label=('volatility'))
    plt.legend()
    plt.show() 
    
#updating pl dataframe with blotter dataframe    
def refresh_pl(blotter): 
    ticker_list = blotter['ticker'].unique()
    ticker_list = np.delete(ticker_list,np.argwhere(ticker_list=="None")) #remove the element which represents initial status
    #creating empty lists to be appended later
    position_list = []
    current_price_list = []
    vwap_list = []
    upl_list = []
    rpl_list = []
    total_pl_list = []
    allocation_share_list = []
    allocation_dollar_list = []
    #storing relevant data to each list
    for ticker in ticker_list:
        #storing information for current_price_list
        price_url = 'https://api.gdax.com/products/' + ticker + '-USD/ticker'
        current_price = float(rq.get(price_url).json()['price']) 
        current_price_list.append(current_price)
        #subsetting a dataframe for each traded crypto currency
        blotter_ticker = blotter[blotter['ticker'] == ticker]
        rpl = blotter_ticker['money in/out'].sum()
        rpl_list.append(rpl)
        position = 'long' if rpl > 0 else 'short'
        position_list.append(position)
        quantity = blotter_ticker['quantity'].sum()
        vwap = rpl/quantity
        vwap_list.append(vwap)
        allocation_share = quantity/blotter['quantity'].sum()
        allocation_share_list.append(allocation_share)
        allocation_dollar = rpl/blotter['money in/out'].sum()
        allocation_dollar_list.append(allocation_dollar)  
        upl = current_price * quantity + rpl
        upl_list.append(upl)
        total_pl_list.append(rpl+upl)
        
    pl = pd.DataFrame({'ticker':ticker_list,'position':position_list,'current market price':current_price_list,'VWAP':vwap_list,'unrealized p/l':upl_list,'realized p/l':rpl,'total p/l':total_pl_list,'allocation by shares':allocation_share_list,'allocation by dollars':allocation_dollar_list})
    return pl
    
# functions for program execution
def trade(): 
    #asking for ticker of the cryptocurrency and check if the data is available or valid 
    stored = 0
    while not stored:
        ticker = input("Please enter the ticker of your selected crypto currency: ").upper()
        price_url = 'https://api.gdax.com/products/' + ticker + '-USD/ticker' #the base currency for our system is set to be USD
        try:
            exe_price = float(rq.get(price_url).json()['price']) 
            stored = 1
        except:
            error_message = rq.get(price_url).json()['message'] 
            print("Error Message: " + error_message + ". \nThis crypto currency might not be traded on GDAX platform. Please try again.")
    #displaying prices for the past 100 days of this crypto currency    
    display_price_days_chart(ticker,100)
    display_analytics_hours(ticker,24)
    moving_average_graph(ticker,250,20)
    rolling_historical_volatility_graph(ticker,250,20)
    #asking for the volume to trade
    quant = float(input("Please enter the quantity of this trade (enter 0 to cancell): "))
    #calculating other data based on given information
    if quant != 0:
        sd = "buy" if quant > 0 else "sell"     
        timestamp = dt.datetime.now()
        moneyinout = -exe_price * quant
        blotter = get_blotter_df() #get blotter dataframe from MongoDB
        currentcash = blotter['cash'].iloc[-1] + moneyinout
        print("Trade executed.\nTicker: " + ticker + "\nquantity: " + str(quant) + "\ncurrent remaining cash: " + str('${:,.2f}'.format(currentcash)))
        temp = pd.DataFrame({'side':[sd],'ticker':[ticker],'quantity':[quant],'executed price':[round(exe_price,2)],'execution timestamp':[str(timestamp)],'money in/out':[round(moneyinout,2)],'cash':[round(currentcash,2)]})
        blotter = pd.concat([blotter,temp]) #appending new trading data to the blotter dataframe
        blotter = blotter.set_index(pd.Index(range(len(blotter)))) 
        write_df_to_Mongo("602A2","blotter",blotter) #resaving the new dataframe to MongoDB
    else:
        print("Trade cancelled.\n")

def blotter():
    blotter = get_blotter_df()
    print(tb.tabulate(blotter,headers=blotter.head(),tablefmt='grid'))
    
def pl():
    blotter = get_blotter_df()
    pl = refresh_pl(blotter)
    pl = pl.set_index(pd.Index(range(len(pl)))) 
    write_df_to_Mongo("602A2","p/l",pl) #resaving the new dataframe to MongoDB
    print(tb.tabulate(pl,headers=pl.head(),tablefmt='grid'))
    
#program execution
print("-----Welcome to GDAX Supported Virtual Crypto Trading System-----\n")
continuing = 1
    
while(continuing): #menu repetition
    print("Please enter 1-4 to choose from the following options:")
    choice = int(input("1-Trade\n2-Show Blotter\n3-Show P/L\n4-Quit"))

    if(choice == 1):
        print("\n---Trade---")
        trade()
    
    elif(choice == 2):
        print("\n---Blotter---")
        blotter()
        
        
    elif(choice == 3):
        print("\n---P\L---")
        pl()
        
    elif(choice == 4):
        print("\nThank you for using the Equity Trading System!\nHave a nice day!")
        continuing = 0
