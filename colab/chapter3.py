# -*- coding: utf-8 -*-
"""chapter3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bCJMB8rLhEIkgsjNALP2U-s7jRR0_n9W
"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 1.x

!wget -c https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh
!chmod +x Anaconda3-2019.10-Linux-x86_64.sh
!bash ./Anaconda3-2019.10-Linux-x86_64.sh -b -f -p /usr/local
!conda install -y -c deepchem -c rdkit -c conda-forge -c omnia deepchem-gpu=2.3.0
import sys
sys.path.append('/usr/local/lib/python3.7/site-packages/')
#import deepchem as dc

import deepchem as dc

dc.__version__

# libraries are installed
#now code has to be made

import numpy as np

#Training a Model to Predict Toxicity of Molecules

#getting the data for the objective
tox21_tasks, tox21_datasets, transformers = dc.molnet.load_tox21()

#corresponds to enzymatic assays
tox21_tasks

# the dataset, split into train valid test
tox21_datasets

train_dataset, valid_dataset, test_dataset = tox21_datasets

#A transformer is an object that modifies a dataset in some way. Deep‐
#Chem provides many transformers that manipulate data in useful ways.

transformers

# """
# DeepChem’s dc.models submodule contains a variety of
# different life science–specific models. All of these various models inherit from the
# parent class dc.models.Model


# dc.models.MultitaskClassifier . This model builds a fully connected
# network (an MLP) that maps input features to multiple output predictions. This
# makes it useful for multitask problems, where there are multiple labels for every sam‐
# ple. It’s well suited for our Tox21 datasets, since we have a total of 12 different assays
# we wish to predict simultaneously.


#I have changed the code compared to the book number of layers, 2 layer with 512 nodes each
# """


model = dc.models.MultitaskClassifier(n_tasks=12,n_features=1024,layer_sizes=[512,512])

model.fit(train_dataset, nb_epoch=20)

metric = dc.metrics.Metric(dc.metrics.roc_auc_score, np.mean)

train_scores = model.evaluate(train_dataset, [metric], transformers)

train_scores

test_scores = model.evaluate(test_dataset, [metric], transformers)

test_scores

#model is heaviy overfit , train aucroc is 0.996, testing is 0.762. one layer extra with more epochs 
# didn't help. This is as expected acording to the theory in ML

# next up is the CNN example for MNIST

!mkdir MNIST_data

!pwd

cd MNIST_data

!wget http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz
!wget http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz
!wget http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz
!wget http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz

#cd MNIST_data/

!pwd



cd ..

from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

import tensorflow as tf
import deepchem.models.tensorgraph.layers as layers

train_dataset = dc.data.NumpyDataset(mnist.train.images, mnist.train.labels)
test_dataset = dc.data.NumpyDataset(mnist.test.images, mnist.test.labels)

#del model

#model = dc.models.TensorGraph(model_dir='mnist')
#feature = layers.Feature(shape=(None, 784))
#label = layers.Label(shape=(None, 10))
#make_image = layers.Reshape(shape=(None, 28, 28), in_layers=feature)
#conv2d_1 = layers.Conv2D(num_outputs=32, activation_fn=tf.nn.relu,in_layers=make_image)
#conv2d_2 = layers.Conv2D(num_outputs=64, activation_fn=tf.nn.relu,in_layers=conv2d_1)
#flatten = layers.Flatten(in_layers=conv2d_2)
#dense1 = layers.Dense(out_channels=1024, activation_fn=tf.nn.relu,in_layers=flatten)
#dense2 = layers.Dense(out_channels=10, activation_fn=None, in_layers=dense1)
#smce = layers.SoftMaxCrossEntropy(in_layers=[label, dense2])
#loss = layers.ReduceMean(in_layers=smce)
#model.set_loss(loss)
#output = layers.SoftMax(in_layers=dense2)
#model.add_output(output)

from tensorflow.keras.layers import Reshape, Conv2D, Flatten, Dense, Softmax

model = tf.keras.Sequential([
    Reshape((28, 28, 1)),
    Conv2D(filters=32, kernel_size=5, activation=tf.nn.relu),
    Conv2D(filters=64, kernel_size=5, activation=tf.nn.relu),
    Flatten(),
    Dense(1024, activation=tf.nn.relu),
    Dense(10),
    Softmax()
])

model = dc.models.KerasModel(model, dc.models.losses.CategoricalCrossEntropy())

model.fit(train_dataset, nb_epoch=10)

prediction = np.squeeze(model.predict_on_batch(test_dataset.X))

prediction.shape

y_classes = prediction.argmax(axis=-1)

y_classes

y_orig = test_dataset.y.argmax(axis=-1)

y_orig

#ypred = np.argmax(prediction, axis=1)

#ypred

#from sklearn import preprocessing
#lb = preprocessing.LabelBinarizer()

from sklearn.metrics import accuracy_score

from sklearn.metrics import roc_curve, auc
import numpy as np

print("Validation")
prediction = np.squeeze(model.predict_on_batch(test_dataset.X))

fpr = dict()
tpr = dict()
roc_auc = dict()
for i in range(10):
    fpr[i], tpr[i], thresh = roc_curve(test_dataset.y[:, i], prediction[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])
    print("class %s:auc=%s" % (i, roc_auc[i]))

test_dataset.y[:, i].shape

ypred.shape

accuracy_score(y_classes, ypred)

#metric = dc.metrics.Metric(dc.metrics.accuracy_score)

#train_dataset.get_shape()

#train_scores = model.evaluate(train_dataset, [metric])
#test_scores = model.evaluate(test_dataset, [metric])

#train_scores

#for training
y_train = np.squeeze(model.predict_on_batch(train_dataset.X))

y_train_predlabels = y_train.argmax(axis=-1)



y_train_labels.shape

y_train_orig = train_dataset.y.argmax(axis=-1)

#
training_accuracy = accuracy_score(y_train_orig, y_train_predlabels)

training_accuracy

# test accuracy already calculated above
accuracy_score(y_classes, ypred)

########### completed after running a GPU instance on colab
