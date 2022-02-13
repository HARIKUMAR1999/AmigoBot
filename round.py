#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist



WHEEL_DIA = 0.195
WHEEL_BASE = 0.331
Wheel_publisher=rospy.Publisher('/cmd_vel',Twist,queue_size=10)
twisty=Twist()



    
def wheel_vel():
    global twisty
    twisty.linear.x=0.5
    twisty.angular.z=-1
    Wheel_publisher.publish(twisty)
    

if __name__ == '__main__':
    rospy.init_node('Movement')
    while not rospy.is_shutdown():
        wheel_vel()
