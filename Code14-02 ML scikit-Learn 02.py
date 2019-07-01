from sklearn import svm, metrics


## 0. Training Data, Test Data

train_data = [[0, 0], [0, 1], [1, 0], [1, 1]]
train_label = [0, 1, 1, 0]
test_data = [[1, 0], [0, 0]]
test_label =[1, 0]

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

print("정답률: ",score*100, '%')

