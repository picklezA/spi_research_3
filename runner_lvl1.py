# version: 3.7.9
# author: picklez

import os
from helper_lvl1 import *
from tqdm import tqdm
import time
import threading
import multiprocessing

source_folder = cwd + "\\sources\\"
stocks_folder = source_folder + "\\stock_data\\"
stock_div_folder = source_folder + "\\stock_data_d\\"
default_extension = ".csv"
dividend_extension = "_dividend.csv"
lvl1_output = "\\lvl1_produced\\"

config_settings = read_config()
defined_beginning = config_settings[0]
defined_ending = config_settings[1]
buy_amount = config_settings[2]

timelist = read_timelist(defined_beginning, defined_ending)
second_timelist = timelist.copy()

data_file_table = get_exist_table()

def task_to_do(line):
    pbar = tqdm(total=len(second_timelist), position=1)
    name_pass = stocks_folder + str(line[0]) + default_extension
    stock_data = get_file(name_pass, defined_beginning, defined_ending)
    div_data = {}
    div_name_pass = stock_div_folder + str(line[0]) + dividend_extension
    if line[1] == True:
        div_data = get_file_div(div_name_pass)
    
    hold_array = []
    
    position = 0
    while position < len(second_timelist):
        growth_array = iterate_through_5(second_timelist[position:], stock_data, div_data, buy_amount)
        string_hold = ""
        ga_hold = str(growth_array)[1:-1] # remove the [] from the string
        string_hold = string_hold + ga_hold
        hold_array.append(string_hold)
        pbar.update()
        pbar.refresh()
        position += 1
    
    write_to(source_folder+lvl1_output+line[0]+".csv", hold_array)
    pbar.refresh()
    pbar.close()
    return

def substepping_threads(list):
    for line in list:
        threading.Thread(target=task_to_do, args=(line,)).start()

if __name__ == '__main__':
    starttime = time.time()
    
    sl1 = data_file_table[:5]
    sl2 = data_file_table[5:10]
    sl3 = data_file_table[10:15]
    sl4 = data_file_table[15:20]
    sl5 = data_file_table[20:25]
    sl6 = data_file_table[25:30]
    sl7 = data_file_table[30:35]
    sl8 = data_file_table[35:40]
    
    proc1 = multiprocessing.Process(target=substepping_threads, args=(sl1,))
    proc2 = multiprocessing.Process(target=substepping_threads, args=(sl2,))
    proc3 = multiprocessing.Process(target=substepping_threads, args=(sl3,))
    proc4 = multiprocessing.Process(target=substepping_threads, args=(sl4,))
    proc5 = multiprocessing.Process(target=substepping_threads, args=(sl5,))
    proc6 = multiprocessing.Process(target=substepping_threads, args=(sl6,))
    proc7 = multiprocessing.Process(target=substepping_threads, args=(sl7,))
    proc8 = multiprocessing.Process(target=substepping_threads, args=(sl8,))

    proc1.start()
    proc2.start()
    proc3.start()
    proc4.start()
    proc5.start()
    proc6.start()
    proc7.start()
    proc8.start()

    proc1.join()
    proc2.join()
    proc3.join()
    proc4.join()
    proc5.join()
    proc6.join()
    proc7.join()
    proc8.join()
    
    os.system("cls")
    print("Level_1 took {}s to complete.".format(round(time.time()-starttime, 2)))
    
    import runner_lvl2