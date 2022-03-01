import logging
import json
import os

from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import lxml
import spyne
from wsgiref.simple_server import WSGIServer
from wsgiref.simple_server import make_server

carsData = {
    '1' :
     {
        "autonomie" : 230,
        "tps_recharge" : 240
    },
    '2' :
     {
        "autonomie" : 505,
        "tps_recharge" : 412
    },
    '3' :
     {
        "autonomie" : 395,
        "tps_recharge" : 300
    },
    '4' :
     {
        "autonomie" : 384,
        "tps_recharge" : 380
    }
}
#carLoad = json.dumps(carsData)
#jsonFile = open('cars.json')
#carLoad = json.load(jsonFile)

class carListService(ServiceBase):
    @rpc(Unicode, Integer, _returns=Iterable(Unicode))
    def say_hello(ctx, name, times):
        for i in range(times):
            yield u'Hello, %s' % name

    @rpc(Integer, Integer, _returns=Integer)
    def addition(ctx, num1, num2):
        return num1+num2
    
    @rpc(_returns=Unicode)
    def showCars(ctx):
        
        return json.dumps(carsData)
        
           
        
# jsonFile.close()




application = Application([carListService], 'spyne.examples.hello.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)


if __name__ == '__main__':
    port = int (os.environ.get('PORT',8000))
    server = make_server('0.0.0.0', port, wsgi_application)
    print("server is running on port " + str(port))
    server.serve_forever()
