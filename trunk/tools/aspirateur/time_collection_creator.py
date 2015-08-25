#!/usr/bin/env python
# -*- coding: utf-8 -*-


from collection_creator_options import time_build_argparse  
import datetime
import time
import re
import os
import subprocess
import tools as tls

def date2str(date) :     
  str_date = str(date).strip('()')
  return str_date

def subPeriod2str(subPeriod) :
  start = re.sub('-',',',str(subPeriod[0]))
  end = re.sub('-',',',str(subPeriod[1]))
  return start,end

def list_lg2str(options) :
  list_lg = options.languages
  str_lg = ",".join(list(list_lg))
  if len(str_lg) == 65 :
    return 'all'
  else :
    return str_lg

def define_subPeriod(options) :
  window = options.window
  step = options.step
  period = options.period
  start,end = tls.starting_ending_date(period,options.input_dir)
  (syyyy,smm,sdd) = start
  (eyyyy,emm,edd) = end
  startPer = datetime.date(int(syyyy),int(smm),int(sdd))
  endPer = datetime.date(int(eyyyy),int(emm),int(edd))
  list_subPeriod = []
  subPeriod = []
  w = datetime.timedelta(window)
  s = datetime.timedelta(step)
  if startPer+w >=endPer:       # Si la fenêtre de temps demandée est supérieure à ma période, ma sous-période = ma période
    subPeriod = [startPer,endPer]
    list_subPeriod.append(subPeriod)
  else:                         # sinon
    startSubPer = startPer      # d'abord le start de ma sous-période équivaut à celui de la période
    endSubPer = startSubPer+w   # et le end de ma sous-période équivaut au start de ma sous-période + la taille de la fenêtre
    subPeriod = [startSubPer,endSubPer]
    list_subPeriod.append(subPeriod)  # j'ajoute la sous-période à ma liste
    while startSubPer+w < endPer :    # tant que la sous-période demandée ne dépasse pas la fin de ma période  
      startSubPer+=s
      if startSubPer>endPer:
        break
      endSubPer = startSubPer+w
      subPeriod = [startSubPer, endSubPer]
      list_subPeriod.append(subPeriod)
      if endSubPer+s >=endPer: # ou == si on ne veut pas d'une période de taille inf à la fenêtre
        subPeriod = [startSubPer+s,endPer]
        list_subPeriod.append(subPeriod)   
        break 
  return list_subPeriod  

def create_command(options,subPeriod) :
  lg = '-l %s'%list_lg2str(options)
  booleen = '-b %s'%options.booleen
  start,end = subPeriod2str(subPeriod)
  period = '-p %s %s'%(start,end)
  subPer = '%s_%s'%(subPeriod[0],subPeriod[1])
  output_dir = '-o %s'%(os.path.join(options.output_dir,subPer))
  input_dir = '-d %s'%options.input_dir
  if options.manifest :
    manifest = '-m'
  else :
    manifest = ''
  if options.clean :
    clean = '-c'
  else :
    clean = ''
  command = 'python collection_creator.py %s %s %s %s %s %s %s'%(input_dir,output_dir,lg,booleen,period,manifest,clean)
  print 'commande ::',command
  os.system(command)

def create_time_collection(options):
  list_subPeriod = define_subPeriod(options)
  for subPeriod in list_subPeriod :
    create_command(options,subPeriod)  

if __name__ == "__main__" :
  parser = time_build_argparse()
  opt = parser.parse_args()
#  list_lg = opt.languages
#  collection = opt.output_dir
#  directory = opt.input_dir
#  booleen = opt.booleen
#  period = opt.period
#  step = opt.step
#  window = opt.window
#  clean = opt.window
#  manifest = opt.window
  res = create_time_collection(opt)
