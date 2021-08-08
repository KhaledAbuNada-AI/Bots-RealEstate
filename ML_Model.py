import pandas as pd # To read data
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn import tree

import urllib
import csv



data = pd.read_csv('OpenSouqRealEstate.csv')  # load data set
X = data.iloc[:, 1:6].values # values converts it into a numpy array
Y = data.iloc[:, 0].values # -1 means that calculate the dimension of rows, but have 1 column
linear_regressor = tree.DecisionTreeClassifier()  # create object for the class
linear_regressor.fit(X, Y)  # perform linear regression
print(linear_regressor.score(X, Y))
#print(X)
Y_pred = linear_regressor.predict([[500,5,3,31.9946531,35.8662013]])  # make predictions
print(Y_pred)