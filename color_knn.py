import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
import statistics
import pickle

df = pd.read_csv('training_data.csv')
rgb = []
for i in list(df): 
    rgb = df[i].tolist()
    break

r_list = []
g_list = []
b_list = []
for im in rgb:
    current = im[1:len(im) - 1].split(',')
    r_list.append(float(current[0]))
    g_list.append(float(current[1]))
    b_list.append(float(current[2]))

df.insert(loc = 1, column = 'B value', value = b_list, allow_duplicates=True)
df.insert(loc = 1, column = 'G value', value = g_list, allow_duplicates=True)
df.insert(loc = 1, column = 'R value', value = r_list, allow_duplicates=True)
df = df.drop('Pixels', axis = 1)

mean = (statistics.mean(df['R value'].tolist()))
std = (statistics.stdev(df['R value'].tolist()))

mean_2 = (statistics.mean(df['G value'].tolist()))
std_2 = (statistics.stdev(df['G value'].tolist()))

mean_3 = (statistics.mean(df['B value'].tolist()))
std_3 = (statistics.stdev(df['B value'].tolist()))

print(mean, std)
print(mean_2, std_2)
print(mean_3, std_3)

scaler = StandardScaler()
  
scaler.fit(df.drop('Classification', axis = 1))
scaled_features = scaler.transform(df.drop('Classification', axis = 1))

df_feat = pd.DataFrame(scaled_features, columns = df.columns[:-1])

from sklearn.model_selection import train_test_split
  
X_train, X_test, y_train, y_test = train_test_split(
      scaled_features, df['Classification'], test_size = 0.10)
  
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix


knn = KNeighborsClassifier(n_neighbors = 5)
  
knn.fit(X_train, y_train)
pred = knn.predict(X_test)
  
print('WITH K = 5')
print('\n')
print(confusion_matrix(y_test, pred))
print('\n')
print(classification_report(y_test, pred))

# error_rate = []
  
# # Will take some time
# for i in range(1, 40):
      
#     knn = KNeighborsClassifier(n_neighbors = i)
#     knn.fit(X_train, y_train)
#     pred_i = knn.predict(X_test)
#     error_rate.append(np.mean(pred_i != y_test))
  
# plt.figure(figsize =(10, 6))
# plt.plot(range(1, 40), error_rate, color ='blue',
#                 linestyle ='dashed', marker ='o',
#          markerfacecolor ='red', markersize = 10)
  
# plt.title('Error Rate vs. K Value')
# plt.xlabel('K')
# plt.ylabel('Error Rate')
# plt.show()

knnPickle = open('knnpickle_file_add', 'wb')
pickle.dump(knn, knnPickle)
