#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd 


API_KEY     =       "C8V33U8F24NDPC4D"
QUERY_URL   =       "https://www.alphavantage.co/query?function={REQUEST_TYPE}&apikey={KEY}&symbol={SYMBOL}"

daily       =       'TIME_SERIES_DAILY'
weekly      =       'TIME_SERIES_WEEKLY'

order_list  =       []


def pd_request(symbol, req_type, extra):
    
    data = pd.read_csv(QUERY_URL.format(REQUEST_TYPE=req_type, KEY=API_KEY, SYMBOL=symbol) + extra)
    
    return data

def start():

    while 1:
        try:
    
            symbol = input ("\nPlease, input you symbol:    ").upper()
            
            print ("\nSearching ... \n\nPlease wait...")
            
            
            df = pd_request(symbol,daily,'&datatype=csv&outputsize=full')

            df50 = pd_request(symbol,'SMA','&interval=daily&time_period=50&series_type=close&datatype=csv')
            df200 = pd_request(symbol,'SMA','&interval=daily&time_period=200&series_type=close&datatype=csv')
            df21 = pd_request(symbol,'EMA','&interval=daily&time_period=21&series_type=close&datatype=csv')

            
            
            if 'Error Message' in str(df.iloc[0]):
                print('\nWrong Symbol, try again ...')
            else:
            
                print("Data has downloaded!\n")
                break
        
        except:
            print ('\nSomething went wrong, try other symbol, please')
        
        
    return (df, symbol, df21, df50, df200) #таблица котировок, имя символа, таблицы средних по дням 21/50/200
    


def date_query(df):       # запрос начальной даты и вывод нужного диапазона  таблицы котировок
    while 1:
        try:
            first = df.iloc[0]['timestamp']
            last = df.iloc[-1]['timestamp']
            print('\nDownloaded {} data has range between {} and {}'.format(symbol,last,first))
            initial_day = input ('\nPlease, input your starting day (yyyy-mm-dd) \nor just press Enter for using all the data range:    ')
            
            if initial_day == '':
                df_slice = df
                break
            
            line_num = df[df['timestamp'] == initial_day].index.tolist()[0]
            df_slice = df[:line_num+1]
            
            print('\nDate accepted, go on...')
            
            break
        except:
            print('\nSomething went wrong, your date wrong, try again ...')
            
            
    return df_slice  
    


def capital_query():     
    while 1:
        try:
            money = float (input ('\nPlease, input your starting cache balance:    '))
            if money > 0:

                print('\n\n  OK, let\'s start ...\n\n')
                               
                break
            else:
                print ("\nYour cash have to be more zero, try again")
        except:
            print('\nSomething went wrong, you need to Input positive number, try again ...')
    
    
    return money



def quotes_msg(df,symbol,df21,df50,df200):
    
    msg_list =[]
    prev_close = 1
    
    for i in reversed(df.index):
        
        data_line = df.iloc[i]
        # o_pen = data.open
        date = data_line.timestamp
        close = data_line.close
        high = data_line.high
        low = data_line.low
        volume = data_line.volume
        
        
        
        try:
            sma50 = df50.iloc[df50.SMA[df50['time'] == date].index[0]].SMA
        except:
            sma50 = 0
        try:    
            sma200 = df200.iloc[df200.SMA[df200['time'] == date].index[0]].SMA
        except:
            sma200 = 0  
        try:
            ema21 = df21.iloc[df21.EMA[df21['time'] == date].index[0]].EMA
        except:
            ema21 = 0  
            
        s50 = 0 if sma50 == 0 else close-sma50
        s200 = 0 if sma200 == 0 else close-sma200
        e21 = 0 if ema21 == 0 else close-ema21
        
            
        msg = '   {}  {}   {:.2f} ({:.2f} - {:.2f}) / {:.2f}M   \n \t\t  (change: {:.1f}%/{:.2f}  size: {:.0f} range: {:.0f}%  MA: {:.0f}/{:.0f}/{:.0f})'.format(
                date, symbol,close, high, low,volume/1000000, (close/prev_close-1)*100,close-prev_close,round(high-low),round(100*(close-low)/(high-low)),e21,s50,s200)
        
        msg_list.append([msg,(high,low,close)])
        
        prev_close = close
    
    
    return msg_list
            

        
def action_query(m):
    
        
        
        while 1:
            
            action = input ('\n[Buy order-\'b; Sell order-\'s\'; Order actions-\'o\'; To continue press \'Enter\']\n\n')
          
            if action == 'b':
                add_order(order_list,buy_action())
            
            elif action == 's':
                add_order(order_list,sell_action())
            
            elif action == 'o':
                change_action()

                drawline ('.', 80) 

                print('\n', m, '\n')

                drawline ('.', 80)
            
            elif action == '':
                break
            
            else:
                print ('\nInput only showed symbols! Try again...')
                
                
def check_order(price, low, high):
    
    if price >= low and price <= high:
        return True
    else:
        return False

def is_digit(string):
    if string.isdigit():
       return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False

    
def buy_action():

    print(" /// BUY ///\n")
    
    while 1:
        buy_price = input("Price:\t\t")
        if is_digit(buy_price):
            break
        else:
            print ("Only positive digits please, try again")
    
    
    while 1:
        buy_amount = input ("Quantity:\t")
        if buy_amount.isdigit():
            break
        else:
            print ("Only positive digits please, try again")
    
    while 1:
        buy_stop = input ("Stop-price:\t")
        if is_digit(buy_stop):
            break
        else:
            print ("Only positive digits please, try again")
   
    drawline ('=',55)
    print ('Your order accepted: Buy {} {} at {}. Stop-order at {}'.format(int(buy_amount), symbol,float(buy_price),float(buy_stop) ))
    return [float(buy_price), int(buy_amount), float(buy_stop), 'buy']

def sell_action():
    print(" /// SELL ///\n")
    while 1:
        sell_price = input("Price:\t\t")
        if is_digit(sell_price):
            break
        else:
            print ("Only positive number please, try again")
    
    while 1:
        sell_amount = input ("Quantity:\t")
        if sell_amount.isdigit():
            break
        else:
            print ("Only positive number please, try again")
    
    drawline ('=',40)
    print ('Your order accepted: Sell {} {} at {}.'.format(int(sell_amount), symbol,float(sell_price)))
    return [float(sell_price), int(sell_amount), 0, 'sell']

def change_action():
    
    if len(order_list) == 0:
        return print ('\n////  You have no any orders!  ////')
    number_list =[]
    for i in order_list:
        drawline ('-',30)
        print ( '\t[',order_list.index(i)+1,']  ', '   {}  {}  {} at  {}\n'.format((i[3].upper()),int(i[1]),symbol,i[0]))
        
        number_list.append(order_list.index(i)+1)
        
    drawline ('-',30)
    while 1:
        
        answer = input ('Input number of the order you want to change/remove. Press ‘Enter’ to back : ')
        try:
            if answer == '':
                return print(' /// Backing... /// ')
                
            elif int(answer) in number_list:
                change_order_process(order_list, int(answer))
                return print ('Changing complete!')
                
            else:
                print('\nWrong order number, try again')
        except:
            print('\nSomething went wrong, try again')
   
            
        
def change_order_process(order_list, answer):
    
    order = order_list[answer-1]
    while 1:
        action = input ('\nYou chose to change order /// [{}]  {}  {} at {}  ///\n\nWhat do you want to change (\'p\'-price, \'a\'-amount, \'r\'-remove, \'Enter\' for cancel:    '.format(answer,order[3].upper(),order[1],order[0]))
        if action == '':
            return print ('\n')
        
        elif action == 'r':
            order_list.remove(order_list[answer-1])
            print ("\nOrder removed!\n")
            break
        elif action == 'p':
            while 1:
                new_price = float(input ('Input new price:    '))
                
                if new_price > 0:
                    order[0] = new_price
                    print ('\nCheck your new order!  ///  {} {} {} at {}   ///\n\n'.format(order[3],order[1],symbol,order[0]))
                    break
                
                    
                else:
                    print('\nWrong price, try again')
                
            
        elif action == 'a':
            while 1:
                new_amount = int(input ('Input new amount:    '))
                if new_amount > 0:
                    order[1] = new_amount
                    print ('\nCheck your new order!  ///  {} {} {} at {}   ///\n\n'.format(order[3],order[1],symbol,order[0]))
                    break
                
                else:    
                    print('\nWrong amount, try again')
                    
            
        else:
            print ('There is not such action, try again...')

def add_order(list,order):
    
    return list.append(order)

def drawline (char, len):
    s =  '{:' + char + '^' + str(len)  + '}'
    return print (s.format('') )

def check_orders_done (order_list,money,m):

    

    if len(order_list) != 0:
        temp_order_list = []
        order_list_copy=order_list.copy()

        for x in order_list:
            
            i = order_list_copy.pop()  

            if check_order (i[0],m[1][1],m[1][0]): #price low high
                sum = i[0] * i[1]
                
                if i[3] == 'buy':
                    print (i)
                    money = money - sum
                    temp_order_list.append([i[2],i[1],0,'sell'])
                
                    
                    

                    print ("\n   /// Order complete ///. Bought {} {} at {}  ///\n\n".format(i[1],symbol,i[0]))
                    print ("\t\tStop-order activated to sell {} at {}\n\n".format(i[1],i[2]))

                    

                elif i[3] == 'sell':
                    money = money + sum
                    
                    print ("\n   /// Order complete. Sold {} {} at {}  ///\n\n".format(i[1],symbol,i[0]))
                    
            else:
                temp_order_list.append(i)
                
        
        order_list = temp_order_list
    
    return [order_list,money]



      
        
        
# ============= START ================= 

print ('\n'*100)
drawline ('*', 80) 
print ("\n\n\t\tStock Trade Simulator by P.Pavlov 2020\n\n")
drawline ('*', 80) 

symb_data = start() # получение данных о символе

symbol = symb_data[1] # имя символа

data = symb_data[0] # таблица данных котировок

ema21 = symb_data[2] # таблица данных EMA21

sma50 = symb_data[3] # таблица данных SMA50

sma200 = symb_data[4] # таблица данных SMA200

df = date_query(data) # обработанная таблица данных для вывода с нужного дня 

money = capital_query() # начальный баланс средств

msg_lst = quotes_msg(df,symbol, ema21, sma50, sma200) #список "телеграм" (форм. вывод из таблиц данных)

 # основной процесс вывода телеграм построчно и меню с обработкой действий

days = 1

for m in msg_lst:

    check = check_orders_done (order_list,money, m)
    order_list = check[0]
    money = check[1]
    
    drawline ('.', 80) 

    print('\n', m[0], '\n')

    drawline ('.', 80)


    print ('Cache: {}  Orders: {}  Days:  {}'.format(money, len(order_list), days))

    action_query(m[0])

    days = days + 1
