#!/usr/local/bin/pythonw
# -*- coding: utf-8 -*-
import re
import sys
from bs4 import BeautifulSoup
from bs4 import NavigableString
from tidylib import tidy_document

def clean_str(soup_elt) :
  elt = unicode(str(soup_elt), 'utf-8');
  elt = re.sub("</?[^>]+>", "", elt, flags=re.U, count=0)
  elt = re.sub("\s+", " ", elt, flags=re.U, count=0)
  elt = elt.strip(" \t\r")
  return elt

def clean_list(soup_elt) :
  l = []
  for sub_elt in soup_elt.children :
    elt = clean_str(sub_elt)
    if(len(elt) > 0) :
      l.append(elt)
  return l

def clean_pre(soup_elt) :
  elt = unicode(str(soup_elt),'utf-8')
  l = re.split("([\s]*\n[\s]*){2,}", elt, maxsplit=0, flags=re.U)
  nl = []
  for e in l :
    e = re.sub("</?[^>]+>", "", e, flags=re.U, count=0)
    e = re.sub("\s+", " ", e, flags=re.U, count=0) 
    e = e.strip(" \t\r")
    if(len(e) > 0):
      nl.append(e)
  return nl

def clean_html(s) :
  str_unicode = unicode(s, 'utf-8')
  str_unicode, _ = tidy_document(str_unicode)
  soup = BeautifulSoup(str_unicode)
  list_str = []
  for soup_elt in soup.body.children :
    if isinstance(soup_elt, NavigableString) :
      continue
    if soup_elt.name == 'ul' or soup_elt.name == 'ol' :
      for e in clean_list(soup_elt) :
        list_str.append(e)
      continue
    if soup_elt.name == 'pre' :
      for e in clean_pre(soup_elt) :
        list_str.append(e)
      continue

    elt = clean_str(soup_elt)
    if(len(elt) > 0) :
      list_str.append(elt)
  return list_str

if __name__ == '__main__':
  file_src = sys.argv[1]
  f_read = open(file_src, 'r')
  str_file = f_read.read()
  for s in clean_html(str_file) :
    print s.encode('utf-8')
