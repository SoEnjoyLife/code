#encoding=utf8
__author__ = 'paul_new'
from tornado import web
from tornado import ioloop

class MainRequestHandler(web.RequestHandler):


    def prepare(self):
        self.write('prepare\n')
        #self.finish()

    def get(self, word):
        name = self.get_argument('names', 'this')
        #print name
        self.write('hallelujah!' + name + word)


    def post(self, word):
        name = self.get_argument('name', 'friend')
        #print name
        data = u'你是有福的：' + name
        self.write(data)

app = web.Application(
    [('/(\w*)', MainRequestHandler), #confuse

     ],
    debug=True, #更新后自己会重启
)

if __name__ == '__main__':
    app.listen(8888)
    ioloop.IOLoop.instance().start()
