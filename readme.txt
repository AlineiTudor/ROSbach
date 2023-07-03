Prerequisites:
	- bluerov_ros_playground (tutorial and package at: https://github.com/patrickelectric/bluerov_ros_playground) 				==>check prerequisites for bluerov_ros_playground
	- robot_localization (http://wiki.ros.org/robot_localization)
	- mavros (http://wiki.ros.org/mavros)

For camera set-up and prerequisites ask David Rete.

Usage:
	!!!! The main package is rov_tf_tree. !!!!
*****don't forget to: "source devel/setup.sh"*************

Posisiton estimation using data from camera (only xy position):
	roslaunch rov_tf_tree pos_est_valid_camera.launch
	You can use it by playing a rosbag where you recorded camera position on a topic called: "/BlueRov2/plane" (it also records the state estimate so if you don't want to record any data, delete the line using "rosbag record" in the above launchfile).

Position estimation using IMU+camera+barometer:
	roslaunch rov_tf_tree pos_est_valid.launch
	It starts the EKF, reads data from camera, imu and barometer and produces the state estimate on the topic /odometry/filtered. It also records depth, estimated depth, imu data, all mavlink messages (on /mavlink/from), and estimated xy coords. (you can delete/comment the record line if needed)

Position estimation using IMU+Barometer:
	roslaunch rov_tf_tree pos_est_valid.launch
	Position estimation using IMU acceleration and barometer pressure.

Important launchfile:
	brov_tf_tree.launch
	It contains the tf tree. It is launched automatically in the above launchfiles (no need to do it separately)

Important nodes:
	Bar30_read.py ==> reads, decodes and converts barometer messages sent via mavlink to depth.
	IMU_comp_bias.py ==>reads imu data, does the bias compensation and data preprocessing and posts new imu mesage (also writes to file sensor bias, gravity bias etc so comment those lines or change file path if needed)
	color2_odom.py ==> gets data from external camera and creates xy measurement message (Needs camera connection to be on: ask David Rete for details if needed)

In BagFiles folder you can find recorded data and additional scripts for data filtering(mean, moving avg, running avg), data preprocessing (changing coord frames for imu or camera data), noise standard deviation computing.

For more details ask Alinei Tudor (tudor_alinei@yahoo.com).


BlueROV2 hardware description:
	https://bluerobotics.com/learn/bluerov2-assembly/#introduction
Configure BlueROV2 to work woth your computer (software config) (see guide for your Operating system):
	https://bluerobotics.com/learn/bluerov2-software-setup/
