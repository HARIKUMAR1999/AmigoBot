#!/usr/bin/env python

import rospy
import tf
import time
import math
from std_msgs.msg import Float32MultiArray
from nav_msgs.msg import Odometry

x = 0
y = 0
theta = 0
vdash = 0
wdash = 0
timenow = time.time()
rate = 0

def WheelVelcallback(data):
    global timenow
    global x
    global y
    global theta
    global vdash
    global wdash
    dt = time.time() - timenow
    timenow = time.time()
    Dleft = data.data[0] * dt * (0.195/2)
    Dright = data.data[1] * dt * (0.195/2)
    Dcenter = (Dright + Dleft) / 2
    phi = (Dright - Dleft) / 0.331
    theta = theta + phi
    x = x + (Dcenter * math.cos(theta))
    y = y + (Dcenter * math.sin(theta))
    vdash = Dcenter / dt
    wdash = phi / dt

def listener():
    global rate
    rospy.init_node('custom_odom', anonymous=True)
    rate = rospy.Rate(10)
    rospy.Subscriber("wheel_velocities", Float32MultiArray, WheelVelcallback)

def compute():
    pub = rospy.Publisher('/my_odom', Odometry, queue_size=10)
    dats = Odometry()
    dats.header.frame_id = "odom"
    dats.child_frame_id = "base_link"
    dats.pose.pose.position.x = x
    dats.pose.pose.position.y = y
    dats.pose.pose.position.z = 0
    quart = tf.transformations.quaternion_about_axis(theta, (0, 0, 1))
    dats.pose.pose.orientation.x = quart[0]
    dats.pose.pose.orientation.y = quart[1]
    dats.pose.pose.orientation.z = quart[2]
    dats.pose.pose.orientation.w = quart[3]
    pub.publish(dats)

if __name__ == "__main__":
    listener()

    while not rospy.is_shutdown():
        compute()
        rate.sleep()