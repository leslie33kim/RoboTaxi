<<<<<<< Updated upstream
<<<<<<< HEAD
# import PyLidar3
#import matplotlib.pyplot as plt
# port = input("Enter port name which lidar is connected:/dev/ttyt0") #windows
# Obj = PyLidar3.YdLidarX4("/dev/ttyt0")
=======
=======
>>>>>>> Stashed changes
import PyLidar3
import matplotlib.pyplot as plt
port = input("Enter port name which lidar is connected:/dev/tty.usbserial-0001") #windows
Obj = PyLidar3.YdLidarX4("/dev/tty.usbserial-0001")
>>>>>>> 0340ce2ef9e245ae9dcd17540ecc2eb8fb8ea2d9
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
<<<<<<< HEAD

# import PyLidar3
# from sklearn.cluster import DBSCAN
# import numpy as np
# import matplotlib.pyplot as plt
# import time # Time module
# #Serial port to which lidar connected, Get it from device manager windows
# #In linux type in terminal -- ls /dev/tty*
# port = input("Enter port name which lidar is connected:com6") #windows
# #port = "/dev/ttyUSB0" #linux
# Obj = PyLidar3.YdLidarX4("com6") #PyLidar3.your_version_of_lidar(port,chunk_size)
=======
from sklearn.cluster import DBSCAN
import PyLidar3
import numpy as np
import matplotlib.pyplot as plt
<<<<<<< Updated upstream
=======
from sklearn.neighbors import NearestNeighbors
import time # Time module
#Serial port to which lidar connected, Get it from device manager windows
#In linux type in terminal -- ls /dev/tty*
#port = input("Enter port name which lidar is connected:com6") #windows
#port = "/dev/ttyUSB0" #linux
#Obj = PyLidar3.YdLidarX4("com6") #PyLidar3.your_version_of_lidar(port,chunk_size)
if(Obj.Connect()):
    print(Obj.GetDeviceInfo())
    gen = Obj.StartScanning()
    t = time.time() # start time
    while (time.time() - t) < 10: #scan for 30 seconds
        print(next(gen))
        time.sleep(0.5)
    Obj.StopScanning()
    Obj.Disconnect()
else:
    print("Error connecting to device")
>>>>>>> Stashed changes
# import time # Time module
# #Serial port to which lidar connected, Get it from device manager windows
# #In linux type in terminal -- ls /dev/tty*
# #port = input("Enter port name which lidar is connected:com6") #windows
# #port = "/dev/ttyUSB0" #linux
port = input("Enter port name which lidar is connected:/dev/tty.usbserial-0001") #windows
Obj = PyLidar3.YdLidarX4("/dev/tty.usbserial-0001")
<<<<<<< Updated upstream
>>>>>>> 0340ce2ef9e245ae9dcd17540ecc2eb8fb8ea2d9
=======
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
<<<<<<< HEAD
from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pyplot as plt
=======
import matplotlib
matplotlib.use('agg')
>>>>>>> 0340ce2ef9e245ae9dcd17540ecc2eb8fb8ea2d9
=======
import matplotlib
#matplotlib.use('agg')
>>>>>>> Stashed changes

def draw():
    global is_plot
    while is_plot:
<<<<<<< Updated upstream
        plt.figure(1)
        plt.cla()
        # plt.ylim(-9000,9000)
        # plt.xlim(-9000,9000)
        # plt.ylim(-5000,5000)
<<<<<<< HEAD

=======
>>>>>>> 0340ce2ef9e245ae9dcd17540ecc2eb8fb8ea2d9
        # plt.xlim(-5000,5000)
        # plt.ylim(-3000,3000)
        # plt.xlim(-3000,3000)
        plt.ylim(-2000,2000)
        plt.xlim(-2000,2000)
        # plt.ylim(-500,500)
        # plt.xlim(-500,500)
<<<<<<< HEAD

        # plt.ylim(-200,200)
        # plt.xlim(-200,200)
        #plt.scatter(x,y,c='r',s=8)
        print(len(x_clusters))
        print(len(y_clusters))
        for i in range(min(len(x_clusters),len(y_clusters))):
            plt.scatter(x_clusters[i], y_clusters[i], c='r', s=8)
=======
        # plt.ylim(-200,200)
        # plt.xlim(-200,200)
        plt.scatter(x,y,c='r',s=8)
        colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
        for i in range(len(x_clusters)):
            color = colors[i % len(colors)]
            plt.scatter(x_clusters[i], y_clusters[i], c=color, s=8)
>>>>>>> 0340ce2ef9e245ae9dcd17540ecc2eb8fb8ea2d9
        # plt.pause(0.001)
        plt.pause(0.01)
    plt.close("all")
    
                
=======
        #plt.figure(1)
        #plt.cla()
        # plt.ylim(-9000,9000)
        # plt.xlim(-9000,9000)
        # plt.ylim(-5000,5000)
        # plt.xlim(-5000,5000)
        # plt.ylim(-3000,3000)
        # plt.xlim(-3000,3000)
        # plt.ylim(-2000,2000)
        # plt.xlim(-2000,2000)
        # plt.ylim(-500,500)
        # plt.xlim(-500,500)
        # plt.ylim(-200,200)
        # plt.xlim(-200,200)
        #plt.scatter(x,y,c='r',s=8)
        colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
        #print("Length of x cluster:",len(x_clusters))
        #print("Length of x cluster:",len(y_clusters))
        # for i in range(len(x_clusters)):
        #     color = colors[i % len(colors)]
        #     plt.scatter(x_clusters[i], y_clusters[i], c=color, s=8)
        #     plt.show()
        # plt.pause(0.01)
    #plt.close("all")
is_plot = True
x=[]
y=[]
x_clusters = []
y_clusters = []
<<<<<<< Updated upstream
<<<<<<< HEAD
for _ in range(360):
    x.append(0)
    y.append(0)
    x_clusters.append(0)
    y_clusters.append(0)

=======

for _ in range(360):
    x.append(0)
    y.append(0)
    # x_clusters.append(0)
    # y_clusters.append(0)
>>>>>>> 0340ce2ef9e245ae9dcd17540ecc2eb8fb8ea2d9

=======

for _ in range(360):
    x.append(0)
    y.append(0)
    # x_clusters.append(0)
    # y_clusters.append(0)

#port =  input("Enter port name which lidar is connected:com6") #windows
#Obj = PyLidar3.YdLidarX4("com6") #PyLidar3.your_version_of_lidar(port,chunk_size) 
>>>>>>> Stashed changes
# port =  input("Enter port name which lidar is connected:/dev/ttyUSB0") #windows
# Obj = PyLidar3.YdLidarX4(port) #PyLidar3.your_version_of_lidar(port,chunk_size) 
threading.Thread(target=draw).start()
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
<<<<<<< Updated upstream
                # eps: maximum distance between clusters, min_samples: minimum number of points in clusters
                dbscan = DBSCAN(eps=0.2, min_samples=5)
                labels = dbscan.fit_predict(features)
                # Separate x and y values for each cluster label
<<<<<<< HEAD
=======
              
>>>>>>> 0340ce2ef9e245ae9dcd17540ecc2eb8fb8ea2d9
                unique_labels = set(labels)
                for label in unique_labels: 
                    if label == -1:
                    # Skip outliersn
                        continue
                    mask = (labels == label)
<<<<<<< HEAD
                    #print('mask',mask)
                    #print('x[mask]',np.array(x)[mask])
                    x_clusters.append(np.array(x)[mask])
                    #print('x_clusters',x_clusters)
                    y_clusters.append(y[mask])
=======
                    x_clusters.append(np.array(x)[mask])
                    y_clusters.append(np.array(y)[mask])
                    # print(x_clusters)
                    # print(y_clusters)
>>>>>>> 0340ce2ef9e245ae9dcd17540ecc2eb8fb8ea2d9
=======
    # eps: maximum distance between clusters, min_samples: minimum number of points in clusters
    dbscan = DBSCAN(eps=130, min_samples=4).fit(features)
    labels = dbscan.labels_
    # Number of meaningful clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)
    #labels = dbscan.fit_predict(features)
    unique_labels = set(labels)
    for label in unique_labels: 
        if label == -1:
            # Skip outliers
            continue
        mask = (labels == label)
        print(mask)
        #print(mask)
        x_clusters.append(np.array(x)[mask])
        y_clusters.append(np.array(y)[mask])
        # print(x_clusters)
        # print(y_clusters)            
    print(n_clusters_)    
>>>>>>> Stashed changes
    is_plot = False

    Obj.StopScanning()
    Obj.Disconnect()
else:
    print("Error connecting to device")
<<<<<<< Updated upstream
=======
    print("Error connecting to device")
>>>>>>> Stashed changes
