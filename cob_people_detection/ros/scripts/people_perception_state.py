#!/usr/bin/python
#################################################################
##\file
#
# \note
#   Copyright (c) 2010 \n
#   Fraunhofer Institute for Manufacturing Engineering
#   and Automation (IPA) \n\n
#
#################################################################
#
# \note
#   Project name: care-o-bot
# \note
#   ROS stack name: 
# \note
#   ROS package name: 
#
# \author
#   Nadia Hammoudeh Garcia, nadia.hammoudeh.garcia@ipa.fhg.de
#
# \date Date of creation: Jun 2012
#
# \brief
#  
#
#################################################################
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     - Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer. \n
#     - Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution. \n
#     - Neither the name of the Fraunhofer Institute for Manufacturing
#       Engineering and Automation (IPA) nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission. \n
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License LGPL as 
# published by the Free Software Foundation, either version 3 of the 
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License LGPL for more details.
# 
# You should have received a copy of the GNU Lesser General Public 
# License LGPL along with this program. 
# If not, see <http://www.gnu.org/licenses/>.
#
#################################################################

import roslib
roslib.load_manifest('cob_people_detection')
roslib.load_manifest('cob_script_server')
import rospy
import smach
import smach_ros

from math import *
import copy

from simple_script_server import *
sss = simple_script_server()

from cob_people_detection_msgs.msg import *
from cob_people_detection.msg import *
from cob_people_detection.srv import *

## Detect state
#
# This state will try to detect an object.
class detect_people(smach.State):
	def __init__(self,name = ""):
		smach.State.__init__(
			self,
			outcomes=['succeeded','no_person','failed'],
			input_keys=['name'],
			output_keys=['people'])

		self.people_list = PeopleDetectionArray()
		self.name = name
		
		self.srv_people_detection = '/cob_people_detection/detect_people'
		self.srv_recognize = '/cob_people_detection/face_detection/recognize_service_server'

	def execute(self, userdata):

		try:
			rospy.wait_for_service(self.srv_recognize)
		except rospy.ROSException, e:
			print "Service not available: %s"%e
			return 'failed'

		# call people detection service
		try:
			recognize_service = rospy.ServiceProxy(self.srv_recognize, Recognition)
			req = RecognitionRequest()
			req.running = True
			req.doRecognition = True
			req.display = True
			res = recognize_service(req)
			print "Success %s" %res.success
		except rospy.ServiceException, e:
			print "Service call failed: %s"%e
			return 'failed' 

		#while (True):
		for i in range (1,500):
			rospy.sleep(2)
			try:
				rospy.wait_for_service(self.srv_people_detection,10)
			except rospy.ROSException, e:
				print "Service not available: %s"%e
				return 'failed'

			# call people detection service
			try:
				detector_service = rospy.ServiceProxy(self.srv_people_detection, DetectPeople)
				req = DetectPeopleRequest()
				res = detector_service(req)
			except rospy.ServiceException, e:
				print "Service call failed: %s"%e
				return 'failed'
			
			
			if len(res.people_list.detections) <= 0:
				rospy.logerr("No faces found")
				return 'no_person'


			for item in res.people_list.detections:
				if (item.label == userdata.name):
					sss.say(["Hi " + item.label + "."],False)
					people = copy.deepcopy(item)
				elif (userdata.name == "all"):
					people = copy.deepcopy(item)
				else:
					print "No people"	


		try:
			recognize_service = rospy.ServiceProxy(self.srv_recognize, Recognition)
			req2 = RecognitionRequest()
			req2.running = False
			req2.doRecognition = False
			req2.display = False
			res2 = recognize_service(req2)
		except rospy.ServiceException, e:
			print "Service call failed: %s"%e
			return 'failed' 

		
		userdata.people = people
		return 'succeeded'
	

