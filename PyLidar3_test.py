import PyLidar3
import matplotlib.pyplot as plt
port = input("Enter port name which lidar is connected:/dev/tty.usbserial-0001") #windows
Obj = PyLidar3.YdLidarX4("/dev/tty.usbserial-0001")
# if(Obj.Connect()):
#     print(Obj.GetDeviceInfo())
#     print(Obj.GetCurrentFrequency())
#     Obj.IncreaseCurrentFrequency(PyLidar3.FrequencyStep.oneTenthHertz)
#     print(Obj.GetCurrentFrequency())
#     Obj.DecreaseCurrentFrequency(PyLidar3.FrequencyStep.oneHertz)
#     print(Obj.GetCurrentFrequency())
#     Obj.Disconnect()
# else:
#     print("Error connecting to device")
from sklearn.cluster import DBSCAN
import PyLidar3
import numpy as np
import matplotlib.pyplot as plt
# import time # Time module
# #Serial port to which lidar connected, Get it from device manager windows
# #In linux type in terminal -- ls /dev/tty*
# #port = input("Enter port name which lidar is connected:com6") #windows
# #port = "/dev/ttyUSB0" #linux
port = input("Enter port name which lidar is connected:/dev/tty.usbserial-0001") #windows
Obj = PyLidar3.YdLidarX4("/dev/tty.usbserial-0001")
# if(Obj.Connect()):
#     print(Obj.GetDeviceInfo())
#     gen = Obj.StartScanning()
#     t = time.time() # start time
#     while (time.time() - t) < 30: #scan for 30 seconds
#         print(next(gen))
#         time.sleep(0.5)
#     Obj.StopScanning()
#     Obj.Disconnect()
# else:
#     print("Error connecting to device")

import threading
import PyLidar3
import matplotlib.pyplot as plt
import math    
import time
import matplotlib
matplotlib.use('agg')

def draw():
    global is_plot
    while is_plot:
        plt.figure(1)
        plt.cla()
        # plt.ylim(-9000,9000)
        # plt.xlim(-9000,9000)
        # plt.ylim(-5000,5000)
        # plt.xlim(-5000,5000)
        # plt.ylim(-3000,3000)
        # plt.xlim(-3000,3000)
        plt.ylim(-2000,2000)
        plt.xlim(-2000,2000)
        # plt.ylim(-500,500)
        # plt.xlim(-500,500)
        # plt.ylim(-200,200)
        # plt.xlim(-200,200)
        plt.scatter(x,y,c='r',s=8)
        colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
        for i in range(len(x_clusters)):
            color = colors[i % len(colors)]
            plt.scatter(x_clusters[i], y_clusters[i], c=color, s=8)
        # plt.pause(0.001)
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
    # x_clusters.append(0)
    # y_clusters.append(0)

# port =  input("Enter port name which lidar is connected:/dev/ttyUSB0") #windows
# Obj = PyLidar3.YdLidarX4(port) #PyLidar3.your_version_of_lidar(port,chunk_size) 
threading.Thread(target=draw).start()
if(Obj.Connect()):
    print(Obj.GetDeviceInfo())
    gen = Obj.StartScanning()
    t = time.time() # start time 
    while (time.time() - t) < 9999999999999999: #scan for 30 seconds
        data = next(gen)
        for angle in range(0,360,2):
            if(data[angle]>100):
                x[angle] = data[angle] * math.cos(math.radians(angle))
                y[angle] = data[angle] * math.sin(math.radians(angle))

                features = np.column_stack((x, y))
                # eps: maximum distance between clusters, min_samples: minimum number of points in clusters
                dbscan = DBSCAN(eps=0.2, min_samples=5)
                labels = dbscan.fit_predict(features)
                # Separate x and y values for each cluster label
              
                unique_labels = set(labels)
                for label in unique_labels: 
                    if label == -1:
                    # Skip outliersn
                        continue
                    mask = (labels == label)
                    x_clusters.append(np.array(x)[mask])
                    y_clusters.append(np.array(y)[mask])
                    # print(x_clusters)
                    # print(y_clusters)
    is_plot = False
    Obj.StopScanning()
    Obj.Disconnect()
else:
    print("Error connecting to device")
