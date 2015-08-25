import UserList
#import numpy
import tool_misc as tm
from array import array


class DistMatrix(UserList.UserList):
  def __init__(self, l1, l2) :
    self.k1 = l1
    self.k2 = l2
    self._width = len(l1)
    self._height = len(l2)
    self.data = []
#    for _ in xrange(self._height) :
#      self.data.append(array('f',[0. for _ in xrange(self._width)]))

    self.data = [[0.0 for _ in xrange(self._width)]
                      for _ in xrange(self._height)]

  def set(self, x, y, value):
    assert(0 <= x < self._width)
    assert(0 <= y < self._height)
    self.data[y][x] = value

  def get(self, x, y):
    assert(0 <= x < self._width)
    assert(0 <= y < self._height)
    return self.data[y][x]

  def convert2pickle(self) :
    dic = {
      'k1' : self.k1, '_width' : self._width, 
      'k2' : self.k2, '_height' : self._height,
      'data' : self.data
    }
    return dic

  def from_pickle(self, dic_pickle) :
    self.k1 = dic_pickle['k1']
    self.k2 = dic_pickle['k2']
    self._width = dic_pickle['_width']
    self._height = dic_pickle['_height']
    self.data = dic_pickle['data']

#  def convert2numpy(self) :
#    matrix2 = []
#    for line in self.data :
#      matrix2.append(list(line))
#    a = numpy.array(matrix2,"float32")
#    return a

class Dotplot(DistMatrix) :
  def OLD_get_list_i(self,l,x) :
    res = []
    for i,(m,a) in enumerate(l) :
      if(m <= x < a) : res.append(i)
      elif x < m : return res
    return res

#  def get_i(self, l, val, step) :
#    return int(val / step)


  def get_list_i(self, l, val, step) :
#    print l
#    1/0
#    i =  tm.dicho_find_inter(l,val)
#    i2 = self.get_i(l, val, step)
    i = int(val / step)
    r = [i]
    cpt = i-1
    while(cpt > 0 and l[cpt][0] <= val <= l[cpt][1]):
      r.append(cpt)
      cpt -= 1
    cpt = i+1
    while(cpt < len(l) and l[cpt][0] <= val <= l[cpt][1]):
      r.append(cpt)
      cpt += 1
    return r

  def inc_dot(self,x,y,cstep) :
    li = self.get_list_i(self.k1, x, cstep[0])
    lj = self.get_list_i(self.k2, y, cstep[1])
    print li
    print lj
    for i in li :
      for j in lj :
        self.data[i][j] += 1

  def __str__(self) :
    return str(self.data)

