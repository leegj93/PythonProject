from sklearn import svm, metrics

## 1. Create Classfire - Select ML Algorithm

clf = svm.SVC(gamma= 'auto')

## 2. Learning Data
#clf.fit([훈련 데이터], [정답])

clf.fit([ [0, 0],
           [0, 1],
           [1, 0],
           [1, 1]],
           [0, 1, 1, 0])
## 3. Predict
# clf.predict([예측할 데이터])

## 4. Check Accuracy Rate


result = clf.predict([[1, 0], [0, 0]])

score = metrics.accuracy_score(result, [1, 0])

print("정답률: ",score*100, '%')



print(result)