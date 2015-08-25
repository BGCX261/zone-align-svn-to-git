#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os

import tools

def content2link(content) :
  pattern_true_content = '<link[^>]+?>'
  re_comp = re.compile(pattern_true_content, re.DOTALL | re.MULTILINE)
  res = re_comp.findall(content)
  return res

def create_list_link(content) :
  list_link_ok = []
  list_link = content2link(content)
  for link in list_link:
    pattern_comp = re.compile('media[\s]*=[\s]*"([^\s]+)"')
    pattern = re.search(pattern_comp,link)
    if pattern : 
      if pattern.group(1) != "print" :
        list_link_ok.append(link) 
    else : 
      list_link_ok.append(link) 
  return list_link_ok

def create_css_list(content) :
  list_css_filename = []
  list_link = create_list_link(content)
  pattern_comp = re.compile('href[\s]*=[\s]*"(/rapid/)?([^\s]+)"')
  for link in list_link :    
    res = pattern_comp.search(link)
    if res :
      if re.match('^http',res.group(2)) :
        url = '%s'%(css_filename) 
      else :
        url = 'http://europa.eu/rapid/%s'%(res.group(2))
      list_css_filename.append(url) 
  return list_css_filename

def get_style_balise_content(content) :
  pattern_true_content = u'<style.+?</style>'
  re_comp = re.compile(pattern_true_content, re.DOTALL | re.MULTILINE)
  style = re_comp.findall(content)
  return style

def construct_css(content,subdirectory,date,id_doc_xml,lg) : 
  list_css_filename = create_css_list(content)
  (dd,mm,yyyy) = date
  filename = '%d-%0.2d-%0.2d_celex_%s.%s.css'%(int(yyyy),int(mm),int(dd),id_doc_xml,lg)  
  path_css = os.path.join(subdirectory,filename)
  f = open(path_css,'w')
  style = get_style_balise_content(content)
  print >>f, style
  for url_css in list_css_filename :
    content_css = tools.url2content(url_css)
    print >>f, content_css
  f.close()
  return filename

