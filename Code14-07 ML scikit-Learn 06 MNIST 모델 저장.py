from sklearn import svm, metrics
from  sklearn.model_selection import train_test_split
import pandas as pd

def changeValue(lst):
    return [float(v)/255 for v in lst]

## 0. Training Data, Test Data

csv = pd.read_csv('C:/PySource/Project1/mnist/train_10k.csv')
train_data = csv.iloc[:, 1:].values
train_data = list(map(changeValue, train_data))
train_label = csv.iloc[:, 0].values

csv = pd.read_csv('C:/PySource/Project1/mnist/t10k_0.5k.csv')
test_data = csv.iloc[:, 1:].values
test_data = list(map(changeValue, test_data))
test_label = csv.iloc[:, 0].values
## 학습용, 훈련용 분리

# train_data, test_data, train_label, test_label = \
#     train_test_split(train_data, train)label, train_size=0.3)
## 1. Create Classfire - Select ML Algorithm

clf = svm.NuSVC(gamma='auto')

## 2. Learning Data
#clf.fit([훈련 데이터], [정답])

clf.fit(train_data, train_label)

import joblib

joblib.dump(clf,'mnist_model_10k.dmp')

clf=joblib.load('mnist_model_10k.dmp')


## 3. Predict
# clf.predict([예측할 데이터])

## 4. Check Accuracy Rate

result = clf.predict(test_data)

score = metrics.accuracy_score(result, test_label)
print(result)
print("정답률: ","{0:.2f}%".format(score*100))

import matplotlib.pyplot as plt
import numpy as np
img= np.array(test_data[0]).reshape([28,28])
plt.imshow(img, cmap='gray')
plt.show()

