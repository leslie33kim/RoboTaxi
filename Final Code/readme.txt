1. Launch RoboTaxi_lidar.py on any IDE or via terminal/command prompt using Python 3 interpreter (not in the MicroPython interpreter)
2. Stop RoboTaxi_lidar.py, then open the RoboTaxi_mainVI in LabVIEW. Set the image path in the LabVIEW GUI to the generated PyLidar_class.py1.jpg image.
3. Upload RoboTaxi_boot.py as boot.py in MicroPython using Thonny IDE
4. Upload RoboTaxi_main.py as main.py in MicroPython using Thonny IDE
5. Run main.py in MicroPython
6. Connect your PC to ESP32-RoboTaxi WiFi hotspot
7. Re-run RoboTaxi_lidar.py again using Python 3 interpreter (not in the MicroPython interpreter)
8. Run the RoboTaxi_mainVI in LabVIEW.
You should be able to see the LiDAR clustered point clouds being updated dynamically while being able to control the vehicle manually or let it drive in autonomous mode.