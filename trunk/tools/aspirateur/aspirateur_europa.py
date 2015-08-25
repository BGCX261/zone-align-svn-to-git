#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import math
import time
import random
import os

import tools
import lib_style_sheet as lss
from aspirateur_options import build_argparse

def check_sleep(cpt) :
  sleep = 1. 
  delta_sleep2 = sleep * 0.2
  delta_sleep1 = sleep * 0.1
  max_doc = 500
  delta_doc = max_doc * 0.2
  if cpt <= random.uniform(max_doc-delta_doc,max_doc+delta_doc) :  
    sec = random.uniform(sleep - delta_sleep1, sleep + delta_sleep1)
  else :
    sec = random.uniform(sleep - delta_sleep2, sleep + delta_sleep2)    
    cpt = 0
  time.sleep(sec)
  return cpt

def content2date(content) : 
  clean_html = re.sub(u'&nbsp;', ' ', content) 
  pattern = 'Date:\s*((\d{2})/(\d{2})/(\d{4}))'
  re_comp = re.compile(pattern,re.I)
  res = re_comp.search(clean_html)
  return res.group(2), res.group(3), res.group(4)

def cut_content(content) :
  pattern_true_content = '</div>[\s]+</div>[\s]+<div id=.*?(<p.*)</div>[\s]+<style>'
  re_comp = re.compile(pattern_true_content, re.I |re.DOTALL | re.MULTILINE)
  res = re_comp.search(content)
  return res.group(1)

def entry2code(entry) :  #entry = contenu de la page de résultats du moteur
  pattern = '<span class="reference">(IP/(\d{2})/(\d{1,4}))'
  re_comp = re.compile(pattern,re.I)
  res = re_comp.search(entry)
  ip_url = 'IP-%s-%s'%(res.group(2), res.group(3))
  ip_doc = 'IP/%s/%s'%(res.group(2), res.group(3))
  return ip_url, ip_doc

def get_entry(content):
  pattern = '<tr class="[^"]+">(.*?)</tr>'
  re_comp = re.compile(pattern, re.DOTALL | re.MULTILINE)
  pattern_href = 'href="(/rapid/press-release_[^"]+)"' 
  href_comp = re.compile(pattern_href)
  list_entry = []
  pattern_url = ".*_([^_]+).htm"
  url_comp = re.compile(pattern_url)
  for e in re_comp.findall(content) :
    l = href_comp.findall(e)
    info = {}
    info['lg'] = {}
    info['date'] = content2date(e)
    info['ip'] = entry2code(e)
    for str_ip in l :
      lg = url_comp.search(str_ip).group(1)
      url = 'http://europa.eu%s'%(str_ip)
      info['lg'][lg] = url
    list_entry.append(info)
  return list_entry

def construct_list_lg(list_lg) :
  str_lg = ""
  for lg in list_lg :
    str_lg += "&language=%s"%(lg)
  return str_lg

def construct_urlpage(start_date, end_date, list_lg, nbPage) :   # à partir de la page 1 des résultats du moteur Europa
  syyyy, smm, sdd = start_date
  eyyyy, emm, edd  = end_date
  strLg = construct_list_lg(list_lg)
  baseUrl = 'http://europa.eu/rapid/search-result.htm?dateRange=period&format=HTML&type=IP&size=50&locale=FR'
  page = 'page=%d'%(nbPage)
  fromDate = 'fromDate=%0.2d%%2F%0.2d%%2F%d'%(sdd,smm,syyyy)
  toDate = 'toDate=%0.2d%%2F%0.2d%%2F%d'%(edd,emm,eyyyy)
  url = '%s&%s&%s&%s%s'%(baseUrl,page,fromDate,toDate,strLg)
  return  url

def compute_nbpage(content) :     #sur 1ère page du moteur de recherche Europa
  pattern = '<span class="pagebanner">(Documents 1 à 50 de )?(.*?)( Documents trouvés)?</span>' 
  res = re.search(pattern, content,re.I|re.U)
  total = res.group(2)
  nb_doc = int(total.strip().replace(',','')) 
  return math.ceil(float(nb_doc)/50.)

def init_crawl(start_date, end_date, list_lg) :
  url = construct_urlpage(start_date, end_date, list_lg, 1)
  content = tools.url2content(url)
  nb_pages = compute_nbpage(content)
  return int(nb_pages)

#def crawl(start_date, end_date, list_lg,directory) :
def crawl(options) :
  list_lg = options.languages
  start_date, end_date = starting_ending_date(options.period)
  directory = options.output_dir
  nb_pages = init_crawl(start_date, end_date, list_lg)

  cpt_done = 0
  for nb in xrange(1, nb_pages+1) :
    url = construct_urlpage(start_date, end_date, list_lg, nb)
    content = tools.url2content(url)
    list_entry = get_entry(content)
    for e in list_entry :
      cpt_done += 1
      cpt_done = check_sleep(cpt_done)
      (code_url, code_document) = e['ip']
      for lg in list_lg :
        if lg not in e['lg'] :
          continue
        if options.verbose :
          print '/'.join(e['date']), code_document, lg 
        url = e['lg'][lg]
        content = tools.url2content(url)          
        process(content, code_url, directory, lg, e['date'], options)
          
def file_path(date,code_url,directory,lang) :
  (dd,mm,yyyy)= date
  subdirectory = tools.create_dir(directory,yyyy,mm) # check if create dir
  filename = '%d-%0.2d-%0.2d_celex_%s.%s.html'%(int(yyyy), int(mm), int(dd), code_url,lang)
  filepath = os.path.join(subdirectory,filename)
  return filepath

def process(content, code_url, directory, lang, date, options) :   #récupération et stockage des communiqués
  try :
    content_cut = cut_content(content)
  except :
    if options.log != '' :
      logline = '%s %s'%(code_url, date)
      f = open(options.log, 'a')
      print >>f, logline
      f.close()
    return
  (dd,mm,yyyy)= date
  filepath = file_path(date, code_url, directory, lang)
  subdirectory = tools.create_dir(directory, yyyy, mm) # check if create dir
  filename_css = lss.construct_css(content, subdirectory, date, code_url, lang)
  tag_document_open = '''<html>
  <head>
  <meta http-equiv="content-type" content="text/html;charset=utf-8"/>
  <link href="%s" type="text/css" rel="stylesheet">
  <meta name="Language" content="%s" />
  <meta name="celex" content="%s" />
  </head>
  <body>
'''%(filename_css,lang, code_url)
  tag_document_close = '''
  </body>
</html>'''
  doc = '%s%s%s'%(tag_document_open,content_cut,tag_document_close)
  f = open(filepath,'w')
  print >>f, doc
  f.close()

def starting_ending_date(period) :
  if period[0] > period[1] :
    period[0], period[1] = period[1], period[0]
  return period[0], period[1]

if __name__ == "__main__" :
  parser = build_argparse()
  options = parser.parse_args()

  if options.log != '' :
    f = open(options.log, 'a')
    print >>f, 'code_url date'
    f.close()

  crawl(options)
