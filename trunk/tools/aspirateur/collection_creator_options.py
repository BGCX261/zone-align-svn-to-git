#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import datetime

def split_languages(s) :
  l = s.split(',')
  if "all" in l :
    l = ["bg","cs","de","da","el","en","es","et","fr","fi","hu","it","lt","lv","mt","nl","pt","pl","sk","sl","sv","ro"]
  else :
    for elt in l :
      assert(len(elt) == 2)
  return l

   
def define_period(s):
    try:
        yyyy, mm, dd = map(int, s.split(','))
        return yyyy, mm, dd
    except:
        raise argparse.ArgumentTypeError("Coordinates must be yyyy, mm, dd")

def read_list_arg1(option, opt, value, parser):
  setattr(parser.values, option.dest, value.split(','))

def collection_build_argparse() :
  parser = argparse.ArgumentParser(description='Options du créateur de collection :')

  parser.add_argument('-d', '--input_dir', dest='input_dir', default='corpus',
                   help='input directory, folder to find corpus')

  parser.add_argument('-o', '--output_dir', dest='output_dir', default='collection',
                   help='output directory, folder to create collection (default=\'collection\')')

  parser.add_argument('-l', '--lg', dest='languages', type=split_languages, default="all", 
                   help='list of languages ​​for which you want to crawl documents (default = all 25 languages)')

  parser.add_argument('-p', '--period', dest='period', default= None, type=define_period, nargs=2, 
                   help='define the start and the end of the crawl (default value : from 1999,01,01 to 2012,12,31')

  parser.add_argument('-b', '--booleen', dest='booleen', default='and', 
                   help='define if languages in list of languages are all mandatory (mode and) or not (mode or). (default = and)')

  parser.add_argument('-m', '--manifest', dest='manifest', default=False, action='store_true',
                   help='put the option to generate the press releases list of paths')
  
  parser.add_argument('-c', '--clean', dest='clean', default=False, action='store_true',
                   help='clean html')
  return parser

def time_build_argparse() :
  parser = collection_build_argparse()
  parser.add_argument('-s', '--step', dest='step', default=7, type=int,
                   help='define the time step')

  parser.add_argument('-w', '--window', dest='window', default=6, type=int,
                   help='define the time step')

  return parser

