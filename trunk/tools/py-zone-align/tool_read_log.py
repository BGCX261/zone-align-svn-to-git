#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tool_file as tf
import re

class Tool_read_log(object) :
  def __init__(self) :
    pass

  def read_header_log(self, path) :
    t = tf.Tool_file()
    text = t.file_load(path)
#    m = re.finditer('.*/([0-9_]+)/(celex_IP.*)\..{2}\.xml', text[:100000])
    m = re.finditer('.*/([0-9_]+)/([^.]+)\..{2}\..*', text[:100000])
    d = {}
    for a in m :
#      if a.group(2) not in d.values() :
      d[a.group(1)] = a.group(2)  

    return d

  def distrib2rel_count(self, distrib, id_multidoc):
    return len(distrib[id_multidoc])

  def str_distrib2info_distrib(self, str_distrib) :
    apparitions = str_distrib.strip().split(" ") 
    dic_res = {}
    for a in apparitions :
      id_document, pos = a.split(":")
#      id_document = int(id_document)
      pos = float(pos)
      if(id_document not in dic_res) :
        dic_res[id_document] = []
      dic_res[id_document].append(pos)
    return dic_res

  def is_paquet_valid(self, paquet) :
    l = len(paquet)
    if(l == 3 and paquet[1][0] == "'" and paquet[2][0] == "'") :
      return True
    elif(l == 5 and paquet[1][0] == "'" and paquet[3][0] == "'") :
      return True
    return False

  def locate_info(self, paquet) :
    l = len(paquet)
    if(l == 3) :
      return paquet[0], paquet[1], paquet[2]
    elif(l == 5) :
      return paquet[0], paquet[1], paquet[3]

  def get_info_distrib(self, info) :
#    info_str1, distrib1 = info.split(") : ")
    l = info.split(") : ")
    info_str1 = ") : ".join(l[:-1])
    distrib1  = l[-1]
    s1, nb_occ1, _ = re.split(" \(([0-9]+)$", info_str1)
    s1 = s1.strip("'")
    return s1, nb_occ1, distrib1

  def path2list_paquet(self, path) :
    res = [p for p in self.path2iter_paquet(path)]
    return res

  def path2iter_paquet(self, path) :
    t = tf.Tool_file()
    text = t.file_load(path)
    paquets = re.split("\n[\s]+\n", text)
    for p in paquets :

      info = p.split("\n")
      if self.is_paquet_valid(info) == False :
        continue

      info0, info1, info2 = self.locate_info(info)

      dist_type, distance_info = info0.split(" : ")
      dist, l1, l2 = distance_info.strip().split(" ")

      s1, nb_occ1, distrib1 = self.get_info_distrib(info1)
      s2, nb_occ2, distrib2 = self.get_info_distrib(info2)

      d1 = self.str_distrib2info_distrib(distrib1)
      d2 = self.str_distrib2info_distrib(distrib2)

      i = {'score_info' : (dist_type, dist), 'list_lg' : (l1, l2), l1 : (s1, d1), l2 : (s2, d2)}

      yield i

  def path2list_paquet_filtered(self, path, config) :
    lg1 = config['lg1']
    lg2 = config['lg2']
    id_multidoc   = config['id_multidoc']
    distance_type = config['distance_type']
    distance_min  = config['distance_min']
    distance_max  = config['distance_max']

    str1_nb_occ_min = config['str1_nb_occ_min']
    str1_nb_occ_max = config['str1_nb_occ_max']
    str2_nb_occ_min = config['str2_nb_occ_min']
    str2_nb_occ_max = config['str2_nb_occ_max']

    str1_len_min = config['str1_len_min']
    str1_len_max = config['str1_len_max']
    str2_len_min = config['str2_len_min']
    str2_len_max = config['str2_len_max']

    str1_nb_occ_min_rel = config['str1_nb_occ_min_rel']
    str1_nb_occ_max_rel = config['str1_nb_occ_max_rel']
    str2_nb_occ_min_rel = config['str1_nb_occ_min_rel']
    str2_nb_occ_max_rel = config['str1_nb_occ_max_rel']

    t = tf.Tool_file()
    text = t.file_load(path)
    paquets = re.split("\n[ \t]*\n", text)
    lg_wanted = set((lg1, lg2))
    print lg_wanted
    res = []

    for p in paquets : 
      info = p.split("\n")
      if(len(info) != 3) :
        continue
      dist_type, distance_info = info[0].split(" : ")
      if(distance_type != dist_type) :
        continue

      dist, l1, l2 = distance_info.strip().split(" ")
      if(lg_wanted != set((l1, l2)) or float(dist) < distance_min or float(dist) > distance_max) :
        continue

      info_str1, distrib1 = info[1].split(") : ")
      s1, nb_occ1, _ = re.split(" \(([0-9]+)$", info_str1)
      s1 = s1.strip("'")
      nb_occ1 = float(nb_occ1)
      if(nb_occ1 < str1_nb_occ_min or nb_occ1 > str1_nb_occ_max) :
        continue

      info_str2, distrib2 = info[2].split(") : ")
      s2, nb_occ2, _ = re.split(" \(([0-9]+)$", info_str2)
      s2 = s2.strip("'")
      nb_occ2 = float(nb_occ2)
      if(nb_occ2 < str2_nb_occ_min or nb_occ2 > str2_nb_occ_max) :
        continue

      d1 = self.str_distrib2info_distrib(distrib1)
      if(id_multidoc not in d1) :
        continue

      d2 = self.str_distrib2info_distrib(distrib2)
      if(id_multidoc not in d2) :
        continue

      k1 = "str_%s"%(l1)
      k2 = "str_%s"%(l2)
      i = {'score' : dist, l1 : d1, l2 : d2, k1 : s1, k2 : s2}

      kt1 = "str_%s"%(lg1)
      kt2 = "str_%s"%(lg2)

      len_s1 = len(i[kt1])
      if(len_s1 < str1_len_min or len_s1 > str1_len_max) :
        continue

      len_s2 = len(i[kt2])
      if(len_s2 < str2_len_min or len_s2 > str2_len_max) :
        continue

      rel_count_s1 = self.distrib2rel_count(i[lg1], id_multidoc)
      if(rel_count_s1 < str1_nb_occ_min_rel or rel_count_s1 > str1_nb_occ_max_rel) :
        continue

      rel_count_s2 = self.distrib2rel_count(i[lg2], id_multidoc)
      if(rel_count_s2 < str2_nb_occ_min_rel or rel_count_s2 > str2_nb_occ_max_rel) :
        continue

      res.append(i)
    return res

