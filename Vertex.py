class Vertex(object):
     def __init__(self, name):
          self.name = name
          self.adjacencies= []

     def addAdjacency(self, neighbour):
          if len(self.adjacencies) ==0 or not neighbour in self.adjacencies:
               self.adjacencies.append(neighbour)

     def __eq__(self, other):
          return self.name == other.name
