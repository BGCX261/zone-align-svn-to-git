#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tool_file import Tool_file
from tool_read_log import Tool_read_log
import time
#import UserList
import sys
import os

import tool_misc as tm
from data_structure import DistMatrix, Dotplot
import cPickle as pickle

from log_optparser import opt_parser_readlog 

def get_fileout(filein,ext) :
  l = os.path.split(filein)
  n = l[-1].split(".")
  path =  "".join(l[:-1])
  basename =  "".join(n[:-1])
  newname = "%s.%s.%s"%(basename,ext,n[-1])
  return newname

parser = opt_parser_readlog()
(opt_options, opt_args) = parser.parse_args(sys.argv[1:])
path_log = opt_options.logfile

if(opt_options.outputfile == 'default') :
  fileout_name = get_fileout(path_log, 'pickle')
else : 
  fileout_name = opt_options.outputfile

s = time.clock()

trl = Tool_read_log()

##
## Paramètres
##

#list_lg_av = [("en","fr")] ## couples de langues considérés
#list_lg_av = [tuple(sorted(i)) for i in list_lg_av]
                                 ## pour tout prendre, list_lg_av = []
                                 ## (traitement alors très lourd)

list_dist_av = ['docdistance']   ## liste des distances considérées
                                 ## pour ne prendre que la docdistance ::
                                 ## list_dist_av = ['docdistance']
                                 ## list_dist_av = [] est équivalant à
                                 ## list_dist_av = ['distance', 'docdistance']

list_md_av = set([])             ## liste des multidocuments dont on affiche les matrices
                                 ## par exemple ::
                                 ## list_md_av = set([1,3,45])

len_str1 = (0, 1000000)          ## longueur des chaînes considérées de la langue 1 (len_str1) et 2 (len_str2)
len_str2 = (0, 1000000)          ## len_str1 = (1,40) équivaut à considérer les chaînes de la langue 1 de
                                 ## longueur comprise entre 1 et 40
                                 
score_av = (0., 1.)              ## score des distances, score_av = (0,0.3) permet de ne garder que les couples
                                 ## de chaînes ayant une distance comprise entre 0 et 0.3

nb_occ_rel_str1 = (0, 10000000)  ## nb d'occur. dans le corpus monolingue de chaque chaine 
                                 ## 
nb_occ_rel_str2 = (0, 10000000)  ##
                                 ##

nb_diff_doc1 = (0,1000)          ##nb de documents différents dans lequel apparait les chaînes de la langue 1 et 2
nb_diff_doc2 = (0,1000)

##
##
##

list_paquets = []
set_distance = set()
set_couple_lg = set()

def check_list_md(list_md_cur, list_md_av) :
  return (len(list_md_cur - list_md_av) == len(list_md_cur) - len(list_md_av))

def check_nb_occ_rel(d, nb_occ_rel) :
  s = 0
  for k,v in d.iteritems() :
    s += len(v)
  return nb_occ_rel[0] <= s <= nb_occ_rel[1]

cpt = 0
print "header"
dico_name_multidoc = trl.read_header_log(path_log)


print "go"

set_md = set()

for it in trl.path2iter_paquet(path_log) :
  a = tuple(sorted(it['list_lg']))
##  if(a not in list_lg_av and list_lg_av != []) :
##    continue
#
  dist_type, score = it['score_info']
#  score = float(score)
#  if not(score_av[0] <= score <= score_av[1]) : #     score < score_av[0] and score > score_av[1] :
#    continue
#
##  if(dist_type not in list_dist_av and list_dist_av != []) :
##    continue
#
  s1,d1 = it[a[0]]
  s2,d2 = it[a[1]]
#  len_s1 = len(s1)
#  len_s2 = len(s2)
#
#
##  if(not(len_str1[0] <= len_s1 <= len_str1[1]) or not(len_str2[0] <= len_s2 <= len_str2[1])) :
##    continue
#
##  if(len_s1 < len_str1[0] or len_s1 > len_str1[1] or len_s2 < len_str2[0] or len_s2 > len_str2[1]) :
##    continue
#
  k1 = set(d1.keys())
  k2 = set(d2.keys())
  kt = list(k1) + list(k2)
#  lk1 = len(k1)
#  lk2 = len(k2)
#  
##  print sorted(list(k1))
##  print sorted(list(k2))
##  print sorted(list(kt))
##  1/0
#
##  if(not(nb_diff_doc1[0] <= lk1 <= nb_diff_doc1[1]) or not(nb_diff_doc2[0] <= lk2 <= nb_diff_doc2[1])) :
##    continue
#
##  if((check_list_md(k1, list_md_av) == False or check_list_md(k2, list_md_av) == False)
##      and list_md_av != set([])) :
##    continue
#
#  nd1 = check_nb_occ_rel(d1,nb_occ_rel_str1)
#  nd2 = check_nb_occ_rel(d2,nb_occ_rel_str2)
#
##  if(nd1 == False or nd2 == False) :
##    continue

  set_distance.add(dist_type)
  set_couple_lg.add(a)
  list_paquets.append(it)

  for k in kt : set_md.add(k)

#  print "\r", cpt,
#  cpt += 1

list_id_md = sorted(set_md)

#dico_name_multidoc = {}
#for i,id_md in enumerate(list_id_md) :
#  dico_name_multidoc[id_md] = list_name_multidoc[i]

tt = time.clock() - s
print
print "time      : %f"%(tt)

dic_matrix = {}
dic_rep_dist = {}

s = time.clock()

##
## Paramètres
##

cstep = (0.005,0.005) ## pas d'avancement des segments de texte comparés
cgap = (0.01,0.01)    ## taille des segments de texte comparés
c1 = [(i,i+cgap[0]) for i in tm.drange(0,1,cstep[0])]
c2 = [(i,i+cgap[1]) for i in tm.drange(0,1,cstep[1])]

##
##
##

for dist_type in set_distance :
  dic_rep_dist[dist_type] = {}
  dic_matrix[dist_type] = {}
  for couple_lg in set_couple_lg :
    dic_rep_dist[dist_type][couple_lg] = []
    dic_matrix[dist_type][couple_lg] = {}
    for id_md in list_id_md :
      dic_matrix[dist_type][couple_lg][id_md] = Dotplot(c1,c2)


print "go"
cpt = 0
lp = len(list_paquets)
for it in list_paquets :
  if(cpt % 1000 == 0) :
    print cpt, "/", lp
  cpt += 1
  a = list(it['list_lg'])
  a.sort()
  a = tuple(a)

  dist_type, score = it['score_info']

  k1 = set(it[a[0]][1].keys())
  k2 = set(it[a[1]][1].keys())

  dic_rep_dist[dist_type][a].append(float(score))

#  lk = list(k1) + list(k2)
  lk = k1.union(k2)

  for id_multi in lk :

    if(id_multi not in it[a[0]][1] or id_multi not in it[a[1]][1]) :
      continue

    lp1 = it[a[0]][1][id_multi]
    lp2 = it[a[1]][1][id_multi]


    for o1 in lp1 :
      for o2 in lp2 :
        dic_matrix[dist_type][a][id_multi].inc_dot(o1/100.0,o2/100.0, cstep)

dic_matrix_array = {}
for dist_type, l1 in dic_matrix.iteritems() :
  dic_matrix_array[dist_type] = {}
  for a, l2 in l1.iteritems() :
    dic_matrix_array[dist_type][a] = {}
    for id_multi, dot_plot in l2.iteritems() :
      dic_matrix_array[dist_type][a][id_multi] = dot_plot.convert2pickle()

tt = time.clock() - s
print "time      : %f"%(tt)

print ">> pickle %s"%fileout_name

dic_pickle = {
  'dic_matrix_array' : dic_matrix_array,
  'dic_rep_dist' : dic_rep_dist,
  'dico_name_multidoc' : dico_name_multidoc
}

pickle.dump(dic_pickle, open(fileout_name, "wb"))
