# -*- coding: utf-8 -*-
class bird(object):

	def __init__(self):
		self.hungry=True

	def eat(self):
		if self.hungry:
			print 'good taste'
			self.hungry=False
		else:
			print 'no,thanks'

class singbird(bird):
	def __init__(self):
		self.song='hallelujah'
		#调用未绑定的超类构造方法
		#super(singbird,self).__init__()
		bird.__init__(self)

	def sing(self):
		print self.song
	
b=singbird()
b.sing()
b.eat()
b.eat()
b.eat()