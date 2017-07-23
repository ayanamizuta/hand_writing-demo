import SocketServer
from two_layer_net import TwoLayerNet
import numpy as np
from itertools import product

class MyHTTPRequestHandler(SocketServer.StreamRequestHandler):

    def trim(self,s):
        h_w = np.zeros((28,28)) 
        for i,j in product(range(28),range(28)):
            for k in range(8):
                h_w[i,j] += sum([float(x) for x in s[(i*8+k)*28:(i*8+k)*28+8]])
        return h_w

    def handle(self):
        data = self.rfile.readline().strip()
        print data
        
        if data.find("POST") >= 0:
            while data.find("write_down=") < 0:
                data = self.rfile.readline().strip()
                print data

        f = open("./demo.html", 'r')
        str_pre = f.read()

        self.wfile.write("HTTP/1.1 200 OK\r\n")
        self.wfile.write("Content-Type: text/html; charset=utf-8\r\n")
        self.wfile.write("\r\n")
        if data.find("?write_down=") != 0:
            self.wfile.write(str_pre)
        else:
            d = data.split(' ')[1]
            _input = trim(d["?write_down=".length:-1])
            str_pre.replace("browser_demo",str(network.predict(_input)))
            self.wfile.write(str_pre)
        f.close()

HOST = '127.0.0.1'
PORT = 8080
s = SocketServer.TCPServer((HOST, PORT), MyHTTPRequestHandler)

print 'connecting http://localhost:' + str(8080)

network = TwoLayerNet(input_size=784, hidden_size=50, output_size=10)
network.paramset()

s.serve_forever()
