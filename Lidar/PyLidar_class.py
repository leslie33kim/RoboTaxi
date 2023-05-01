import PyLidar3
import matplotlib.pyplot as plt
import math    
import time
from sklearn.cluster import DBSCAN
import numpy as np

class Lidar:
    def __init__(self, port):
        self.port = "/dev/tty.usbserial-0001" #mac
        #self.port = "com6" #windows 
        self.Obj = PyLidar3.YdLidarX4(port)
        self.x = []
        self.y = []
        self.x_clusters = []
        self.y_clusters = []
        self.center_points = {}
        self.is_plot = False
    
    # Connect to PyLidar3 through port 
    def connect(self):
        if self.Obj.Connect():
            print(self.Obj.GetDeviceInfo())
            return True
        else:
            print("Error connecting to device")
            return False
    
    #Start lidar scanning process
    def start_scanning(self, scan_time=5, eps=90, min_samples=4):
        self.x = [0] * 360
        self.y = [0] * 360
        gen = self.Obj.StartScanning()
        t = time.time()
        while (time.time() - t) < scan_time:
            data = next(gen)
            for angle in range(0, 360, 2):
                if data[angle] > 100:
                    self.x[angle] = data[angle] * math.cos(math.radians(angle))
                    self.y[angle] = data[angle] * math.sin(math.radians(angle))
            features = np.column_stack((self.x, self.y))
            # eps: maximum distance between clusters, min_samples: minimum number of points in clusters
            dbscan = DBSCAN(eps=eps, min_samples=min_samples).fit(features)
            labels = dbscan.labels_
            self.x_clusters = []
            self.y_clusters = []
            self.center_points = {}
            self.center_angles = {}
            self.cluster_info = {}
            unique_labels = set(labels)
            for label in unique_labels:
                if label == -1:
                    continue
                mask = (labels == label)
                x_cluster = np.array(self.x)[mask]
                y_cluster = np.array(self.y)[mask]
                center_point = {'x': np.mean(x_cluster), 'y': np.mean(y_cluster)}
                center_angles = {'x': np.mean(np.array(self.x[angle])[mask]), 'x': np.mean(np.array(self.y[angle])[mask])}
                self.center_points[label] = center_point
                self.center_angles[label] = center_angles
                #Calculate distance from lidar ty center of each cluster
                center_distance = math.sqrt(center_point['x']**2 + center_point['y']**2)
                self.cluster_info[label] = (center_distance, center_angles)
                
                self.x_clusters.append(x_cluster)
                self.y_clusters.append(y_cluster)
                #self.center_points[label] = {'x': np.mean(np.array(self.x)[mask]), 'y': np.mean(np.array(self.y)[mask])}
                #center_point = {'x': np.mean(np.array(self.x)[mask]), 'y': np.mean(np.array(self.y)[mask])}
                # calculate distance from each point to center point
                # distances = [math.sqrt((x - center_point['x'])**2 + (y - center_point['y'])**2) for x, y in zip(x_cluster, y_cluster)]
                # self.cluster_distances[label] = distances
            #print(self.center_points)
            #print(f"Number of clusters: {len(self.x_clusters)}")
    
    def stop_scanning(self):
        self.Obj.StopScanning()
        self.Obj.Disconnect()
        
    def plot_clusters(self):
        self.is_plot = True
        plt.figure(1)
        plt.ylim(-1000, 1000)
        plt.xlim(-1000, 1000)
        colors = ['g', 'b', 'c', 'm', 'y', 'k']
        for i in range(len(self.x_clusters)):
            color = colors[i % len(colors)]
            plt.scatter(self.x_clusters[i], self.y_clusters[i], c=color, s=8)
        x_centers = [self.center_points[label]['x'] for label in self.center_points]
        y_centers = [self.center_points[label]['y'] for label in self.center_points]
        plt.scatter(x_centers, y_centers, c='r', s=12, alpha=1.0, marker='X')
        plt.show()

        
    # return list of x-coords of points in each cluster
    def get_x_clusters(self):
        return self.x_clusters
    
    # return list of x-coords of points in each cluster
    def get_y_clusters(self):
        return self.y_clusters
    
    # return number of meaningful clusters: wanna get this down to <3 for object detection
    def get_num_clusters(self):
        return len(self.x_clusters)
    
    # returns number of points in each x-cluster (list of integers)
    def get_num_points(self):
        num_points = [len(cluster) for cluster in self.x_clusters]
        return num_points
     
    # returns distance from lidar to cluster 
    def get_cluster_info(self): 
        return self.cluster_info

    #object detection using cluster distance (set threshold)
    def object_detection(self, max_distance=500):
        cluster_distances = self.get_cluster_distance()
        detected_objects = []
        for label, distance in cluster_distances.items():
            if distance <= max_distance:
                num_points = len(self.x_clusters[label])
                object_data = {'label': label, 'distance': distance, 'num_points': num_points}
                detected_objects.append(object_data)
        return detected_objects

