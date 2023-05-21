from pyrplidar import PyRPlidar
import time
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import RobustScaler

def getting_shortest_distance(Distance,Angle):
    min_dist_index = np.argmin(Distance)
    min_dist = Distance[min_dist_index]
    min_angle = Angle[min_dist_index]
    return min_dist,min_angle

def car2pol(x,y):
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y,x)
    return r , theta

def pol2carteisan_x(rho,theta):
    x = rho * math.cos(theta)
    return x

def pol2carteisan_y(rho,theta):
    y = rho * math.sin(theta)
    return y

def plot(x,y):
    # plot
    #plt.plot(y, x, color='green', linestyle='', linewidth=0.5,
    #         marker='o', markerfacecolor='blue', markersize=5)
    plt.scatter(x, y, marker='.')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()

def remove_zero_distance(distances, angles):
  new_distances = []
  new_angles = []
  for i in range(len(distances)):
    if distances[i] != 0:
      new_distances.append(distances[i])
      new_angles.append(angles[i])
  return np.array(new_distances), np.array(new_angles)

def simple_scan():
    lidar = PyRPlidar()
    lidar.connect(port="COM6", baudrate=256000, timeout=3)
    # Linux   : "/dev/ttyUSB0"
    # MacOS   : "/dev/cu.SLAB_USBtoUART"
    # Windows : "COM5"

    lidar.set_motor_pwm(800)
    time.sleep(5)
    arr_dist = []
    arr_angle = []
    len_count = []

    #scan_generator = lidar.get_scan_modes()  # 16K
    scan_generator = lidar.start_scan_express(mode = 2) #2 or 3
    for count, scan in enumerate(scan_generator()):
        # print(count, scan.distance)
        arr_dist.append(scan.distance)
        arr_angle.append(scan.angle)
        len_count.append(count)
        if count == 1600: break
    lidar.stop()
    lidar.set_motor_pwm(0)
    lidar.disconnect()
    return arr_dist,arr_angle,len_count

def data_processing():
    dist,angle,count =simple_scan()
    radius = 130
    distance = np.array(dist)
    index = np.array(count)
    angle1 = np.array(angle)

    # Converting to radians
    radian_angle = np.radians(angle1)
    arr_angle_rounded = np.round(radian_angle, 3)

    # Remove Zero distances
    distance_non_zero, angles_non_zero = remove_zero_distance(distance, arr_angle_rounded)

    # Convert to X and Y
    X1, Y1 = [], []
    for i in range(len(distance_non_zero)):
        X1.append(pol2carteisan_x(distance_non_zero[i], angles_non_zero[i]))
        Y1.append(pol2carteisan_y(distance_non_zero[i], angles_non_zero[i]))

    # Distance between data points
    index1 = []
    for i in range(len(X1)):
        distance = 0
        distance = np.sqrt((X1[i] - X1[i - 1]) ** 2 + (Y1[i] - Y1[i - 1]) ** 2)
        # if distance < 3 or distance > 30: #remove
        if distance < 2 or distance > 30:  # remove
            index1.append(i)

    remove_x = np.delete(X1, index1)
    remove_y = np.delete(Y1, index1)

    # Angles between two vectors
    index_to_remove = []
    # Find Vx, Vy and to get tan(theta)
    # iterate through the list
    # AB = distance between x1,y1 and x2,y2
    # BC = distance between x2,y2 and x3,y3
    for i in range(len(remove_x) - 2):
        AB = math.sqrt((remove_x[i + 1] - remove_x[i]) ** 2 + (remove_y[i + 1] - remove_y[i]) ** 2)
        BC = math.sqrt((remove_x[i + 2] - remove_x[i + 1]) ** 2 + (remove_y[i + 2] - remove_y[i + 1]) ** 2)
        arc_tan = np.arctan2(BC, AB)
        # if arc_tan < 0.6 or arc_tan> 0.9:
        if arc_tan < 0.2 or arc_tan > 0.9:
            index_to_remove.append(i)

    X_Vector = np.delete(remove_x, index_to_remove)
    Y_Vector = np.delete(remove_y, index_to_remove)
    #plot(X_Vector, Y_Vector)

    # GROUP
    # DBSCAN
    # Cluster the data
    # dbscan = DBSCAN(eps=0.1, min_samples=6) # 0.2,5
    data = np.column_stack((X_Vector, Y_Vector))
    # Scale the data
    scaler = RobustScaler()
    scaled_data = scaler.fit_transform(data)
    dbscan = DBSCAN(eps=0.1, min_samples=4)  # 0.2,5
    clusters = dbscan.fit_predict(scaled_data)
    """
    # Plot the clusters
    plt.scatter(X_Vector, Y_Vector, c=clusters, cmap='viridis')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()
    """
    # Least Square Regression
    num_clusters = len(set(clusters)) - (1 if -1 in clusters else 0)  # account for noise points labeled as -1
    ARC, X_ARC, Y_ARC, RESIDUALS = [], [], [], []

    distance_arc, SLOPE = [], []
    for i in range(num_clusters):
        # ARC = data[clusters == i]
        arc_points = data[clusters == i]
        x_arc = arc_points[:, 0]  # .flatten().tolist() #array
        y_arc = arc_points[:, 1]

        if 8 < len(arc_points) < 80:
            # check for the distance for each cluster
            first_x = x_arc[0]
            last_x = x_arc[-1]
            first_y = y_arc[0]
            last_y = y_arc[-1]
            distance_cluster = np.sqrt((first_x - last_x) ** 2 + (first_y - last_y) ** 2)
            print(distance_cluster)
            if 90 < distance_cluster < 190:
                X_ARC.append(x_arc)
                Y_ARC.append(y_arc)

    #for i in range(len(X_ARC)):
        #plot(X_ARC[i], Y_ARC[i])

    # Convert Cartesian to polar
    D_ARC_1, A_ARC_1 = car2pol(X_ARC[0], Y_ARC[0])  # All same size
    D_ARC_2, A_ARC_2 = car2pol(X_ARC[1], Y_ARC[1])
    D_ARC_3, A_ARC_3 = car2pol(X_ARC[2], Y_ARC[2])

    # Find the shortest distance and its angle
    # ARC1
    R1, Theta1 = getting_shortest_distance(D_ARC_1, A_ARC_1)
    # ARC2
    R2, Theta2 = getting_shortest_distance(D_ARC_2, A_ARC_2)
    # ARC3
    R3, Theta3 = getting_shortest_distance(D_ARC_3, A_ARC_3)

    if Theta1 < 0:
        Theta1 = Theta1 + (2 * math.pi)
    if Theta2 < 0:
        Theta2 = Theta2 + (2 * math.pi)
    if Theta3 < 0:
        Theta3 = Theta3 + (2 * math.pi)

    # Update R1 with radius
    R1 = R1 + radius
    R2 = R2 + radius
    R3 = R3 + radius

    # Convert Radian to degree
    theta1_degree = Theta1 * (180 / math.pi)
    theta2_degree = Theta2 * (180 / math.pi)
    theta3_degree = Theta3 * (180 / math.pi)
    #print("R1: ", R1, "Theta 1 :", theta1_degree)
    #print("R2: ", R2, "Theta 2 :", theta2_degree)
    #print("R3: ", R3, "Theta 3 :", theta3_degree)
    return R1,R2,R3,theta1_degree,theta2_degree,theta3_degree

if __name__ == "__main__":
    distance1,distance2,distance3,theta_1,theta_2,theta_3 = data_processing()