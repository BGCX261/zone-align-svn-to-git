#!/usr/local/bin/pythonw
# -*- coding: utf-8 -*-
import re
import os
import glob
import sys
import shutil

import fnmatch

def recursive_glob(path_dir) :
  matches = []
  for root, dirnames, filenames in os.walk(path_dir):
    for filename in fnmatch.filter(filenames, '*'):
        matches.append(os.path.join(root, filename))
  return matches

directory_src = sys.argv[1]
directory_tgt = sys.argv[2]

if os.path.isdir(directory_tgt) == False :
  os.makedirs(directory_tgt)

list_lg = sys.argv[3:]

if list_lg == [] :
  list_lg = ['fr', 'en', 'es', 'el', 'fi', 'hu', 'de', 'da', 'lv', 'lt']

set_lg = set(list_lg)

#all_filename_src = os.path.join(directory_src, '*')
#list_filename = glob.glob(all_filename_src)
list_filename = recursive_glob(directory_src)

dictionnary_multi = {}
dictionnary_path_src = {}

for path_src in list_filename :
  filename_src = path_src.split('/')[-1]
  info_document = filename_src.split('.')
  multidocument_name = info_document[0]
  lg_doc = info_document[1]
  if dictionnary_multi.has_key(multidocument_name) == False :
    dictionnary_multi[multidocument_name] = set()
  dictionnary_multi[multidocument_name].add(lg_doc)
  dictionnary_path_src[(multidocument_name, lg_doc)] = path_src

cpt = 1
list_id_multidoc = dictionnary_multi.keys()
list_id_multidoc.sort()
for i, id_multi in enumerate(list_id_multidoc) :
  set_lg_multi = dictionnary_multi[id_multi]
  if set_lg <= set_lg_multi:
    subdirectory_tgt = os.path.join(directory_tgt, str(cpt))
    if os.path.isdir(subdirectory_tgt) == False :
      os.makedirs(subdirectory_tgt)
    for lg in set_lg :
      filename = '%s.%s.xml'%(id_multi, lg)
      filepath_src = dictionnary_path_src[(id_multi, lg)]
#      filepath_src = os.path.join(directory_src, filename)
      filepath_tgt = os.path.join(subdirectory_tgt, filename)
      print filepath_src, '>>' , filepath_tgt
      shutil.copyfile(filepath_src, filepath_tgt)
    cpt += 1

