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
from cob_people_detection.msg import *
from cob_people_detection.srv import *


class DetectPeopleScript(script):
		
	def Initialize(self):
		self.srv_people_detection = '/cob_people_detection/detect_people'
		self.srv_recognize = '/cob_people_detection/face_detection/recognize_service_server'

		
	def Run(self):
		try:
			rospy.wait_for_service(self.srv_recognize,10)
		except rospy.ROSException, e:
			print "Service not available: %s"%e

		# call people detection service
		try:
			recognize_service = rospy.ServiceProxy(self.srv_recognize, Recognition)
			req1 = RecognitionRequest()
			req1.running == True
			req1.doRecognition == True
			req1.display == True
			res1 = recognize_service(req1)
		except rospy.ServiceException, e:
			print "Service call failed: %s"%e
			return 'failed' 
		#while (True):
		for i in range (1,500):
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
				return 'failed'
			
			# check for no objects
			if len(res.people_list.detections) <= 0:
				rospy.logerr("No faces found")


			for item in res.people_list.detections:
				sss.say(["Hi " + item.label + "."],False)

		try:
			recognize_service = rospy.ServiceProxy(self.srv_recognize, Recognition)
			req2 = RecognitionRequest()
			req2.running == False
			req2.doRecognition == False
			req2.display == False
			res2 = recognize_service(req2)
		except rospy.ServiceException, e:
			print "Service call failed: %s"%e
			return 'failed' 

		
	

if __name__ == "__main__":
	SCRIPT = DetectPeopleScript()
	SCRIPT.Start()
