#!/usr/bin/python

import time

import roslib
roslib.load_manifest('cob_people_detection')
roslib.load_manifest('cob_script_server')
import rospy

from math import *
import copy

from simple_script_server import *
sss = simple_script_server()

from cob_people_detection_msgs.msg import *
from cob_people_detection.srv import *


class DetectPeopleScript(script):
		
	def Initialize(self):
		self.srv_people_detection = '/cob_people_detection/detect_people'

		
	def Run(self): 


		try:
			rospy.wait_for_service(self.srv_people_detection,10)
		except rospy.ROSException, e:
			print "Service not available: %s"%e

		# call people detection service
		try:
			detector_service = rospy.ServiceProxy(self.srv_people_detection, DetectPeople)
			req = DetectPeopleRequest()
			res = detector_service(req)
		except rospy.ServiceException, e:
			print "Service call failed: %s"%e
			self.retries = 0
			return 'failed'
			
		# check for no objects
		if len(res.people_list.detections) <= 0:
			rospy.logerr("No faces found")
			self.retries += 1


		for item in res.people_list.detections:
			sss.say(["Hi " + item.label + "."],False)

		
	

if __name__ == "__main__":
	SCRIPT = DetectPeopleScript()
	SCRIPT.Start()
