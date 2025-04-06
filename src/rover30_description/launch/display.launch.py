import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import Command, LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

from launch.actions import TimerAction
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    rover30_description_dir = get_package_share_directory("rover30_description")

    model_arg = DeclareLaunchArgument(name="model", default_value=os.path.join(
                                        rover30_description_dir, "urdf", "rover30.urdf.xacro"
                                        ),
                                      description="Absolute path to robot urdf file")

    robot_description = ParameterValue(Command(["xacro ", LaunchConfiguration("model")]),
                                       value_type=str)

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}]
    )

    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui"
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", os.path.join(rover30_description_dir, "rviz", "display.rviz")],
    )

    gzserver_process = ExecuteProcess(
        cmd=["gzserver", "--verbose"],
        output="screen"
    )

    gzclient_process = ExecuteProcess(
        cmd=["gzclient"],
        output="screen"
    )

    spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-topic", "robot_description",
            "-entity", "rover30",
            "-x", "0", "-y", "0", "-z", "0.1"
        ],
        output="screen"
    )

    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
             )


    return LaunchDescription([
        model_arg,
        joint_state_publisher_gui_node,
        robot_state_publisher_node,
        gzserver_process,
        gzclient_process,
        TimerAction(
            period=3.0,
            actions=[spawn_entity]
        ),
        #gazebo,
        #spawn_entity,
        #TimerAction(
        #    period=60.0,
        #    actions=[spawn_entity]
        #),
        rviz_node

    ])