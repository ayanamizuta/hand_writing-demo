import sys
sys.path.append('./common')
sys.path.append('./network')
sys.path.append('./param')
import SocketServer
from two_layer_net import TwoLayerNet
from simple_convnet import SimpleConvNet
import numpy as np
from itertools import product

class MyHTTPRequestHandler(SocketServer.StreamRequestHandler):

    def trim(self,s,net):
        if net == "nn":
            h_w = np.zeros(784)
            for i,k in product(range(784),range(8)):
                r = i / 28
                c = i % 28
                h_w[i] += sum([float(x) for x in s[(r*8+k)*224+c*8:(r*8+k)*224+c*8+8]])
        else:
            h_w = np.zeros((1,1,28,28))
            for i,k in product(range(784),range(8)):
                r = i / 28
                c = i % 28
                h_w[0,0,r,c] += sum([float(x) for x in s[(r*8+k)*224+c*8:(r*8+k)*224+c*8+8]])
        return h_w

    def handle(self):
        data = ""
        network = "nn"
        if self.request.recv(1) != "G":
            recv = self.request.recv(8192)
            #print recv
            recv = self.request.recv(8192)
            #print recv
            if recv.find("write_down=") >= 0:
                if recv.find("cnn") >= 0:
                    network = "cnn"
                else:
                    network = "nn"
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
        elif network == "nn":
            _input = self.trim(data[len("write_down="):-1],network)
            self.wfile.write(str_pre.replace("browser_demo","NN: " + str(np.argmax(simplenn.predict(_input)))))
        elif network == "cnn":
            _input = self.trim(data[len("write_down="):-1],network)
            self.wfile.write(str_pre.replace("browser_demo","CNN:" + str(np.argmax(simplecnn.predict(_input)))))
            
        f.close()

HOST = '127.0.0.1'
PORT = 8080
s = SocketServer.TCPServer((HOST, PORT), MyHTTPRequestHandler)

print 'connecting http://localhost:' + str(8080)

simplenn = TwoLayerNet(input_size=784, hidden_size=50, output_size=10)
simplenn.paramset()

simplecnn = SimpleConvNet(input_dim=(1,28,28), 
                        conv_param = {'filter_num': 30, 'filter_size': 5, 'pad': 0, 'stride': 1},
                        hidden_size=100, output_size=10, weight_init_std=0.01)
simplecnn.load_params()

s.serve_forever()
