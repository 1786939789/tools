import os
def add_write_txt(path,txt):
    f=open(path,"ab")
    f.write(txt)
    f.write("\n")
    f.close()
def read_txt(path):
    f=open(path,"rb")
    txt=f.read()
    f.close()
    return txt
def read_lines(path):
    f=open(path,"r")
    lines=[]
    for line in f.readlines():
        lines+=[line.strip('\n')]
    return lines
def write_txt(path,txt):
    f=open(path,"wb")
    f.write(txt)
    f.close()
def info():
    print("add_write_txt(path,txt) -> void")
    print("read_txt(path) -> void")
    print("write_txt(path,txt) -> void")
    exit()
