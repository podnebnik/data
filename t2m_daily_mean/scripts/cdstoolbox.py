#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 00:07:36 2021

@author: zaplotnikz
"""

import __main__
import cdsapi
import sys
 
c = cdsapi.Client()
 
with open(__main__.__file__) as f:
    code = f.read()
 
print(c.download(c.workflow(code)))
sys.exit(0)