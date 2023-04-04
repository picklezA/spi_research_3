# version: 1.5.9
# author: picklez

print("Level_2 starting!")

import os
from helper_lvl1 import *
import time
import matplotlib.pyplot as plt
import scipy

starttime = time.time()
lvl1_sources = cwd + "\\sources\\lvl1_produced\\"
default_extension = ".csv"
img_extension = ".png"
folder_plots = cwd + "\\sources\\plots\\"
folder_plots_lvl2 = folder_plots + "\\lvl2\\"
folder_plots_reg_line = folder_plots + "\\reg_lines\\"

config_settings = read_config()
defined_beginning = config_settings[0]
defined_ending = config_settings[1]
buy_amount = config_settings[2]

timelist = read_timelist(defined_beginning, defined_ending)
second_timelist = timelist.copy()

print("Creating file cube!")

def get_file_cube(location):
    file_list = [os.path.splitext(filename)[0] for filename in os.listdir(location)]
    files = {}
    for file in file_list:
        file_contents_hold = {}
        read_file = open((lvl1_sources+file+default_extension), "r")
        hold = read_file.read().split("\n")
        for i in range(len(hold)):
            file_contents_hold[second_timelist[i][0]] = hold[i].split(", ")
        files[file] = dict(file_contents_hold)
    return files, file_list

file_cube, file_list = get_file_cube(lvl1_sources)

print("File Cube took {}s to create!".format(round(time.time()-starttime, 2)))

bbitop15 = {'AMZN':0.0666, 'AAPL':0.0666, 'AVGO':0.0666, 'BRK-B':0.0666, 'GOOG':0.0666, 'GOOGL':0.0666, 'GS':0.0666, 'HD':0.0666, 'MCD':0.0666, 'META':0.0666, 'MSFT':0.0666, 'NVDA':0.0666, 'PEP':0.0666, 'TSLA':0.0666, 'UNH':0.0666}
bbi15 = {'BAC':0.0666, 'BLK':0.0666, 'F':0.0666, 'IVR':0.0666, 'JNJ':0.0666, 'JPM':0.0666, 'KO':0.0666, 'RITM':0.0666, 'SIRI':0.0666, 'SPG':0.0666, 'TGT':0.0666, 'VOO':0.0666, 'VOOV':0.0666, 'WMT':0.0666, 'XOM':0.0666}
bbi7 = {'ARCC':0.1333, 'ET':0.1333, 'NEWT':0.1333, 'NLY':0.1333, 'PSEC':0.1998, 'T':0.1333, 'VTI':0.1333}

day_array = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']

# manually doing this cause I do not have time to figure out how to implement it otherwise...
bbitop15_dict_wo = {}
bbitop15_dict_bo = {}
bbitop15_dict_avg = {}

bbi15_dict_wo = {}
bbi15_dict_bo = {}
bbi15_dict_avg = {}

bbi7_dict_wo = {}
bbi7_dict_bo = {}
bbi7_dict_avg = {}

def create_figure(file_cube, day_array, file, second_timelist):
    fig = plt.figure(figsize=(13, 11), layout="constrained")
    spec = fig.add_gridspec(2,2)
    
    ax0 = fig.add_subplot(spec[0, :])
    ax0.set_xlabel("Time accounted for (Days)")
    ax0.set_ylabel("Percentage Growth")
    plt.axhline(y=0, linestyle='--')
    ax0.plot([i for i in range(len(second_timelist))], [(file_cube[file]["averaged"][line[0]]*100) for line in second_timelist], color='purple', linestyle='-', linewidth= 3, marker='o', markerfacecolor='blue', markersize=3)
    ax0.plot([i for i in range(len(second_timelist))], [(file_cube[file]["worst occurences"][line[0]]*100) for line in second_timelist], color='red', linestyle='-', linewidth= 3, marker='o', markerfacecolor='blue', markersize=3)
    ax0.plot([i for i in range(len(second_timelist))], [(file_cube[file]["best occurences"][line[0]]*100) for line in second_timelist], color='blue', linestyle='-', linewidth= 3, marker='o', markerfacecolor='blue', markersize=3)
    
    ax10 = fig.add_subplot(spec[1, 0])
    ax10.bar(day_array, file_cube[file]["worst occurences distro"], width=0.8, color="red")
    ax10.set_title(file + " Worst Occurences Distribution")
    
    ax11 = fig.add_subplot(spec[1, 1])
    ax11.bar(day_array, file_cube[file]["best occurences distro"], width=0.8, color="blue")
    ax11.set_title(file + " Best Occurences Distribution")
    
    fig.suptitle("Graphs produced from data for " + file)
    plt.savefig(folder_plots + file + "_plot" + img_extension)
    plt.close()

def create_figure_BBIs(wo, bo, avg, fn):
    fig = plt.figure(figsize=(13,11), layout="constrained")
    spec = fig.add_gridspec(1,1)
    ax0 = fig.add_subplot(spec[0,0])
    plt.axhline(y=0, linestyle='--')
    ax0.set_xlabel("Time account for (Days)")
    ax0.set_ylabel("Percentage Growth")
    ax0.plot([i for i in range(len(second_timelist))], [(avg[line[0]]*100) for line in second_timelist], color='purple', linestyle='-', linewidth= 3, marker='o', markerfacecolor='blue', markersize=3)
    ax0.plot([i for i in range(len(second_timelist))], [(wo[line[0]]*100) for line in second_timelist], color='red', linestyle='-', linewidth= 3, marker='o', markerfacecolor='blue', markersize=3)
    ax0.plot([i for i in range(len(second_timelist))], [(bo[line[0]]*100) for line in second_timelist], color='blue', linestyle='-', linewidth= 3, marker='o', markerfacecolor='blue', markersize=3)
    ax0.set_title("Graphs produced from data for " + fn)
    plt.savefig(folder_plots_lvl2 + fn + "_plot" + img_extension)
    plt.close()
    
def create_figure_other(file_cube, file):
    fig = plt.figure(figsize=(13,11), layout="constrained")
    spec = fig.add_gridspec(1,1)
    ax0 = fig.add_subplot(spec[0,0])
    plt.axhline(y=0, linestyle='--')
    ax0.set_xlabel("Time account for (Days)")
    ax0.set_ylabel("Percentage Growth")
    ax0.plot([i for i in range(len(second_timelist))], [(file_cube[file]["averaged"][line[0]]*100) for line in second_timelist], color='purple', linestyle='-', linewidth= 3, marker='o', markerfacecolor='blue', markersize=3)
    ax0.plot([i for i in range(len(second_timelist))], [(file_cube[file]["worst occurences"][line[0]]*100) for line in second_timelist], color='red', linestyle='-', linewidth= 3, marker='o', markerfacecolor='blue', markersize=3)
    ax0.plot([i for i in range(len(second_timelist))], [(file_cube[file]["best occurences"][line[0]]*100) for line in second_timelist], color='blue', linestyle='-', linewidth= 3, marker='o', markerfacecolor='blue', markersize=3)
    ax0.set_title("Graphs produced from data for " + file)
    plt.savefig(folder_plots_lvl2 + file + "_plot" + img_extension)
    plt.close()

print("Generating figures and regression lines!")
starttime2 = time.time()

for file in file_list:
    wo_array = [0] * 5
    bo_array = [0] * 5
    averaged_dict =  {}
    bo_dict = {}
    wo_dict = {}
    
    for line in second_timelist:
        dict_cont_array = file_cube[file][line[0]]
        dict_float_array = []
        for x in dict_cont_array:
            dict_float_array.append(float(x))
        wo_array[dict_float_array.index(min(dict_float_array))] = wo_array[dict_float_array.index(min(dict_float_array))] + 1
        bo_array[dict_float_array.index(max(dict_float_array))] = bo_array[dict_float_array.index(max(dict_float_array))] + 1
        averaged_dict[line[0]] = round((sum(dict_float_array)/5), 4)
        wo_dict[line[0]] = min(dict_float_array)
        bo_dict[line[0]] = max(dict_float_array)
        
        if file in bbi7:
            if line[0] in bbi7_dict_wo:
                bbi7_dict_wo[line[0]] = round(bbi7_dict_wo[line[0]] + (wo_dict[line[0]] * bbi7[file]),4)
            else:
                bbi7_dict_wo[line[0]] = round((wo_dict[line[0]] * bbi7[file]),4)
            if line[0] in bbi7_dict_bo:
                bbi7_dict_bo[line[0]] = round(bbi7_dict_bo[line[0]] + (bo_dict[line[0]] * bbi7[file]),4)
            else:
                bbi7_dict_bo[line[0]] = round((bo_dict[line[0]] * bbi7[file]),4)
            if line[0] in bbi7_dict_avg:
                bbi7_dict_avg[line[0]] = round(bbi7_dict_avg[line[0]] + (averaged_dict[line[0]] * bbi7[file]),4)
            else:
                bbi7_dict_avg[line[0]] = round((averaged_dict[line[0]] * bbi7[file]),4)
        if file in bbitop15:
            if line[0] in bbitop15_dict_wo:
                bbitop15_dict_wo[line[0]] = round(bbitop15_dict_wo[line[0]] + (wo_dict[line[0]] * bbitop15[file]),4)
            else:
                bbitop15_dict_wo[line[0]] = round((wo_dict[line[0]] * bbitop15[file]),4)
            if line[0] in bbitop15_dict_bo:
                bbitop15_dict_bo[line[0]] = round(bbitop15_dict_bo[line[0]] + (bo_dict[line[0]] * bbitop15[file]),4)
            else:
                bbitop15_dict_bo[line[0]] = round((bo_dict[line[0]] * bbitop15[file]),4)
            if line[0] in bbitop15_dict_avg:
                bbitop15_dict_avg[line[0]] = round(bbitop15_dict_avg[line[0]] + (averaged_dict[line[0]] * bbitop15[file]),4)
            else:
                bbitop15_dict_avg[line[0]] = round((averaged_dict[line[0]] * bbitop15[file]),4)
        if file in bbi15:
            if line[0] in bbi15_dict_wo:
                bbi15_dict_wo[line[0]] = round(bbi15_dict_wo[line[0]] + (wo_dict[line[0]] * bbi15[file]),4)
            else:
                bbi15_dict_wo[line[0]] = round((wo_dict[line[0]] * bbi15[file]),4)
            if line[0] in bbi15_dict_bo:
                bbi15_dict_bo[line[0]] = round(bbi15_dict_bo[line[0]] + (bo_dict[line[0]] * bbi15[file]),4)
            else:
                bbi15_dict_bo[line[0]] = round((bo_dict[line[0]] * bbi15[file]),4)
            if line[0] in bbi15_dict_avg:
                bbi15_dict_avg[line[0]] = round(bbi15_dict_avg[line[0]] + (averaged_dict[line[0]] * bbi15[file]),4)
            else:
                bbi15_dict_avg[line[0]] = round((averaged_dict[line[0]] * bbi15[file]),4)
    
    file_cube[file]["worst occurences distro"] = wo_array
    file_cube[file]["best occurences distro"] = bo_array
    file_cube[file]["averaged"] = averaged_dict
    file_cube[file]["worst occurences"] = wo_dict
    file_cube[file]["best occurences"] = bo_dict
    
    # messing with linear regression lines...
    w_slope, w_intercept, w_r_value, w_p_value, w_std_err = scipy.stats.linregress([i for i in range(len(second_timelist))], [file_cube[file]["worst occurences"][line[0]] for line in second_timelist])
    b_slope, b_intercept, b_r_value, b_p_value, b_std_err = scipy.stats.linregress([i for i in range(len(second_timelist))], [file_cube[file]["best occurences"][line[0]] for line in second_timelist])
    a_slope, a_intercept, a_r_value, a_p_value, a_std_err = scipy.stats.linregress([i for i in range(len(second_timelist))], [file_cube[file]["averaged"][line[0]] for line in second_timelist])
    
    regression_line_writer = open(folder_plots_reg_line+file+".txt", "w")
    regression_line_writer.write("Worst")
    regression_line_writer.write("\ny= "+str(round(w_slope,8))+"x + ("+str(round(w_intercept,8))+")")
    regression_line_writer.write("\nR: " + str(round(w_r_value,8)))
    regression_line_writer.write("\nP: " + str(round(w_p_value,8)))
    regression_line_writer.write("\nSTD Err: " + str(round(w_std_err,8)))
    regression_line_writer.write("\n\nBest")
    regression_line_writer.write("\ny= "+str(round(b_slope,8))+"x + ("+str(round(b_intercept,8))+")")
    regression_line_writer.write("\nR: " + str(round(b_r_value,8)))
    regression_line_writer.write("\nP: " + str(round(b_p_value,8)))
    regression_line_writer.write("\nSTD Err: " + str(round(b_std_err,8)))
    regression_line_writer.write("\n\nAverage")
    regression_line_writer.write("\ny= "+str(round(a_slope,8))+"x + ("+str(round(a_intercept,8))+")")
    regression_line_writer.write("\nR: " + str(round(a_r_value,8)))
    regression_line_writer.write("\nP: " + str(round(a_r_value,8)))
    regression_line_writer.write("\nSTD Err: " + str(round(a_std_err,8)))
    regression_line_writer.close()
    
    create_figure(file_cube, day_array, file, second_timelist)

print("Done with bulk plots!")
print("Bulk plots & regression vectors took {}s to create!".format(round(time.time()-starttime2, 2)))

create_figure_BBIs(bbi7_dict_wo, bbi7_dict_bo, bbi7_dict_avg, "BBI7")
create_figure_BBIs(bbi15_dict_wo, bbi15_dict_bo, bbi15_dict_avg, "BBI15")
create_figure_BBIs(bbitop15_dict_wo, bbitop15_dict_bo, bbitop15_dict_avg, "BBI-Top15")

print("Done with BBI plots!")

create_figure_other(file_cube, "NASDAQ")
create_figure_other(file_cube, "DJIA")
create_figure_other(file_cube, "S&P500")

print("Done with other plots!")

print("Level_2 took {}s to complete.".format(round(time.time()-starttime2, 2)))
# end of program