import numpy as np
import os,sys
from subprocess import call
import time

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()
    
    
for year in list(range(2007,2023)):
    print(year)
    replace_line("workflow.py", 19, "    for yr in ['{0}']:\n".format(year))
    call("python workflow.py",shell=True)
    time.sleep(5)
    call("mv *.nc tcw_{0}.nc".format(year),shell=True)
    call("mv tcw_{0}.nc ../sources/".format(year),shell=True)
    
