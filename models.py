# -*- coding: utf-8 -*-
"""
Created on Sat Jul 31 15:40:28 2021

@author: hugo_
"""

import struct
from obj import Obj

def char(c):
  # char
  return struct.pack('=c', c.encode('ascii'))

def word(w):
  # short
  return struct.pack('=h', w)

def dword(w):
  # long
  return struct.pack('=l', w)


def color(r, g, b):
  return bytes([b, g, r])

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)


class Renderer(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.current_color = WHITE
    self.clear()

  def clear(self):
    self.framebuffer = [
      [BLACK for x in range(self.width)]
      for y in range(self.height)
    ]
  
  def write(self, filename):
    f = open(filename, 'bw')

    # file header 14
    f.write(char('B'))
    f.write(char('M'))
    f.write(dword(14 + 40 + 3*(self.width*self.height)))
    f.write(dword(0))
    f.write(dword(14 + 40))

    # info header 40
    f.write(dword(40))
    f.write(dword(self.width))
    f.write(dword(self.height))
    f.write(word(1))
    f.write(word(24))
    f.write(dword(0))
    f.write(dword(3*(self.width*self.height)))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))
    
    # bitmap
    for y in range(self.height):
      for x in range(self.width):
        f.write(self.framebuffer[y][x])

    f.close()
    
 
     
              
  
  def render(self):
    self.write('a.bmp')

  def point(self, x, y, color= None):
    self.framebuffer[y][x] = color  or self.current_color
    
  def glLine(self,x0,y0,x1,y1):
      
   dy = abs(y1-y0)
   dx = abs(x1- x0)
       
        
   s = dy > dx
        
   if s:
    x0,y0 = y0,x0
    x1,y1= y1,x1
            
    dy = abs(y1 - y0)
    dx = abs(x1 - x0)
        # m = dy/dx * dx
        
        
   offset = 0 * 2* dx
   tr = 0.5 * 2 * dx
   y = y0
        
   points = []
   for x in range (x0,x1):
    if s:
        points.append((y,x))
    else:
        points.append((x,y))
                
    offset += (dy/dx) * 2 * dx
    if offset >= tr:
     y+=1 if y0 < y1 else -1
     tr +=1 * 2  * dx
     
   for point in points:
       r.point(*point)
    

    
  def load(self, filename, translate, scale):
    model = Obj(filename)
    
    for face in model.faces:
      vcount = len(face)
      for j in range(vcount):
        f1 = face[j][0]
        f2 = face[(j + 1) % vcount][0]

        v1 = model.vertices[f1 - 1]
        v2 = model.vertices[f2 - 1]

        x1 = round((v1[0] + translate[0]) * scale[0])
        y1 = round((v1[1] + translate[1]) * scale[1])
        x2 = round((v2[0] + translate[0]) * scale[0])
        y2 = round((v2[1] + translate[1]) * scale[1])

        self.glLine(x1, y1, x2, y2)
      
    


r = Renderer(800, 600)
r.load('./stormtrooper.obj' ,[4,1],[100,100])



r.render()