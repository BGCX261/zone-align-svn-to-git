#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import datetime

def split_languages(s) :
  l = s.split(',')
  if "all" in l :
    l = ["bg","cs","de","da","el","en",
         "es","et","fr","ga","fi","hu",
         "it", "lt","lv","mt","nl","pt",
         "pl", "sk","sl","sv","ro"]
  else :
    for elt in l :
      assert(len(elt) == 2)
        
  return l
    
def define_period(s):
    try:
        yyyy, mm, dd = map(int, s.split(','))
        return yyyy, mm, dd
    except:
        raise argparse.ArgumentTypeError("Coordinates must be yyyy,mm,dd")

def read_list_arg1(option, opt, value, parser):
  setattr(parser.values, option.dest, value.split(','))

def build_argparse() :

  parser = argparse.ArgumentParser(description='Crawler of europa.eu.')

  parser.add_argument('-o', '--output_dir', dest='output_dir', default='corpus',
                   help='output directory, folder to drop crawled files (default value : -o corpus)')

  parser.add_argument('-l', '--lg', dest='languages', type=split_languages, default="all", 
                   help='list of languages for which you want to crawl documents (default value : -l all)')

  parser.add_argument('-p', '--period', dest='period', default=[(1999, 01, 01), (2012, 12, 31)], type=define_period, nargs=2, 
                   help='define the start and the end of the crawl (default value : from 1999,01,01 to 2012,12,31)')

  parser.add_argument('-q', '--quiet', dest='verbose', default=True, action='store_false',
                      help = 'desactive the verbose mode -- no print in stdout (default value : verbose)')

  parser.add_argument('-g', '--log', dest='log', default = '',
                      help='write log in LOG (default value : "")')

  return parser

