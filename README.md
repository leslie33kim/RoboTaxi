# RobooTaxi

## Introduction
RoboTaxi is a semi-autonomous robotic vehicle project inspired by leading autonomous taxi services like Cruise, Waymo, and Zoox. The goal of this project is to create a vehicle capable of following designated tracks while autonomously avoiding obstacles in real-time. The vehicle is equipped with an ESP32 microcontroller, two DC motors, three ultrasonic sensors, and a LiDAR for obstacle detection. A graphical user interface (GUI) developed in LabVIEW allows users to interact with the vehicle, providing options for manual control and obstacle avoidance modes. The project also incorporates multitasking and real-time capabilities to efficiently process LiDAR data and control the vehicle's movements. Future plans involve adding computer vision using a camera for object detection and implementing model predictive control (MPC) for advanced path planning.

## Installation and Environment Requirements 
You will need to install PyLidar3 from Python, Labview, and THonny IDE for ESP 32 to run the following program. 

1. Launch RoboTaxi_lidar.py on any IDE or via terminal/command prompt using Python 3 interpreter (not in the MicroPython interpreter)
2. Stop RoboTaxi_lidar.py, then open the RoboTaxi_mainVI in LabVIEW. Set the image path in the LabVIEW GUI to the generated PyLidar_class.py1.jpg image.
3. Upload RoboTaxi_boot.py as boot.py in MicroPython using Thonny IDE
4. Upload RoboTaxi_main.py as main.py in MicroPython using Thonny IDE
5. Run main.py in MicroPython
6. Connect your PC to ESP32-RoboTaxi WiFi hotspot
7. Re-run RoboTaxi_lidar.py again using Python 3 interpreter (not in the MicroPython interpreter)
8. Run the RoboTaxi_mainVI in LabVIEW.
You should be able to see the LiDAR clustered point clouds being updated dynamically while being able to control the vehicle manually or let it drive in autonomous mode.

## Chassis Design 
<img width="388" alt="chassis" src="https://github.com/rafaelrivero16/RoboTaxi/assets/67294700/1607f806-3045-4a9a-bde1-20c514d7c3f2">

## GUI design 
A GUI was used to allow the user to interact with the vehicle both autonomously and manually. Features included in the GUI created via LabVIEW were as follows:

1. Pre-programmed track selection:
Track 1 drives the vehicle on a triangular track
Track 2 drives the vehicle on a square track
2. Manual control with emergency stop
Drive forward
Drive backward
Turn left
Turn right
3. Two selectable obstacle avoidance modes:
Track 2 Mode avoided objects while attempting to remain on the track
Dynamic Mode avoided objects turning left or right depending on where objects are located
4. Plot of the LiDAR clustered point clouds: 

<img width="618" alt="gui" src="https://github.com/rafaelrivero16/RoboTaxi/assets/67294700/ddb857cc-99f2-46f4-a2fe-c911441c44c1">


