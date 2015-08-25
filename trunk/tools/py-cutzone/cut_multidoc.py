#!/usr/bin/env python<F5>
# -*- coding: utf-8 -*-
import re
import sys
import os
import glob
from cut_optparser import opt_parser

def read_file(path) :
  f = open(path,'r')
  s = f.read()
  f.close()
  return s

def get_info_file(path) :
  s = read_file(path)
  su = unicode(s,'utf-8')
  lu = len(su)
  return su,lu

def cut2offset(indice_cut, len_su) :
  '''sur 200x200 :: taille de l'image par défaut'''
  return (indice_cut / 200.) * len_su

def cutpath2info(cutpath) :
  l = os.path.split(cutpath)
  pathdir = "".join(l[:-1])
  filename = l[-1]
  pat = '(.*)\.([a-z]{2})-([a-z]{2})'
  m = re.search(pat,filename)
  idmultidoc, lg1, lg2 = m.group(1), m.group(2), m.group(3)
  return pathdir, idmultidoc, lg1, lg2

def idmultidoc2info(idmultidoc, pathdir_corpus) :
  d = os.path.join(pathdir_corpus,'*','%s*'%idmultidoc)
  l = glob.glob(d)
  if len(l) == 1 :
    path, fn = os.path.split(l[0])
    subdirname = path.split('/')[-1]
    return path, subdirname, l[0]
  else :
    print idmultidoc, pathdir_corpus, l
    print 'error detection'

def get_all_diagfile(diagdir, typediag) :
  lt = []
  for typ in typediag :
    if typ == 'a' :
      lt.append('asynchrone')
    if typ == 'u' :
      lt.append('indefini')
    if typ == 's' :
      lt.append('synchrone')
  reg = '(%s)'%("|".join(lt))

  tall = os.path.join(diagdir,'*')
  rt = '.*\.[a-z]{2}-[a-z]{2}\.xml_%s\.txt'%(reg)
  l = []
  for p in glob.glob(tall) :
    fn = os.path.split(p)[-1]
    m = re.match(rt,fn)
    if m :
      id_multidoc,lgs,diagt,suffix = fn.split('.')
      rec = '%s.%s.%s'%(id_multidoc,lgs,suffix) 
      path_cut = os.path.join(diagdir,rec)
      l.append(path_cut)

  return l

def treat_cut_file_line(line) :
  strl = line.strip('() ')
  a1,a2 = strl.split(') (')
  s1,s2 = a1.split(', ')
  e1,e2 = a2.split(', ')
  return int(s1),int(e1),int(s2),int(e2) 

def treat_cut_file(cutpath, corpuspath, corpusout) :
  co = corpusout
  if os.path.isdir(co) == False :
    os.makedirs(co)
  else :
    print ">dir %s exists!"%(co)

  pathdir,idmultidoc,lg1,lg2 = cutpath2info(cutpath)
  t1 = '%s.%s.xml'%(idmultidoc,lg1)
  t2 = '%s.%s.xml'%(idmultidoc,lg2)
  print t1
  print t2
  path, subdirname, fn1 = idmultidoc2info(t1,corpuspath)
  path, subdirname, fn2 = idmultidoc2info(t2,corpuspath)
  print fn1
  print fn2
  info_t1 = get_info_file(fn1)
  info_t2 = get_info_file(fn2)

  s = read_file(cutpath)
  list_lignes = s.split('\n')

  i = 0
  for l in list_lignes :
    if l == '' : continue
    s1,e1,s2,e2 = treat_cut_file_line(l)
#    print '[%s,%s], [%s,%s]'%(s1,e1,s2,e2)
    ns1 = cut2offset(s1, info_t1[1]) 
    ne1 = cut2offset(e1, info_t1[1])
    ns2 = cut2offset(s2, info_t2[1]) 
    ne2 = cut2offset(e2, info_t2[1])
#    print '[%s,%s], [%s,%s]'%(ns1,ne1,ns2,ne2)

    nd1 = info_t1[0][int(ns1):int(ne1)+1]
    nd2 = info_t2[0][int(ns2):int(ne2)+1]

    new_subdirname = '%s_%d'%(subdirname,i)
    dirpartname = '%s/%s'%(co,new_subdirname)
    if os.path.isdir(dirpartname) == False :
      os.makedirs(dirpartname)

    fn1_part = '%s/%s_%d.%s.xml'%(dirpartname,idmultidoc,i,lg1)
    fn2_part = '%s/%s_%d.%s.xml'%(dirpartname,idmultidoc,i,lg2)

    of1 = open(fn1_part,'w')
    of2 = open(fn2_part,'w')

    print >> of1, nd1.encode('utf-8')
    print >> of2, nd2.encode('utf-8')

    i += 1

def main(args) :
  parser = opt_parser()
  (opt_options, opt_args) = parser.parse_args(args)  
  diagdirpath = opt_options.diagdir
  corpuspath = opt_options.corpus
  corpusout = opt_options.outputdir
  typediag = opt_options.typediag

  list_df = get_all_diagfile(diagdirpath, typediag)

  for diagfile in list_df :
    treat_cut_file(diagfile, corpuspath, corpusout)

if __name__ == "__main__":
  main(sys.argv[1:])

 
#cutpath = sys.argv[1]
#corpuspath = sys.argv[2]
#corpusout = sys.argv[3]

