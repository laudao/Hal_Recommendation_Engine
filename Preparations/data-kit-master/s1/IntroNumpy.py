import numpy as np

#data = np.random.randn(2, 3)
#print data
#print data*10
#print type(data)
#
#data1 = [1, 2, 3, 4]
#arr1 = np.array(data1)
#print arr1
#
#data2 = [[1, 2, 3], [4, 5, 6]]
#arr2 = np.array(data2)
#print arr2
#
#print np.arange(10)

#arr_string=np.array(['1.2', '2.3'])
#print arr_string.astype(np.float64)

#arr2d=np.array([[1,2,3],[4,5,6]])
#print arr2d[:,1]

### Exercices

#data3=[[19.23, 39.14, 67.78, 98.49], [56.78, 88.78, 99.01, 99.99], [12.00, 76.87, 91.09, 10.01], [99.01, 70.32, 64.89, 36.68]]
#arr3 = np.array(data3)
#print arr3
#print arr3[1:3]
#print arr3[:,3]

arr = np.arange(-10,10,0.5)
print arr[arr < 0]
print arr[(arr == 2) | (arr ==3)]

###

#arr = np.arange(-10, 10, 0.5)
#print arr > 0
#print arr[arr > 0]


