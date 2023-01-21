import MetaTrader5 as mt5
import pandas as pd
import os
from variable import *
from mt5 import *
import MetaTrader5 as mt5
import os
from variable import *
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pytz

def initConection():

    if not load_dotenv():
        print('Não foi possível acessar as variáveis de ambiente')
        quit()

    if account == 'Real':
        initialize =  mt5.initialize(login = int(os.environ['login']),
                                     password = os.environ['password'],
                                     server = os.environ['server'])
    else:
        initialize =  mt5.initialize(login = int(os.environ['loginDemo']),
                                     password = os.environ['passwordDemo'],
                                     server = os.environ['serverDemo'])       

    if not initialize:
        print("initialize() failed, error code =",mt5.last_error())
        quit()

    else:
        print("MetaTrader5 package version: ",mt5.__version__)

    symbol_info = mt5.symbol_info(symbol)

    if symbol_info is None:
        print(symbol, "not found, can not call order_check()")
        mt5.shutdown()
        quit()
        
    if not symbol_info.visible:
        print(symbol, "is not visible, trying to switch on")
        
        if not mt5.symbol_select(symbol, True):
            print("symbol_select({}}) failed, exit", symbol)
            mt5.shutdown()
            quit()
   
def printInfo():
    account_info = mt5.account_info()
    terminal_info = mt5.terminal_info()
    positions = mt5.positions_get(symbol = symbol)

    try:
        deals = mt5.history_deals_get(datetime.now(pytz.timezone('Etc/GMT-3')) - timedelta(days = 1), datetime.now(pytz.timezone('Etc/GMT-3')))
        df = pd.DataFrame(list(deals),columns=deals[0]._asdict().keys())
        dfProfit = df[df['profit']>0]['profit']
        dfLoss = df[df['profit']<0]['profit']
        profit = dfProfit.sum()
        loss = dfLoss.sum()
        total24h = profit + loss

        deals = mt5.history_deals_get(startDate, datetime.now(pytz.timezone('Etc/GMT-3')))
        df = pd.DataFrame(list(deals),columns=deals[0]._asdict().keys())
        dfProfit = df[df['profit']>0]['profit']
        dfLoss = df[df['profit']<0]['profit']
        lenOperation = len(dfProfit) + len(dfLoss)
        profit = dfProfit.sum()
        loss = dfLoss.sum()
        total = profit + loss

    except:
        return 0

    print('\n\n========================================================')
    print("Company: {}\nServer: {}\nAccount: {}\nOwner: {}\nInitial Date: {}\nCurrency: {}\nBalance: {} \
          \n\nProfit: {:.2f}\nLoss: {:.2f}\nTotal: {:.2f}\nTotal last 24h: {:.2f}\n\nProfit operation: {}\nLoss operation: {} \
          \nNumber of operations: {}\n\nOpen position(s): {}" \
          .format(account_info.company,
                  account_info.server,
                  account_info.login,
                  account_info.name,
                  startDate.strftime('%d-%m-%Y'),
                  account_info.currency,
                  account_info.balance,
                  profit,
                  loss,
                  total,
                  total24h,
                  len(dfProfit),
                  len(dfLoss),
                  lenOperation,
                  len(positions),
                  ))
    print('========================================================')

    print('========================================================')
    print("Connected: {}\nAlgoTrade Allowed: {}\nAPI Python Enabled: {}" \
          .format(terminal_info.connected,
                  terminal_info.trade_allowed,
                  not terminal_info.tradeapi_disabled
                  ))
    print('========================================================')

    return lenOperation

def trader(action, symbol, lot, delta): 
    positions = mt5.positions_get(symbol = symbol)
    if len(positions) != 0:
        print("There is already an open operation\n\n")
        return
    
    point = mt5.symbol_info(symbol).point
    if action == mt5.ORDER_TYPE_BUY:
        price = mt5.symbol_info_tick(symbol).ask
        
    else:
        price = mt5.symbol_info_tick(symbol).bid

    request={
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": action,
        "price": price,
        "tp": round(price + tpDelta * (delta * 10**5) * point, 5),
        "sl": round(price - slDelta * (delta * 10**5) * point, 5),
        "deviation": deviation,
        "magic": 234000,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    
    result = mt5.order_send(request)
    print("1. order_send(): by {} {} lots at {} with deviation={} points\n\n".format(symbol,lot,price,deviation))

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. order_send failed, retcode={}\n\n".format(result.retcode))
        result_dict=result._asdict()
        for field in result_dict.keys():
            print("   {}={}".format(field,result_dict[field]))
            if field == "request":
                traderequest_dict = result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
                    print("       traderequest: {}={}\n\n".format(tradereq_filed,traderequest_dict[tradereq_filed]))
        mt5.shutdown()
        quit()

    print("Order_send done {}\n\n".format(result))
    print("\nOpened position with POSITION_TICKET = {}\n\n".format(result.order))       
    return
    
    result = mt5.order_send(request)
    print("1. order_send(): by {} {} lots at {} with deviation={} points\n".format(symbol,lot,price,deviation))

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. order_send failed, retcode={}".format(result.retcode))
        result_dict=result._asdict()
        for field in result_dict.keys():
            print("   {}={}".format(field,result_dict[field]))
            if field == "request":
                traderequest_dict = result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
                    print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))

        mt5.shutdown()
        quit()

    print("Order_send done, ", result)
    print("\nOpened position with POSITION_TICKET = {}\n\n".format(result.order))
              
def closeAllTrader(symbol): 
    positions = mt5.positions_get(symbol = symbol)
    if positions == None:
        print("No positions on {}, error code={}\n\n".format(symbol, mt5.last_error()))
        
    elif len(positions) > 0:
        print("Total positions on {}: {}\n\n".format(symbol, len(positions)))

    for position in positions:
        position_id = position.ticket
        
        if position.type == mt5.ORDER_TYPE_SELL:            
            typeOrder = mt5.ORDER_TYPE_BUY
            price = mt5.symbol_info_tick(symbol).ask
        
        else:        
            typeOrder = mt5.ORDER_TYPE_SELL
            price = mt5.symbol_info_tick(symbol).bid
    
        request={
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": position.symbol,
            "volume": position.volume,
            "type": typeOrder,
            "position": position_id,
            "price": price,
            "deviation": deviation,
            "magic": 234000,
            "comment": "python script close",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)
        print("Close position #{}: sell {} {} lots at {} with deviation={} points\n\n" \
              .format(position_id,symbol,lot,price,deviation))
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("Order_send failed, retcode = {}\n\n".format(result.retcode))
            print("   result", result)
            
        else:
            print("Position #{} closed, {}\n\n".format(position_id, result))
            
    return

def changeOrder(symbol, tp = None, sl = None, verbose = True):

    positions = mt5.positions_get(symbol = symbol)
    if len(positions) == 0:
        # print("No positions on {}\n\n".format(symbol))
        return
              
    if len(positions) > 1:
        # print("To many positions on {}\n\n".format(symbol))
        return
        
    position = positions[0]
    position_id = position.ticket
    
    if tp == None:
        tp = position.tp
        
    if sl == None:
        sl = position.sl
    
    request={
            "action": mt5.TRADE_ACTION_SLTP,
            "symbol": position.symbol,
            "volume": position.volume,
            "type": position.type,
            "position": position_id,
            "price_open": position.price_open,
            "sl": sl,
            "tp": tp,
            "magic": 234000,
            "comment": "python change stop's",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC
    }

    result = mt5.order_send(request)
    if verbose:
        print("Send order to change stop level at #{}: {}\n\n".format(position_id, symbol))
            
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("Order_send failed, retcode = {}\n\n".format(result.retcode))
            print("   result", result)
                
        else:
            print("Position #{} modified, {}\n\n".format(position_id, result))

def updateSL():
    positions = mt5.positions_get(symbol = symbol)
    if len(positions) == 1:
        position = positions[0]
        delta = position.tp - position.price_open
        newSL = 2 * position.price_open - position.tp + trailStopSpeed * (position.price_current - position.price_open)

        if (delta > 0) & (newSL > position.sl) & (newSL < position.price_open + fee):
            changeOrder(symbol, sl = newSL, verbose = False)

        elif (delta < 0) & (newSL < position.sl) & (newSL > position.price_open - fee):
            changeOrder(symbol, sl = newSL, verbose = False)