# import PyLidar3
#import matplotlib.pyplot as plt
# port = input("Enter port name which lidar is connected:/dev/ttyt0") #windows
# Obj = PyLidar3.YdLidarX4("/dev/ttyt0")

import PyLidar3
import matplotlib.pyplot as plt
port = input("Enter port name which lidar is connected:/dev/tty.usbserial-0001") #mac
#port = input("Enter port name which lidar is connected:com6") #windows
Obj = PyLidar3.YdLidarX4("/dev/tty.usbserial-0001") #mac
#Obj = PyLidar3.YdLidarX4("com6") #windows

from sklearn.cluster import DBSCAN
import PyLidar3
import numpy as np
import matplotlib.pyplot as plt

from sklearn.neighbors import NearestNeighbors
import time # Time module
#Serial port to which lidar connected, Get it from device manager windows
#In linux type in terminal -- ls /dev/tty*
#port = input("Enter port name which lidar is connected:com6") #windows
#port = "/dev/ttyUSB0" #linux
#Obj = PyLidar3.YdLidarX4("com6") #PyLidar3.your_version_of_lidar(port,chunk_size)
# if(Obj.Connect()):
#     print(Obj.GetDeviceInfo())
#     gen = Obj.StartScanning()
#     t = time.time() # start time
#     while (time.time() - t) < 10: #scan for 30 seconds
#         print(next(gen))
#         time.sleep(0.5)
#     Obj.StopScanning()
#     Obj.Disconnect()
# else:
#     print("Error connecting to device")

#import threading
import PyLidar3
import matplotlib.pyplot as plt
import math    
import time
from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pyplot as plt

def draw():
    global is_plot
    while is_plot:
        plt.figure(1)
        plt.cla()
        plt.ylim(-1000,1000)
        plt.xlim(-1000,1000)
        colors = ['g', 'b', 'c', 'm', 'y', 'k']
        for i in range(len(x_clusters)):
            color = colors[i % len(colors)]
            plt.scatter(x_clusters[i], y_clusters[i], c=color, s=8)
            # center_x = np.mean(x_clusters[i])
            # center_y = np.mean(y_clusters[i])
        x_centers = [center_points[label]['x'] for label in center_points]
        y_centers = [center_points[label]['y'] for label in center_points]
        # Plot the center points (color=red)
        plt.scatter(x_centers, y_centers, c = 'r', s=12, alpha=1.0, marker='X')
        plt.show()
        plt.pause(0.01)
    plt.close("all")

is_plot = True
x=[]
y=[]
x_clusters = []
y_clusters = []

for _ in range(360):
    x.append(0)
    y.append(0)

# threading.Thread(target=draw).start()
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

    # eps: maximum distance between clusters, min_samples: minimum number of points in clusters
    dbscan = DBSCAN(eps=140, min_samples=4).fit(features)
    labels = dbscan.labels_
    # Number of meaningful clusters in labels, ignoring noise if present
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)
    #labels = dbscan.fit_predict(features)
    unique_labels = set(labels)
    center_points = {}  # dictionary to store center points
    for label in unique_labels: 
        if label == -1:
            # Skip outliers
            continue
        mask = (labels == label)
        print(mask)
        x_cluster = np.array(x)[mask]
        y_cluster = np.array(y)[mask]
        #set cluster threshold 
        # if len(x_cluster) < 10:
        #     continue
        x_clusters.append(x_cluster)
        y_clusters.append(y_cluster)
        center_points[label] = {'x': np.mean(np.array(x)[mask]), 'y': np.mean(np.array(y)[mask])}           
    print(n_clusters_) 
    print(center_points)   
    draw()
    is_plot = False
    Obj.StopScanning()
    Obj.Disconnect()
else:
    print("Error connecting to device")

