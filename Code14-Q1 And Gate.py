from sklearn import svm

## 1. Create Classfire - Select ML Algorithm

clf = svm.SVC(gamma= 'auto')

clf.fit([[0, 0],
         [0, 1],
         [1, 0],
         [1, 1]],
        [0, 0, 0, 1])


result = clf.predict([[1, 1]])

print(result)