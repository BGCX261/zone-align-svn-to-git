#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import os
import glob
import re

def url2content(url, loop=10) :
  while loop > 0 :
    loop -= 1
    try :
      sock = urllib.urlopen(url)
      content = sock.read()
      sock.close()
      return content
    except :
      pass

def create_dir(directory, yyyy, mm) :
  subdirectory_yyyy = os.path.join(directory, yyyy)
  subdirectory_mm = os.path.join(subdirectory_yyyy, mm)
  if not os.path.isdir(subdirectory_yyyy) :
    os.makedirs(subdirectory_yyyy)
  if not os.path.isdir(subdirectory_mm) :
    os.makedirs(subdirectory_mm)
  return subdirectory_mm

#i = url2content('http://www.google.com', 100)
#print i


def list_subdir(directory) :                                
  pattern_subdir = os.path.join(directory, '*')
  l = []
  for subdir in glob.glob(pattern_subdir) :
    l.append(os.path.split(subdir)[-1])
  return l

def get_extremum(directory, select) :
  list_year = list_subdir(directory)
  year = select(list_year)
  dir_year = os.path.join(directory, year)
  list_month = list_subdir(dir_year)
  month = select(list_month)
  dir_month = os.path.join(dir_year,month)
  glob_file = os.path.join(dir_month, '*.html')
  pattern_compile = re.compile('.*[0-9]{4}-[0-9]{2}-([0-9]{2})_.*\.html')
  list_day = []
  for path in glob.glob(glob_file) :
    list_day.append(pattern_compile.search(path).group(1))
  day = select(list_day)
  return year,month,day

def get_start(directory) :
  return get_extremum(directory, min)

def get_end(directory) :
  return get_extremum(directory, max)

def starting_ending_date(period,d) :
  if (period == None) :
    period = ['','']
    period[0] = get_start(d)
    period[1] = get_end(d)
  elif period[0] > period[1] :
    period[0], period[1] = period[1], period[0]
  return period[0], period[1]
