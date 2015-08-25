#!/usr/local/bin/pythonw
# -*- coding: utf-8 -*-
import os.path
import sys
import getopt
import time
from tools_karkkainen_sanders import *
from rstr_max import *
from string import *
import glob
from align_optparser import opt_parser

def get_equiv_j(i, len1, len2) :
  percent = (i / float(len1))
  j = int(percent * len2)
  return j

def combinations(iterable, r) :
  # combinations('ABCD', 2) --> AB AC AD BC BD CD
  # combinations(range(4), 3) --> 012 013 023 123
  pool = tuple(iterable)
  n = len(pool)
  if r > n :
    return
  indices = range(r)
  yield tuple(pool[i] for i in indices)
  while True:
    for i in reversed(range(r)) :
      if indices[i] != i + n - r:
        break
    else :
      return
    indices[i] += 1
    for j in xrange(i+1, r) :
      indices[j] = indices[j-1] + 1
    yield tuple(pool[i] for i in indices)

def get_root(path_dir) :
    l = path_dir.split("/")
    info = l[-1].split(".")
    d = info[:-2]
    return ".".join(d)
#    d = l[-1][:-7]
  

def dir_lg2dic_contents(path_dir, list_lg) :
  content = {}
  all_subdir = os.path.join(path_dir, '*')
  set_lg = set(list_lg)
  dic_doc_id = {}
  for subdoc in glob.glob(all_subdir) :
    subdoc_id = subdoc.split("/")[-1]
    all_doc   = os.path.join(subdoc, '*')
    dic_lang_content = {}
    abs_path_subdoc  = os.path.abspath(path_dir)
    for path_doc in glob.glob(all_doc) :
      path_dir,filename = os.path.split(path_doc)
      l = filename.split('.')
      lg = l[-2]
      if lg not in list_lg :
        continue
      root_filename = '.'.join(l[:-2])
      if lg not in dic_lang_content :
        dic_lang_content[lg] = {}
      dic_lang_content[lg]
    
      chaine = open(path_doc,'r').read()
      dic_lang_content[lg] = unicode(chaine, 'utf-8', 'replace')
    if set(dic_lang_content.keys()) == set_lg :
#      content[abs_path_subdoc] = dic_lang_content
      content[subdoc] = dic_lang_content
      dic_doc_id[subdoc] = subdoc_id
  return content, dic_doc_id

def dir_lg2dic_contents2(path_dir, list_lg) :
  contents = {}
 
  all_in_dir = os.path.join(path_dir, '*', '*') 
  docs = set()
  dic_doc_id = {}

  for d in glob.glob(all_in_dir) :
    l = d.split("/")
    d = get_root(d)
#    d = l[-1][:-7]
#    i = int(l[-2])
    i = l[-2]
    docs.add(d)
    dic_doc_id[d] = i

  for doc in docs:
    ismulti = True      
    dic_lg = {}
    for lang in list_lg:
      filename = '%s.%s.*'%(doc,lang)
      fg = os.path.join(path_dir,'*',filename)
      fileexists = len(glob.glob(fg))
      ismulti = ismulti and fileexists == 1

    if ismulti == False :
      continue

    contents[doc] = {}

    for lang in list_lg:
      filename = '%s.%s.*'%(doc,lang)
      fg = os.path.join(path_dir,'*',filename)
      chaine = open(glob.glob(fg)[0],'r').read()
      contents[doc][lang] = unicode(chaine, 'utf-8', 'replace')

  return contents,dic_doc_id

def dic_contents2dic_rstr(dic_contents, list_lg) :
  dic_rstr = {}
  for lg in list_lg :
    dic_rstr[lg] = Rstr_max()

  for id_multidoc, dic_lang in dic_contents.iteritems() :
    for lg,content in dic_lang.iteritems() :
      dic_rstr[lg].add_str(content)

  return dic_rstr

def rstr2list_str_sorted(rstr) :
  array_repeated = rstr.go()
  l_info = array_repeated.items()
  l_sort = sorted(l_info,lambda x, y : cmp((y[0][1],y[1][0]), (x[0][1],x[1][0])))
  return l_sort

def dic_rstr_max2dic_str(dic_str, len_int, eff_int, nb_multi_int) :
  dic_res = {}

  for lg,rstr_max in dic_str.iteritems() :
    i = rstr2list_str_sorted(rstr_max)
    dic_res[lg] = [] 
    for k,v in i :
      if not(len_int[0] <= v[0] <= len_int[1]) : # len_int[0] > v[0] or v[0] > len_int[1] :
        continue
      if not(eff_int[0] <= k[1] <= eff_int[1]) : #eff_int[0] > k[1] or k[1] > eff_int[1] :
        continue

      ((id_str, end), nb), (l, start_plage) = (k,v)
      set_id_multi = set()
      for o in xrange(start_plage, start_plage + nb) :
        _, id_multi  = rstr_max.array_suffix[o]
        set_id_multi.add(id_multi)
      nb_diff_multi = len(set_id_multi)

      if not(nb_multi_int[0] <= nb_diff_multi <= nb_multi_int[1]) :#nb_multi_int[0] > nb_diff_multi or nb_diff_multi > nb_multi_int[1] :
        continue

      dic_res[lg].append((k,v))

  return dic_res

def analyse_couple(info_lg1, info_lg2, nb_dim, window_size, score_int, output_file, distance, diff_freq, li) :
  rstr_max1, list_str1, lg1 = info_lg1
  rstr_max2, list_str2, lg2 = info_lg2

  len1 = len(list_str1)
  len2 = len(list_str2)

  mid_window = window_size / 2

  print len1, len2
#  cpt = 0
  for i in xrange(0,len1) :
    if i % 1000 == 0 :
      print '  ', i, '/', len1
#    print "\r", i, '/', len1, 
    ((id_str1, end1), nb1), (l1, start_plage1) = list_str1[i]
    string1 = rstr_max1.array_str[id_str1][end1-l1:end1].encode('utf-8','ignore')
    string1 = string1.replace("\n","$$")
    v1 = vector_empty_list(nb_dim)
    for o1 in xrange(start_plage1, start_plage1 + nb1) :
      offset1, id1  = rstr_max1.array_suffix[o1]
      v1[id1].append(offset1)

    prep1 = print_rep(v1, rstr_max1, li)

    nj = get_equiv_j(i, len1, len2)
    for j in xrange(nj-mid_window, nj+mid_window+1) :
      if(j >= len2 or j < 0) :
        continue

      ((id_str2, end2), nb2), (l2, start_plage2) = list_str2[j]

      if(abs(nb1-nb2) > diff_freq) :
        continue

      v2 = vector_empty_list(nb_dim)
      for o2 in xrange(start_plage2, start_plage2 + nb2) :
        offset2, id2  = rstr_max2.array_suffix[o2]
        v2[id2].append(offset2)

      dist = docdistance(v1,v2)

#      if v2[34] == 0 and v1[34] == 0 :
#        continue

      if(score_int[0] <= dist <= score_int[1]) :
        string2 = rstr_max2.array_str[id_str2][end2-l2:end2].encode('utf-8','ignore')
        string2 = string2.replace("\n","$$")
        prep2 = print_rep(v2,rstr_max2, li)

        print >>output_file, '%s : %.3f %s %s '%(distance, dist, lg1, lg2)
        print >>output_file, '\'%s\' (%d) : %s'%(string1,  nb1,  prep1)
        print >>output_file, '\'%s\' (%d) : %s'%(string2,  nb2,  prep2)
        print >>output_file, ' '

def vector_empty_list(nb_dim) :
  return [[] for _ in xrange(nb_dim)]

def docdistance(v1,v2) :
  nb_dim = len(v1)
  sum_diff = sum_all = 0.
  for i in xrange(nb_dim) :
    sum_diff += abs(len(v1[i]) - len(v2[i]))
    sum_all  += len(v1[i]) + len(v2[i])
  return sum_diff / sum_all

def print_rep(v, rstr_max, li) :
  res = []
  for i,list_app in enumerate(v) :
    len_doc = len(rstr_max.array_str[i])
    ni = li[i]
    for offset in list_app :
      relative_offset = (float(offset) / float(len_doc)) * 100.
      print_offset = min(99.99,float('%.2f'%relative_offset))
#      res.append('%s:%.2f'%(ni,relative_offset))
      res.append('%s:%s'%(ni,print_offset))
  return " ".join(res)

def main(args):
  parser = opt_parser()
  (opt_options, opt_args) = parser.parse_args(args)

  output_filename = opt_options.outputfile
  output_file = open(output_filename,'w')

  print >>output_file, "cmd :: [python interpret.] corpusalign.py %s"%(" ".join(args))
  s = time.clock()

  langs = opt_options.languages
  dirname = os.path.join(opt_options.corpus,'')

  multidocs,dic_doc_id = dir_lg2dic_contents(dirname, langs)
#  print multidocs.keys()
#  print multidocs['celex_IP-05-1068'].keys()
#  print dic_doc_id
#  exit(0)

  li = [dic_doc_id[id_multidoc] for id_multidoc,_ in multidocs.iteritems()]

  for id_multidoc,list_lg in multidocs.iteritems() :
    idd = dic_doc_id[id_multidoc]
    for lg in list_lg.keys() :
      print >>output_file, '/%s/*.%s.*'%(idd,lg)
#      print >>output_file, '/%s/%s.%s.xml'%(idd,id_multidoc,lg) #if call to dir_lg2dic_contents2
  print >>output_file, ''

  nb_dim = len(multidocs.keys())

  dic_rstr = dic_contents2dic_rstr(multidocs, langs)

  opt_len = opt_options.length
  len_int = (int(opt_len[0]), int(opt_len[1]))

  opt_freq = opt_options.relative_frequency
  eff_int = (int(opt_freq[0]), int(opt_freq[1]))

  opt_nb_multi = opt_options.nb_multidoc_occur
  nb_multi_int = (int(opt_nb_multi[0]), int(opt_nb_multi[1]))

  dic_str = dic_rstr_max2dic_str(dic_rstr, len_int, eff_int, nb_multi_int)

#  for lg, list_info_str in dic_str.iteritems() :
#    print lg, len(list_info_str)
  tt = time.clock() - s
  print
  print "prepare : %f"%(tt)

  s = time.clock()

  score = opt_options.score
  score_int = (float(score[0]), float(score[1]))
  distance = opt_options.distance
  window_size = opt_options.window_size
  diff_freq = opt_options.difference_frequency
  for i in combinations(dic_str.keys(), 2) :
    info_lg1 = (dic_rstr[i[0]], dic_str[i[0]], i[0])
    info_lg2 = (dic_rstr[i[1]], dic_str[i[1]], i[1])
    analyse_couple(info_lg1, info_lg2, nb_dim, window_size, score_int, output_file, distance, diff_freq, li)

  tt = time.clock() - s
  print
  print "compare all : %f"%(tt)

  output_file.close()

if __name__ == "__main__":
    main(sys.argv[1:])
