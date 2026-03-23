from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
import os
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    ld = LaunchDescription()

    rviz_inc = IncludeLaunchDescription(PythonLaunchDescriptionSource(PathJoinSubstitution([
        FindPackageShare("gr_description"), "launch", "rviz.launch.py"]
    )))

    print("pass 1")

    # Include gazebo Fortress launch file.
    ign_inc =IncludeLaunchDescription(PythonLaunchDescriptionSource(PathJoinSubstitution([
        FindPackageShare("gr_description"), "launch", "ign_gazebo.launch.py"]
    )))   

    teleop = ExecuteProcess(
            cmd=["xterm", "-e", "ros2", "run", "teleop_twist_keyboard", "teleop_twist_keyboard", '--ros-args', '-r', '/cmd_vel:=/cmd_vel'],
            output="screen",
            shell=True
    )

    print("pass 2")

    # Launch them all!
    return LaunchDescription([
        rviz_inc,
        ign_inc,
        teleop
    ])