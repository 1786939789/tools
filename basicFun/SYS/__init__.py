import os
import commands
def get_ram():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            # print(line.split()[1:4])
            RAM_total = round(int(line.split()[1:4][0]) / 1000,1)
            RAM_used = round(int(line.split()[1:4][1]) / 1000,1)
            RAM_free = round(int(line.split()[1:4][2]) / 1000,1)         
            return(RAM_total,RAM_used,RAM_free)
def info():
    print("get_ram()->RAM_total,RAM_used,RAM_free")
