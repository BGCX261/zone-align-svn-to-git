#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tool_file import Tool_file
from tool_read_log import Tool_read_log
#import numpypy as numpy
import numpy
#import matplotlib.mlab as mlab
#import matplotlib.pyplot as plt
import Image
import time
import UserList
from data_structure import DistMatrix, Dotplot
import cPickle as pickle
#import pprint
import munk


import os
import sys

from log_optparser import opt_parser_treatlog

def convert2numpy(dist_matrix) :
  matrix2 = []
  for line in dist_matrix.data :
    matrix2.append(list(line))
  a = numpy.array(matrix2,"float32")
  return a

def convert2list(numpy_matrix) :
  m = []
  for line in numpy_matrix :
    l = [1. - v for v in line]
    m.append(l)
  return m

def get_pickle_basename(filein) :
  l = os.path.split(filein)
  n = l[-1].split(".")
  return ".".join(n[:-1])

def normalize_row_matrix(matrix) :
  m2 = []
#  lmax = []
#  for l in matrix :
#    lmax.append(max(l))
#  maxi = max(lmax)

  for l in matrix :
    maxi = max(l)
    line = [float(val) / float(maxi) if maxi != 0 else 0 for val in l]
    m2.append(line)
  res = numpy.array(m2,"float32")
  return res

def matrix2image(matrix,_path):
  a_print = matrix.copy()
  a_print = (1. - a_print) * 255
  a_print = a_print.astype(numpy.uint8)
  Image.fromarray(a_print).save(_path)

def matrix2matrix_linkage(matrix, linkage) :
  m = matrix.copy()
  for i,l in enumerate(m) :
    for j,v in enumerate(l) :
      if linkage[i] == j :
        m[i][j] = 1. - v
      else :
        m[i][j] = 0.
  return m 

def compute_munkres(matrix) :
  m = munk.maxWeightMatching(matrix)
  return m[0]

def compute_score(matrix, linkage) :
  s1 = 0
  for i,j in linkage.iteritems() :
    s1 += matrix[i][j]
  return s1


parser = opt_parser_treatlog()
(opt_options, opt_args) = parser.parse_args(sys.argv[1:])
path_pickle = opt_options.picklefile

pickle_basename = get_pickle_basename(path_pickle)

pic = pickle.load(open(path_pickle))

dic_matrix_array = pic['dic_matrix_array']
dic_rep_dist = pic['dic_rep_dist']
dico_name_multidoc = pic['dico_name_multidoc']
print dico_name_multidoc


s = time.clock()

#
# boucle de génération des matrices
#

for methode_dist,rep in dic_matrix_array.iteritems() :
  for couple,dic_md in rep.iteritems() :
    print "bmp", couple
    for id_md,matrix in dic_md.iteritems() :
      d = Dotplot([],[])
      d.from_pickle(matrix)
      m = normalize_row_matrix(convert2numpy(d))
      linkage  = compute_munkres(convert2list(m))
      score    = compute_score(m, linkage) / float(max(d._width, d._height))
      dir_name = './bmp/%s_%s/'%(pickle_basename,methode_dist)
      if os.path.isdir(dir_name) == False :
        os.makedirs(dir_name)

#      name_md = dico_name_multidoc[str(id_md)]
      o1 = "%s%s.%s-%s.bmp"%(dir_name, id_md, couple[0], couple[1])
      o2 = "%s%s.%s-%s.linkage.bmp"%(dir_name, id_md, couple[0], couple[1])
      print ">>", o1, o2
      print "distance ::", score
      matrix2image(m, o1)
      ml = matrix2matrix_linkage(m, linkage)
      matrix2image(ml, o2)

#
# A commenter pour ne pas générer les .pdf
#
tt = time.clock() - s
print "time      : %f"%(tt)
exit()
for methode_dist,rep in dic_rep_dist.iteritems() :
  for couple,l in rep.iteritems() :
    print "pdf", couple
    l = numpy.array(l,"float32")
    n, bins, patches = plt.hist(l, 20, normed=0, facecolor='green', alpha=0.75)
    plt.ylabel('distance')
    plt.ylabel('densite')
    plt.title(r'Repartition des distances')
    plt.axis()
    plt.grid(True)
    dir_name = './pdf/%s_%s/'%(pickle_basename,methode_dist)
    if os.path.isdir(dir_name) == False :
      os.makedirs(dir_name)
    o = "%s%s_%s_%s.pdf"%(dir_name,methode_dist,couple[0],couple[1])
    print ">>", o
    plt.savefig(o)
    plt.figure()

tt = time.clock() - s
print "time      : %f"%(tt)
