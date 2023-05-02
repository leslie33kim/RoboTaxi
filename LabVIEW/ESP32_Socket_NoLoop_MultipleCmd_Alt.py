import network
import socket
import binascii

import gc
gc.collect()

import esp
esp.osdebug(None)

from machine import Pin, PWM   
from time import sleep

import PyLidar3
import matplotlib.pyplot as plt
import math    
import time
from sklearn.cluster import DBSCAN
import numpy as np

class DCMotor:      
  def __init__(self, pin1, pin2, enable_pin, min_duty=750, max_duty=1023):
    self.pin1=pin1
    self.pin2=pin2
    self.enable_pin=enable_pin
    self.min_duty = min_duty
    self.max_duty = max_duty

  def forward(self,speed):
    self.speed = speed
    self.enable_pin.duty(self.duty_cycle(self.speed))
    self.pin1.value(1)
    self.pin2.value(0)
    
  def backward(self, speed):
    self.speed = speed
    self.enable_pin.duty(self.duty_cycle(self.speed))
    self.pin1.value(0)
    self.pin2.value(1)

  def stop(self):
    self.enable_pin.duty(0)
    self.pin1.value(0)
    self.pin2.value(0)
    
  def duty_cycle(self, speed):
    if self.speed <= 0 or self.speed > 100:
      duty_cycle = 0
    else:
      duty_cycle = int(self.min_duty + (self.max_duty - self.min_duty)*((self.speed-1)/(100-1)))
      return duty_cycle

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
                print('masklen',len(mask))
                x_cluster = np.array(self.x)[mask]
                y_cluster = np.array(self.y)[mask]
                print('xlen',len(x_cluster))
                angle_cluster = np.array(range(0, 360, 1))[mask] # create array of angles for cluster
                print('anglelen',len(angle_cluster))
                center_point = {'x': np.mean(x_cluster), 'y': np.mean(y_cluster)}
                center_angle = np.mean(angle_cluster) # calculate mean angle for cluster
                self.center_points[label] = center_point
                self.center_angles[label] = center_angle
                #Calculate distance from lidar ty center of each cluster
                center_distance = math.sqrt(center_point['x']**2 + center_point['y']**2)
                self.cluster_info[label] = (center_distance, center_angle)
                #dj
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

lidar = Lidar(port="com6")
if lidar.connect(): 
    lidar.start_scanning(scan_time=5, eps=90, min_samples=4)
    num_clusters = lidar.get_num_clusters()
    x_clusters = lidar.get_x_clusters()
    y_clusters = lidar.get_y_clusters()
    num_points = lidar.get_num_points()
    cluster_dist = lidar.get_cluster_info()
    print(f"Number of clusters: {num_clusters}")
    print(f"Number of points in each cluster: {num_points}")
    print(f"Distance to each cluster: {cluster_dist}")
    lidar.plot_clusters()
    lidar.stop_scanning()
# wlan = network.WLAN(network.STA_IF) # create station interface
# wlan.active(True)       # activate the interface
# wlan.scan()             # scan for access points
# wlan.isconnected()      # check if the station is connected to an AP
# wlan.connect('Berkeley-IoT', '4,pEg&"W') # connect to an AP
# wlan.config('mac')      # get the interface's MAC address
# print(wlan.ifconfig())         # get the interface's IP/netmask/gw/DNS addresses

ap = network.WLAN(network.AP_IF) # create access-point interface
ap.active(True)
macaddress = (ap.config('mac'))
print(macaddress)


# mac_str = binascii.hexlify(ap.config('mac')).decode()
# print(mac_str)

ap.config(essid='ESP32-RoboTaxi',password='RoboTaxi') # set the SSID of the access point
print(ap.config('essid'))
ap.config(max_clients=10) # set how many clients can connect to the network
ap.active(True)         # activate the interface

print(ap.ifconfig())

def web_page():
  html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
  <body><h1>Hello, World! This is your ESP32 Talking</h1></body></html>"""
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # for AP
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # for Berkeley-IoT
s.bind(('', 80))
s.listen(30)
print('socket')

print('before running motors')
frequency = 15000       
pinLf = Pin(4, Pin.OUT) #left wheel forward
pinLb = Pin(5, Pin.OUT) #left wheel backward
enableL = PWM(Pin(13), frequency) #left wheel PWM
pinRf = Pin(18, Pin.OUT) #right wheel forward
pinRb = Pin(19, Pin.OUT) #right wheel backward
enableR = PWM(Pin(12), frequency) #right wheel PWM

dc_motorL = DCMotor(pinLf, pinLb, enableL, 350, 1023)
dc_motorL = DCMotor(pinLf, pinLb, enableL, 350, 1023)
dc_motorR = DCMotor(pinRf, pinRb, enableR, 350, 1023)
dc_motorR = DCMotor(pinRf, pinRb, enableR, 350, 1023)

while(1):
    print('waiting for connection')
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    print('Content = %s' % str(request))
    Command=str(request)[2]
    if Command == 'A':
        response = 'Forward'
        dc_motorL.forward(100) 
        dc_motorR.forward(100)
    elif Command == 'B':
        response = 'Backward'
        dc_motorL.backward(100) 
        dc_motorR.backward(100)
    elif Command == 'C':
        response = 'Left'
        dc_motorL.forward(0) 
        dc_motorR.forward(100)
    elif Command == 'D':
        response = 'Right'
        dc_motorL.forward(100) 
        dc_motorR.forward(0)
    elif Command == 'E':
        response = 'Stop'
        dc_motorL.stop() 
        dc_motorR.stop()
    elif Command == 'F': # Track 1
        response = 'Track 1'
        # Straight run from (0,0)
        for i in range(50):
            conn.close()
            conn, addr = s.accept()
            request = conn.recv(1024)
            Command=str(request)[2]
            if Command == 'E':
                dc_motorL.stop() 
                dc_motorR.stop()
                break
            dc_motorL.forward(100) 
            dc_motorR.forward(100)
            sleep(0.1)
        if Command == 'E':
            conn.close()
            continue
        # First semi-circle
        dc_motorL.forward(100)  
        dc_motorR.forward(0)
        sleep(5)
        # Straight run after first semi-circle
        dc_motorL.forward(100) 
        dc_motorR.forward(100)
        sleep(5)
        # Second semi-circle to close the loop
        dc_motorL.forward(100)  
        dc_motorR.forward(0)
        sleep(5)
        dc_motorL.stop()
        dc_motorR.stop()
    elif Command == 'G': # Track 2
        response = 'Track 2'
        # Circular-loop
        dc_motorL.forward(100)  
        dc_motorR.forward(0)
    conn.send(response)
    conn.close()

