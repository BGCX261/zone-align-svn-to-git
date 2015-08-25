#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

class Tool_file(object) :

  def __init__(self) :
    pass 

  def file_load(self, path) :
    f = open(path)
    r = f.read()
    f.close()
    return r

  def csv_load(self, path, delim_line, delim_col) :
    r = csv.reader(self.file_load(path), delimiter = delim_line, quotechar = '|')
    return r

