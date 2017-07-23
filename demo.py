import SocketServer
from two_layer_net import TwoLayerNet
import numpy as np
from itertools import product

class MyHTTPRequestHandler(SocketServer.StreamRequestHandler):

    def trim(self,s):
        h_w = np.zeros(784)
        for i,k in product(range(784),range(8)):
            r = i / 28
            c = i % 28
            h_w[i] += sum([float(x) for x in s[(r*8+k)*224+c*8:(r*8+k)*224+c*8+8]])
        return h_w

    def handle(self):
        #data = self.rfile.readline().strip()
        #print data
        
        #if data.find("POST") >= 0:
        #    while data.find("write_down=") < 0 or data == "":
        #        data = self.rfile.readline().strip()
        #        print data
        data = ""
        if self.request.recv(1) != "G":
            recv = self.request.recv(8192)
            #print recv
            recv = self.request.recv(8192)
            #print recv
            if recv.find("write_down=") >= 0:
                data += recv[recv.find("write_down="):-1]
                data += self.request.recv(224*224+len("write_down=")-len(data))
                #print data
        
        f = open("./demo.html", 'r')
        str_pre = f.read()

        self.wfile.write("HTTP/1.1 200 OK\r\n")
        self.wfile.write("Content-Type: text/html; charset=utf-8\r\n")
        self.wfile.write("\r\n")
        if data.find("write_down=") != 0:
            self.wfile.write(str_pre)
        else:
            _input = self.trim(data[len("write_down="):-1])
            self.wfile.write(str_pre.replace("browser_demo",str(np.argmax(network.predict(_input)))))
        f.close()

HOST = '127.0.0.1'
PORT = 8080
s = SocketServer.TCPServer((HOST, PORT), MyHTTPRequestHandler)

print 'connecting http://localhost:' + str(8080)

network = TwoLayerNet(input_size=784, hidden_size=50, output_size=10)
network.paramset()

s.serve_forever()
