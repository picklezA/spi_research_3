# version: 2.4.9
# author: picklez

""" shoutout to my friend Brady for looking at my code and going "you need to
use a dictionary, not an array for this", this man saved me and exponential
amount of time oh my goodness. We went from 37 hour run time to less than
3 minutes."""

import os
cwd = os.getcwd()
source_folder = cwd + "\\sources\\"
stocks_folder = source_folder + "\\stock_data\\"
stock_div_folder = source_folder + "\\stock_data_d\\"

def write_to(fn, array_to_write):
    file_writer = open(fn, "w")
    file_writer.write(A_1D_to_CSV(array_to_write))
    file_writer.close()
    
def A_1D_to_CSV(a):
    ash = str(a)
    ash = ash.replace("[","")
    ash = ash.replace("]","")
    ash = ash.replace("', '","\n")
    ash = ash.replace("'","")
    return ash

def read_config():
    r_config = open("config.txt","r")
    config_ls = r_config.read().split("\n")
    r_config.close()
    return config_ls

def trimlist(file_contents, begin, end):
    while file_contents[0][0] != begin or file_contents[len(file_contents)-1][0] != end:
        if file_contents[0][0] != begin:
            file_contents.pop(0)
        if file_contents[len(file_contents)-1][0] != end:
            file_contents.pop(len(file_contents)-1)
    return file_contents

def read_timelist(begin, end):
    file_read_hold = open("tl.csv", "r")
    hold = file_read_hold.read().split("\n")
    file_read_hold.close()
    file_contents = []
    for line in hold:
        line_hold = line.split(",")
        file_contents.append(line_hold)
    trimmed = trimlist(file_contents, begin, end)
    return trimmed

def averaged_p(o, l, h, c):
    return round((o+l+h+c)/4, 2)
    
def averaged_s(o, l, h, c):
    return round((o+l+h+c)/4, 8)
    
def share_value(shares, stock_price):
    return round((shares * stock_price), 2)
    
def shares_bought(stock_price, buying_amount):
    return round((buying_amount / stock_price), 8)

def percentage_growth(shares, stock_price, invested_amount):
    if invested_amount == 0:
        return 0
    return round(((share_value(shares, stock_price) / invested_amount)-1), 4)
    
def get_file(file_name, begin, end):
    file_read = open(file_name, "r")
    hold = file_read.read().split("\n")
    file_read.close()
    file_contents = {}
    for line in hold:
        line_hold = line.split(",")
        # Dummy None first element to fix indexing in other parts of the code
        file_contents[line_hold[0]] = [None] + line_hold[1:]
    return file_formatter(file_contents)
    
def file_formatter(file_contents):
    for key, value in file_contents.items():
        value[1] = round(float(value[1]), 2)
        value[2] = round(float(value[2]), 2)
        value[3] = round(float(value[3]), 2)
        value[4] = round(float(value[4]), 2)
        value.pop(6)
        value.pop(5)
    return file_contents
    
def get_stocks_file_list():
    return os.listdir(stocks_folder)

def get_stocks_div_file_list():
    return os.listdir(stock_div_folder)
    
def get_exist_table():
    stocks_exists = get_stocks_file_list()
    div_exists = get_stocks_div_file_list()
    ms_hold = []
    for item in stocks_exists:
        hold = []
        name_str = item.replace(".csv","")
        hold.append(name_str)
        holder = False
        for x in div_exists:
            x_str = x.replace("_dividend.csv","")
            if x_str == name_str:
                holder = True
        if holder != True:
            holder = False
        hold.append(holder)
        ms_hold.append(hold)
    return ms_hold
    
def get_file_div(file_name):
    file_read = open(file_name, "r")
    hold = file_read.read().split("\n")
    file_read.close()
    file_contents = {}
    for line in hold:
        line_hold = line.split(",")
        # Dummy None first element to fix indexing in other parts of the code
        file_contents[line_hold[0]] = [None] + line_hold[1:]
    return file_contents
    
def iterate_through_5(timelist, stock_data, div_data, buy_amount):
    return [iterate_through(timelist, stock_data, div_data, buy_amount, x) for x in range(5)]
    
def iterate_through(timelist, stock_data, div_data, buy_amount, buy_day):
    buying_amount = float(buy_amount)
    running_ia = 0
    running_shares = 0
    last_line = stock_data[timelist[-1][0]] # technically the end can not exist, but we are assuming it will exist cause we are giving it only input that exists
    
    for line in timelist:
        current_day = line[0]
        day_passed_delta = float(line[1])
        DOW = line[2]
        stock_line = stock_data.get(current_day, None)
        
        if stock_line:
            if int(DOW) - int(day_passed_delta) == buy_day and int(day_passed_delta) != 0:
                avg_shares_div = averaged_s(shares_bought(stock_line[1], (float(buying_amount)*float(day_passed_delta))), shares_bought(stock_line[2], (float(buying_amount)*float(day_passed_delta))), shares_bought(stock_line[3], (float(buying_amount)*float(day_passed_delta))), shares_bought(stock_line[4], (float(buying_amount)*float(day_passed_delta))),)
                running_shares = round(avg_shares_div + running_shares, 8)
        
        if buy_day != int(DOW):
            continue
        
        div_amount = 0
        if div_data != False:
            div_line = div_data.get(current_day, None)
            if div_line:
                div_amount = float(div_line[1])
        
        if stock_line:
            avg_shares = averaged_s(shares_bought(stock_line[1], buying_amount), shares_bought(stock_line[2], buying_amount), shares_bought(stock_line[3], buying_amount), shares_bought(stock_line[4], buying_amount))
            avg_price = averaged_p(stock_line[1], stock_line[2], stock_line[3], stock_line[4])
            
            div_shares = averaged_s(shares_bought(stock_line[1], div_amount), shares_bought(stock_line[2], div_amount), shares_bought(stock_line[3], div_amount), shares_bought(stock_line[4], div_amount))
            
            running_shares = round(running_shares + avg_shares + div_shares, 8)
            running_ia = running_ia + 1
        else:
            continue
            
    last_avg_price = averaged_p(last_line[1], last_line[2], last_line[3], last_line[4])
    accumulated_growth = percentage_growth(running_shares, last_avg_price, running_ia)
    return accumulated_growth