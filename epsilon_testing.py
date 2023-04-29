import PyLidar3
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import NearestNeighbors
import time # Time module
import math
import threading

#using K-nearest neighbor algorithm to find the eps value for DBSCAN
from sklearn.cluster import DBSCAN
port = "/dev/tty.usbserial-0001" #mac
#port = "com6" #windows
Obj = PyLidar3.YdLidarX4(port)

x=[]
y=[]
for _ in range(360):
    x.append(0)
    y.append(0)

if(Obj.Connect()):
    print(Obj.GetDeviceInfo())
    print(Obj.GetDeviceInfo())
    gen = Obj.StartScanning()
    t = time.time() # start time 
    while (time.time() - t) < 5: #scan for 5 seconds
        data = next(gen)
        for angle in range(0,360,2):
            if(data[angle]>100):
                x[angle] = data[angle] * math.cos(math.radians(angle))
                y[angle] = data[angle] * math.sin(math.radians(angle))
                features = np.column_stack((x, y))
                #print('features',features)
                # eps: maximum distance between clusters, min_samples: minimum number of points in clusters
    neighbors = NearestNeighbors(n_neighbors=4)
    neighbors_fit = neighbors.fit(features)
    distances, indices = neighbors_fit.kneighbors(features)
    distances = np.sort(distances, axis=0)
    distances = distances[:,1]

    # Compute elbow point using second derivative
    gradients = np.gradient(np.gradient(distances))
    elbow_index = np.argmax(gradients)
    elbow_value = distances[elbow_index]
    print(elbow_value)
    plt.plot(distances)
    plt.show()
    #try epsilon = 120
    
    Obj.StopScanning()
    Obj.Disconnect()
else:
    print("Error connecting to device")
    print("Error connecting to device")
