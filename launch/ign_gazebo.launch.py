from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir, LaunchConfiguration, Command
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

from launch.actions import TimerAction

def generate_launch_description():
    #Environment variables
    pkg_path = get_package_share_directory("gr_description")
    
    # Assuming models are inside a models folder in your package
    models_path = os.path.join(pkg_path, 'models')

    # Set Ignition resource paths
    ign_resource_path = SetEnvironmentVariable(
        name='IGN_GAZEBO_RESOURCE_PATH',
        value=f"{models_path}:" + os.environ.get('IGN_GAZEBO_RESOURCE_PATH', '')
    )

    # Set the plugin path
    set_plugin_path = SetEnvironmentVariable(
        name='IGN_GAZEBO_SYSTEM_PLUGIN_PATH',
        value='/usr/lib/x86_64-linux-gnu/ign-gazebo-6/plugins:' + os.environ.get('IGN_GAZEBO_SYSTEM_PLUGIN_PATH', '')
    )

    # Launch ignition fortress
    simulation_world_file_path = os.path.join(pkg_path, "worlds/my_world2.sdf")
    ign_launch = ExecuteProcess(
        cmd=['ign', 'gazebo', '-v', '4','-r', simulation_world_file_path],
        output='screen'
    )

    # # Spawn the model (delayed to ensure Gazebo is ready)
    # # Path to the SDF.xacro file
    # sdf_xacro_file = os.path.join(pkg_path, "sdf", "gr_p247.sdf.xacro")

    # # Generate the SDF file from Xacro
    # generated_sdf_file = os.path.join(pkg_path, "sdf", "gr_p247.generated.sdf")

    # # Command to generate the SDF file
    # generate_sdf_cmd = ExecuteProcess(
    #     cmd=["xacro", sdf_xacro_file, ">>", generated_sdf_file],
    #     output="screen",
    # )

    # spawn_model_cmd = TimerAction(
    #     period=5.0,  # Delay in seconds
    #     actions=[
    #         Node(
    #             package="ros_ign_gazebo",
    #             executable="create",
    #             arguments=[
    #                 "-name", "my_robot",
    #                 "-allow_renaming", "true",
    #                 "-file", generated_sdf_file,
    #             ],
    #             output="screen",
    #         )
    #     ],
    # )


    # # Load the URDF file
    urdf_file = os.path.join(pkg_path, 'models', 'gr_robot', 'model_urdf.urdf')
    with open(urdf_file, "r") as f:
        description = f.read()
    
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name="robot_state_publisher",
        output="screen",
        parameters=[{'robot_description': description, "use_sim_time": True}],
        # remappings=[("/robot_description", "/gr_robot/gr_description")]
    )

    bridge_params = os.path.join(
        pkg_path,
        'params',
        'ignition_bridge.yaml'
    )

    start_gazebo_ros_bridge_cmd = Node(
        package='ros_ign_bridge',
        executable='parameter_bridge',
        arguments=['--ros-args', '-p', f'config_file:={bridge_params}'],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    odom_tf_node = Node(
        package='odom_frame_gen',
        executable='odom_frame_node',
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    return LaunchDescription([
        ign_resource_path,
        set_plugin_path,
        # generate_sdf_cmd,
        ign_launch,
        # spawn_model_cmd,
        TimerAction(period=2.0, actions=[robot_state_publisher_node]),  # Delay to ensure Gazebo is ready
        start_gazebo_ros_bridge_cmd,
        TimerAction(period=2.0, actions=[odom_tf_node])
    ])
