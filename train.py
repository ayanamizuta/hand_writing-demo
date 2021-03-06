# coding: utf-8
import sys
sys.path.append('./common')
sys.path.append('./network')
import os
import numpy as np
import matplotlib.pyplot as plt
from mnist import load_mnist
from trainer import Trainer
from two_layer_net import TwoLayerNet
from simple_convnet import SimpleConvNet

(x_train, t_train), (x_test, t_test) = load_mnist(normalize=True, one_hot_label=True)

network = TwoLayerNet(input_size=784, hidden_size=50, output_size=10)

iters_num = 10000
train_size = x_train.shape[0]
batch_size = 100
learning_rate = 0.1

train_loss_list = []
train_acc_list = []
test_acc_list = []

iter_per_epoch = max(train_size / batch_size, 1)

for i in range(iters_num):
    batch_mask = np.random.choice(train_size, batch_size)
    x_batch = x_train[batch_mask]
    t_batch = t_train[batch_mask]
    
    grad = network.gradient(x_batch, t_batch)
    
    for key in ('W1', 'b1', 'W2', 'b2'):
        network.params[key] -= learning_rate * grad[key]
    
    loss = network.loss(x_batch, t_batch)
    train_loss_list.append(loss)
    
    if i % iter_per_epoch == 0:
        train_acc = network.accuracy(x_train, t_train)
        test_acc = network.accuracy(x_test, t_test)
        train_acc_list.append(train_acc)
        test_acc_list.append(test_acc)
        print("train acc, test acc | " + str(train_acc) + ", " + str(test_acc))

f = open('param.txt','w+')

for i,x in enumerate(network.params['W1']):
    if i != 0:
        f.write(",")
    f.write(",".join([str(s) for s in x]))
f.write("\n")

for i,x in enumerate(network.params['b1']):
    if i != 0:
        f.write(",")
    f.write(str(x))
f.write("\n")

for i,x in enumerate(network.params['W2']):
    if i != 0:
        f.write(",")
    f.write(",".join([str(s) for s in x]))
f.write("\n")

for i,x in enumerate(network.params['b2']):
    if i != 0:
        f.write(",")
    f.write(str(x))
f.write("\n")

f.close()

(x_train, t_train), (x_test, t_test) = load_mnist(flatten=False)

max_epochs = 20

network = SimpleConvNet(input_dim=(1,28,28), 
                        conv_param = {'filter_num': 30, 'filter_size': 5, 'pad': 0, 'stride': 1},
                        hidden_size=100, output_size=10, weight_init_std=0.01)
                        
trainer = Trainer(network, x_train, t_train, x_test, t_test,
                  epochs=max_epochs, mini_batch_size=100,
                  optimizer='Adam', optimizer_param={'lr': 0.001},
                  evaluate_sample_num_per_epoch=10000)
trainer.train()

network.save_params("params.pkl")
