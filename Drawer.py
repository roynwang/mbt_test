import svgwrite
from Edge import *

class Drawer(object):
	def __init__(self, graph):
		#init start positin and delta constant
		self.x = 300
		self.y = 0
		self.delta = 150
		self.r  = 50
		self.graph = graph

		self.arcs = []
		self.circles = []
		self.dwg = svgwrite.Drawing("test.svg",size=("100%","150%"), viewBox=('0,0,1900,900'))

		#add marker
		marker = self.dwg.marker(insert=(3,2), size=(10,10), orient='auto')
		arrow = self.dwg.path(d=("M0,0 L4,2 0,4"), stroke_width=1, stroke='black', fill='none')
		marker.add(arrow)
		self.dwg.defs.add(marker)
		self.marker = marker.get_funciri()

		#add linear gradient
		lgcw = svgwrite.gradients.LinearGradient(("0%","0%"),("0%","100%"))
		lgcw.add_stop_color("0%","grey",0.7)
		lgcw.add_stop_color("100%","black",1)
		self.dwg.defs.add(lgcw)
		self.lgcw = lgcw.get_paint_server()

		lgacw = svgwrite.gradients.LinearGradient(("0%","100%"),("0%","0%"))
		lgacw.add_stop_color("0%","grey",0.7)
		lgacw.add_stop_color("100%","black",1)
		self.dwg.defs.add(lgacw)
		self.lgacw = lgacw.get_paint_server()
	
	def genstate(self, id, x, y, tip = '', fill='white'):
		g = self.dwg.g(id=id, fill='black')
		#append the circle
		cir = self.dwg.circle(center=(x, y), r=self.r, stroke='blue',stroke_width=3, fill=fill)
		text = self.dwg.text('S'+str(id), insert=(x,y))
		cir.set_desc(tip)
		g.add(cir)
		g.add(text)
		return g

	def gen(self, path = None):
		id = 0
		if path is None:
			path = self.graph.edges
		vexes = self.graph.edges_to_vexes(path)
		for vex in vexes:
			fill = 'white'
			if vex.postype == 1:
				fill = 'grey'
			sta = self.genstate(id, self.x, self.y + id*self.delta, str(vex), fill)
			self.circles.append(sta)
			#self.y += self.delta
			id += 1
		for edge in path:
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
			get_desc = lambda x: (x is None and 'None') or str(x)
			arc.set_desc(str(get_desc(edge.action)))
			arc['marker-end']= self.marker
			if endy > starty :
				arc['stroke'] = self.lgcw
			else:
				arc['stroke'] = self.lgacw
			self.arcs.append(arc)
	
	def save(self, vertical = 0):
		#rot = "0degree";
		#if vertical == 0:
		#	rot = "rotate(-90, 800, 800)"
		g = self.dwg.g(id='fsm')
		#g['transform'] = rot
		for circle in self.circles:
			g.add(circle)
		for arc in self.arcs:
			g.add(arc)
		self.dwg.add(g)
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
