cmake_minimum_required(VERSION 2.4.6)
include($ENV{ROS_ROOT}/core/rosbuild/rosbuild.cmake)

# Set the build type.  Options are:
#  Coverage       : w/ debug symbols, w/o optimization, w/ code-coverage
#  Debug          : w/ debug symbols, w/o optimization
#  Release        : w/o debug symbols, w/ optimization
#  RelWithDebInfo : w/ debug symbols, w/ optimization
#  MinSizeRel     : w/o debug symbols, w/ optimization, stripped binaries
#set(ROS_BUILD_TYPE RelWithDebInfo)

rosbuild_find_ros_package(actionlib_msgs)
include(${actionlib_msgs_PACKAGE_PATH}/cmake/actionbuild.cmake)
genaction()

rosbuild_init()

#set the default path for built executables to the "bin" directory
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)
#set the default path for built libraries to the "lib" directory
set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/lib)

#uncomment if you have defined messages
rosbuild_genmsg()
#uncomment if you have defined services
rosbuild_gensrv()

# Check for sse support
rosbuild_check_for_sse()
#set(SSE_FLAGS "-msse2 -mfpmath=sse")

#common commands for building c++ executables and libraries
#rosbuild_add_library(${PROJECT_NAME} src/example.cpp)
#target_link_libraries(${PROJECT_NAME} another_library)
#rosbuild_add_boost_directories()
#rosbuild_link_boost(${PROJECT_NAME} thread)
#rosbuild_add_executable(example examples/example.cpp)
#target_link_libraries(example ${PROJECT_NAME})
#rosbuild_add_executable(face_detector

#rosbuild_add_library(color_face_detector
#                       ros/src/color_face_detection.cpp 
#                       ros/src/faces.cpp)
#rosbuild_link_boost(color_face_detector thread)

#rosbuild_add_executable(face_detector
			#common/src/PeopleDetector.cpp
			#ros/src/people_detection.cpp)
rosbuild_add_library(face_detector
			common/src/PeopleDetector.cpp
			ros/src/face_detection.cpp)

rosbuild_add_library(people_detector
			ros/src/people_detection.cpp)
add_custom_command(TARGET people_detector POST_BUILD COMMAND mkdir -p ${PROJECT_SOURCE_DIR}/common/files/windows/TrainingData)

rosbuild_add_executable(people_detection_client
			ros/src/people_detection_action_client.cpp)

# modified openni tracker
#rosbuild_add_executable(openni_tracker ros/src/openni_tracker.cpp
#                                       ros/src/SceneDrawer.cpp)
			
#rosbuild_add_executable(ros_face_detector
			#common/src/CuiPeopleDetector.cpp
			#common/src/PeopleDetector.cpp
			#common/src/PeopleDetectorControlFlow.cpp
			#common/src/PeopleDetectorMain.cpp)

# add include search paths
INCLUDE_DIRECTORIES(${PROJECT_SOURCE_DIR}/ros/include
		    ${PROJECT_SOURCE_DIR}/common/include)

rosbuild_add_compile_flags(face_detector -D__LINUX__)
rosbuild_add_compile_flags(people_detector -D__LINUX__)
rosbuild_add_compile_flags(people_detection_client -D__LINUX__)

# rostest
#rosbuild_download_test_data(http://pr.willowgarage.com/data/face_detector/face_detector_noface_test_diamondback.bag face_detector_noface_test.bag 37f043be780a4511c853379defdd9855)
#rosbuild_download_test_data(http://pr.willowgarage.com/data/face_detector/face_detector_withface_test_diamondback.bag face_detector_withface_test.bag 59126117e049e69d577b7ee27251a6f8)
#rosbuild_add_rostest(ros/test/face_detector_true_rtest.xml)
#rosbuild_add_rostest(ros/test/face_detector_false_rtest.xml)

rosbuild_add_roslaunch_check(ros/launch)
