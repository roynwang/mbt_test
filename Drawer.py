import svgwrite
from Edge import *

class Drawer(object):
	def __init__(self, graph):
		#init start positin and delta constant
		self.x = 800
		self.y = 100
		self.delta = 150
		self.r  = 50
		self.graph = graph

		self.arcs = []
		self.circles = []
		self.dwg = svgwrite.Drawing("test.svg")

		#add marker
		self.marker = self.dwg.marker(insert=(3,2), size=(10,10), orient='auto')
		arrow = self.dwg.path(d=("M0,0 L4,2 0,4"), stroke_width=1, stroke='black', fill='none')
		self.marker.add(arrow)
		self.dwg.defs.add(self.marker)
	
	def genstate(self, id, x, y, tip = '', fill='white'):
		g = self.dwg.g(id=id, fill='black')
		#append the circle
		cir = self.dwg.circle(center=(x, y), r=self.r, stroke='blue',stroke_width=3, fill=fill)
		text = self.dwg.text('S'+str(id), insert=(x,y))
		cir.set_desc(tip)
		g.add(cir)
		g.add(text)
		return g

	def gen(self):
		id = 0
		for vex in self.graph.vertexes:
			fill = 'white'
			if vex.postype == 1:
				fill = 'grey'
			sta = self.genstate(id, self.x, self.y + id*self.delta, str(vex), fill)
			self.circles.append(sta)
			#self.y += self.delta
			id += 1
		for edge in self.graph.edges:
			if edge.status == 1:
				continue
			starty = self.y  + self.graph.vertexes.index(edge.start)*self.delta
			endy = self.y + self.graph.vertexes.index(edge.end)*self.delta
			cx1=cx2=x=0
			cy1 = starty
			cy2 = endy

			#if starty < endy => arc at right side
			if starty < endy :
				x = self.x + self.r
				#arc = (mx, starty c x+50,starty x+50, endy x,endy)
			#else => arc at left side
			elif starty > endy :
				x = self.x - self.r
			else:
				continue
			#use endy - starty to controll the arc heigh
			cx1 = cx2 = x + 0.5*(endy - starty)
			arc = self.dwg.path(d=("M {0},{1} C {2},{3} {4},{5} {6},{7}".format(x,
				starty, cx1,starty, cx2,endy,x,endy)),stroke_width=5, stroke='black',
				fill='none')
			arc.set_desc(edge.action.name)
			arc['marker-end']= self.marker.get_funciri()
			self.arcs.append(arc)
	
	def save(self):
		for circle in self.circles:
			self.dwg.add(circle)
		for arc in self.arcs:
			self.dwg.add(arc)
		self.dwg.save()
		


if __name__ == '__main__':
	dwg = svgwrite.Drawing('test.svg', profile='tiny')
	dwg.add(dwg.line((0, 0), (100, 100), stroke=svgwrite.rgb(10, 10, 16, '%')))
	sharps = dwg.add(dwg.g(id='shapes', fill='red'))
	cir = dwg.circle(center=(400, 100), r=50, stroke='blue',stroke_width=5, fill='white')
	cir.set_desc("test", "sdfsdfas")
	sharps.add(cir)
	sharps.add(dwg.text('Test', insert=(400, 100)))
	dwg.save()
