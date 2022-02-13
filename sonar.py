#!/usr/bin/env python
import rospy
from sensor_msgs.msg import PointCloud

def customcallback(data):
    print("Sonar values\n")
    print(data.points)
    print("\n")

def listener():
    rospy.init_node('reading_sound',anonymous=True)
    rospy.Subscriber("sonar",PointCloud,customcallback)
    rospy.spin()

if __name__ == "__main__":
    listener()