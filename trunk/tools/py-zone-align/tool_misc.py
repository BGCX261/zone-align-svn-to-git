#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

def pop_val(l,val) :
  length = len(l)
  for i in xrange(length) :
    k = length - i - 1
    if(l[k] == val) :
      return l[:k] + l[k+1:]
  return l

def pop_val_id(l, val) :
  length = len(l)
  for i in xrange(length) :
    k = length - i - 1
    if(l[k] == val) :
      return k
  return -1

def dict_append(d, k, v) :
  if(d.has_key(k)) :
    d[k].append(v)
  else :
    d[k] = [v]

def drange(start, stop, step) :
  r = start
  while r < stop :
    yield r
    r += step

def dicho_find(l, val) :
  start = 0
  end = len(l)
  find = False

  while find == False and start <= end:
    _, mid = math.modf(start + ((end - start) / 2))
    mid = int(mid)
    if(l[mid] == val) :
      find = True
    elif val > l[mid] :
      start = mid + 1
    else :
      end = mid - 1

  return mid

def dicho_find_inter(l, val) :
  start = 0
  end = len(l)
  find = False

  while find == False and start <= end:
    _, mid = math.modf(start + ((end - start) / 2))
    mid = int(mid)
    if(l[mid][0] <= val <= l[mid][1]) :
      find = True
    elif val > l[mid][1] :
      start = mid + 1
    elif val < l[mid][0] :
      end = mid - 1

  return mid
