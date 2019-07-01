from sklearn import svm, metrics
from  sklearn.model_selection import train_test_split
import pandas as pd

'''
#붓꽃 데이터 분류기(머신러닝)
- 개요 : 150개 붓꽃 정보(꽃받침 길이, 꽃받침 폭, 꽃잎 길이, 꽃잎 폭)
- 종류 : 3개 (Iris-setosa, Iris-vesicolor, Iris-virginica)
 - CSV File: 검색 Iris.csv'''


## 0. Training Data, Test Data

csv = pd.read_csv('C:/PySource/Project1/csV/iris.csv')
data = csv.iloc[:, 0:-1]
label = csv.iloc[:, [-1]]
## 학습용, 훈련용 분리

train_data, test_data, train_label, test_label = \
    train_test_split(data,label, train_size=0.3)
## 1. Create Classfire - Select ML Algorithm

clf = svm.SVC(gamma='auto')

## 2. Learning Data
#clf.fit([훈련 데이터], [정답])

clf.fit(train_data, train_label)

## 3. Predict
# clf.predict([예측할 데이터])


## 4. Check Accuracy Rate

result = clf.predict(test_data)

score = metrics.accuracy_score(result, test_label)

print(result)
print("정답률: ","{0:.2f}%".format(score*100))
