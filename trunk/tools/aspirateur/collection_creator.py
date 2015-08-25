#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import glob 
import shutil
from collection_creator_options import collection_build_argparse
import tools
import clean_bs as cb

def path2lg(path) :
  pattern = '(.*celex_IP-[0-9]{2}-[0-9]{,4})\.([a-z]{2}).html'
  find = re.search(pattern, path)
  return find.group(2)

#def path2info(path) :
#  pattern = '(.*celex_IP-[0-9]{2}-[0-9]{,4})\.([a-z]{2}).html'
#  find = re.search(pattern, path)
#  d = {'lg' : find.group(2), 'id' : find.group(1)}
#  return d

def getDicMultidoc(directory,list_lg,start,end) :
  yStart, mStart, dStart = start
  yEnd,   mEnd, dEnd   = end
  pattern = '(.*celex_IP-[0-9]{2}-[0-9]{,4})\.([a-z]{2}).html'
  pattern_compiled = re.compile(pattern)
  d = {}
  liste_days = getListdays(start,end)
  liste_months = getListmonths(start,end)
  cpt = 0
  for y in xrange(int(yStart), int(yEnd)+1) :
    str_y = '%0.4d'%(y)
    start_month = mStart if (y == yStart) else 1
    end_month = mEnd if (y == yEnd) else 12
    start_month,end_month = liste_months[cpt]
    cpt += 1
    cpt_days = 0
    for m in xrange(start_month, int(end_month)+1) :
      str_m = '%0.2d'%(m)
      start_day = dStart if (y == yStart) else 1
      end_day = dEnd if (y == yEnd) else 31
      start_day,end_day = liste_days[cpt_days]
      cpt_days += 1
      for day in xrange(start_day, int(end_day)+1) :
        str_day = '%0.2d'%(day)
        glob_file = '*%s-%s-%s_*.html'%(str_y,str_m,str_day)
        path_subdir = os.path.join(directory, str_y, str_m, glob_file)
        for path in glob.glob(path_subdir):
          filename = os.path.split(path)[-1]  
          find = pattern_compiled.search(filename)
          if find.group(1) not in d :
            d[find.group(1)] = {}
          if find.group(2) in list_lg : 
            d[find.group(1)][find.group(2)] = path
  return d

def getListdays (start,end) :
  yStart, mStart, dStart = start
  yEnd,   mEnd, dEnd   = end
  liste_days = []
  if mStart==mEnd:
    days = (dStart,dEnd)
    liste_days.append(days)
  else:
    days = (dStart,31)
    liste_days.append(days)
    for month in xrange(mStart+1,mEnd):
      days = (1,31)
      liste_days.append(days)
    days_end = (1,dEnd)
    liste_days.append(days_end)
  return liste_days

def getListmonths (start,end) :
  yStart, mStart, dStart = start
  yEnd,   mEnd,   dEnd   = end
  liste_months = []
  if yStart == yEnd:
    months = (mStart,mEnd)
    liste_months.append(months)
  else:
    months = (mStart,12)
    liste_months.append(months)
    for year in xrange(yStart+1,yEnd):
      months = (1,12)
      liste_months.append(months)
    months_end = (1,mEnd)
    liste_months.append(months_end)
  return liste_months

def createListMd(dic,list_lg) :
  list_path = []
  for ip,lginfo in dic.iteritems() :
    if len(lginfo.keys()) != len(list_lg) :
      continue
    for lg in list_lg :
      list_path.append(lginfo[lg])
  return list_path

def createListDoc(dic) :
  list_path = [path for path in [lg_info for lg_info in dic.values()]]
#  for _,lginfo in dic.iteritems() :
#    for _,path in lginfo.iteritems() :
#      list_path.append(path)
  return list_path

def copy_doc(list_path,options) :   
  dic_newpath = {}
  for path in list_path :
    dirs,filename = os.path.split(path)
    directory,yyyy,mm = dirs.split(os.sep)[-3:]
    subdirectory = tools.create_dir(opt.output_dir,yyyy,mm) # check if create dir
    rootsubdir = os.sep.join(subdirectory.split(os.sep)[-3:])
    newpath = os.path.join(subdirectory,filename)  
    newpathmanifest = os.path.join(rootsubdir,filename)

    lg = path2lg(path)
    if lg not in dic_newpath :
      dic_newpath[lg] = []
    dic_newpath[lg].append(newpathmanifest)

    filename_css = '.'.join(filename.split('.')[:-1])+'.css'
    newpath_css = os.path.join(subdirectory,filename_css)
    path_css = os.path.join(dirs,filename_css)
    if options.clean :
      clean_html(path, newpath)
    else :
      shutil.copyfile(path, newpath)
      shutil.copyfile(path_css, newpath_css)  
  return dic_newpath  
    
def define_mode(booleen,list_lg,dic) :
  if (booleen == 'or') :
    list_path = createListDoc(dic)
  else : 
    list_path = createListMd(dic, list_lg)
  return list_path


def create_manifest(dic_newfilepath, start, end, options) :
  yStart, mStart, dStart = start
  yEnd,   mEnd,   dEnd   = end
  for lg, list_newfilepath in dic_newfilepath.iteritems() :
    manifest_file = 'manifest_%0.4d-%0.2d-%0.2d_%0.4d-%0.2d-%0.2d.%s.txt'%(yStart, mStart, dStart, yEnd, mEnd, dEnd, lg)
    root_dir = os.path.split(options.output_dir)[0]
    manifest_path = os.path.join(root_dir,manifest_file)
    f = open(manifest_path,'w')
    for path in list_newfilepath :
      #abs_path = os.path.abspath(path)
      print >>f, path
    f.close()

def clean_html(path_in, path_out) :
  f_read = open(path_in, 'r')
  str_file = f_read.read()
  l = cb.clean_html(str_file)
  f_write = open(path_out, 'w')
  for s in l :
    print >>f_write, s.encode('utf-8')
  f_write.close()
 
def create_collection(options) :
  start,end = tools.starting_ending_date(options.period, options.input_dir)
  dic = getDicMultidoc(options.input_dir, options.languages, start, end)
  list_path = define_mode(options.booleen, options.languages, dic)
  dic_path = copy_doc(list_path, options)
  if options.manifest and len(list_path) > 0 : 
    create_manifest(dic_path, start, end, options)

##
# deprecated
##

#  clean_str_unicode = unicode(str_file, 'utf-8')
#  f_read.close()
#  clean_str_unicode = re.sub("</?[^>]+>", "", clean_str_unicode, flags=re.U, count=0)
#  clean_str_unicode = re.sub("\r*", "", clean_str_unicode, count=0)
#  clean_str_unicode = re.sub("([\s]*\n[\s]*){2,}", "", clean_str_unicode, count=0, flags=re.U)
#  clean_str = clean_str_unicode.encode('utf-8', 'replace')
#  f_write = open(path_out, 'w')
#  print >>f_write, clean_str
#  f_write.close()

#def clean_doc(filepath,newfilepath) :
#  f_read = open(filepath, 'r')
#  str_file = f_read.read()
# str_unicode = unicode(str_file, 'utf-8')
# f_read.close()
# clean_str_unicode = re.sub('[\r\n\s]*</body>[\s]*</html>[\r\n\s]*','', str_unicode)
# clean_str_unicode = re.sub('[\r\n\s]*<p class=".*?">','\r<p class=".*?">', clean_str_unicode)
# clean_str_unicode = re.sub('[\r\n\s]*<p>','\r<p>', clean_str_unicode)
# clean_str_unicode = re.sub('[\r\n\s]*<P>','\r<P>', clean_str_unicode)
# clean_str_unicode = re.sub('<[/]?H\w{1}>[\n\r]*','', clean_str_unicode)
# clean_str_unicode = re.sub('[\r\n\s]*<(span|td|col) class=".*?">','', clean_str_unicode)
# clean_str_unicode = re.sub('<(A|a) (HREF|href|NAME|name)=.*?</(A|a)>','', clean_str_unicode)
# pattern = re.compile('<img style=".*?"/>', re.MULTILINE|re.DOTALL)
# clean_str_unicode = pattern.sub("", clean_str_unicode)
# pattern2 = re.compile('<div class="[^<]+?</div>', re.MULTILINE|re.DOTALL)
# clean_str_unicode = pattern2.sub("", clean_str_unicode)
# clean_str_unicode = re.sub('<div class="[^<]+?</div>','', clean_str_unicode)
# clean_str_unicode = re.sub('</(span|SPAN|p|P)>','', clean_str_unicode) 
# clean_str_unicode = re.sub('<[/]?(B|I|UL|U|SUP|TD|TR|LI|ul|li|tr|sup|tbody|colgroup).*?>','', clean_str_unicode)
# clean_str_unicode = re.sub('[\n]*(</.*?)?</(table|TABLE)>','', clean_str_unicode)
# clean_str_unicode = re.sub('[\n]*<(table|TABLE).*?=.*?>','', clean_str_unicode)
# clean_str_unicode = re.sub('[\r\n\s]*<p class=".*?">','\r', clean_str_unicode)
# clean_str_unicode = re.sub('[\r\n\s]*<(P|p)>','\n', clean_str_unicode)
# clean_str = clean_str_unicode.encode('utf-8', 'replace')
# f_write = open(newfilepath, 'w')
# print newfilepath
# print >>f_write, clean_str
# f_write.close()

if __name__ == "__main__" :
  parser = collection_build_argparse()
  opt = parser.parse_args()
  create_collection(opt)
