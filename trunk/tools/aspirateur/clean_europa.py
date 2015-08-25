#!/usr/local/bin/pythonw
# -*- coding: utf-8 -*-
import re
import os
import glob
import sys

def clean_html(path_in, path_out) :
  f_read = open(path_in, 'r')
  str_file = f_read.read()
  clean_str_unicode = unicode(str_file, 'utf-8')
  f_read.close()
  clean_str_unicode = re.sub("</?[^>]+>", "", clean_str_unicode, flags=re.U, count=0)
  clean_str_unicode = re.sub("\r*", "", clean_str_unicode, count=0)
  clean_str_unicode = re.sub("([\s]*\n[\s]*){2,}", "", clean_str_unicode, count=0, flags=re.U)
  clean_str = clean_str_unicode.encode('utf-8', 'replace')
  f_write = open(path_out, 'w')
  print >>f_write, clean_str
  f_write.close()

file_src = sys.argv[1]
file_tgt = sys.argv[2]

clean_html(file_src, file_tgt)

exit()

directory_src = sys.argv[1]
directory_tgt = sys.argv[2]
if os.path.isdir(directory_tgt) == False :
  os.makedirs(directory_tgt)

all_filename_src = os.path.join(directory_src, '*')
list_filename = glob.glob(all_filename_src)

for path_src in list_filename :
  filename_src = path_src.split('/')[-1]
  f_read = open(path_src, 'r')
  str_file = f_read.read()
  str_unicode_file = unicode(str_file, 'utf-8', 'replace')
  f_read.close()
  clean_str_unicode = re.sub('[ \t]+',' ', str_unicode_file)
  clean_str_unicode = re.sub('<[^>]+>','', clean_str_unicode, re.U|re.DOTALL)
  clean_str_unicode = re.sub('(\n[\s]){2,}','', clean_str_unicode, re.U|re.DOTALL)
  clean_str = clean_str_unicode.encode('utf-8', 'replace')
  filename_tgt = os.path.join(directory_tgt, filename_src)
  f_write = open(filename_tgt, 'w')
  print '\r', filename_tgt,'           ',
  print >>f_write, clean_str
  f_write.close()
