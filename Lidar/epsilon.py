import matplotlib.pyplot as plt
import numpy as np
from PyLidar_class import Lidar

# Using K-nearest neighbor algorithm to find the eps value for DBSCAN
from sklearn.neighbors import NearestNeighbors

# Initialize Lidar object
# lidar = Lidar("/dev/tty.usbserial-0001") # mac
lidar = Lidar("com6") # mac

if lidar.connect():
    lidar.start_scanning(scan_time=5, eps=90, min_samples=4)

    # Compute elbow point using K-nearest neighbor algorithm
    features = np.column_stack((lidar.x, lidar.y))
    neighbors = NearestNeighbors(n_neighbors=4)
    neighbors_fit = neighbors.fit(features)
    distances, indices = neighbors_fit.kneighbors(features)
    distances = np.sort(distances, axis=0)
    distances = distances[:, 1]
    print('dis',distances)
    gradients = np.gradient(distances)
    print('grad',gradients)
    elbow_index = np.argmax(gradients)
    elbow_value = distances[elbow_index]
    print("Elbow value:", elbow_value)
    plt.plot(distances)
    plt.show()

    lidar.stop_scanning()
    lidar.disconnect()
else:
    print("Error connecting to device")