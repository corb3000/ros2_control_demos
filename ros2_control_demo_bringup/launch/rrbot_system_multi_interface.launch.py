# Copyright 2021 Department of Engineering Cybernetics, NTNU.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, ThisLaunchFileDir


def generate_launch_description():
    # Declare arguments
    declared_arguments = []
    declared_arguments.append(
        DeclareLaunchArgument(
            "prefix",
            default_value='""',
            description="Prefix of the joint names, useful for \
        multi-robot setup. If changed than also joint names in the controllers' configuration \
        have to be updated.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "slowdown", default_value="50.0", description="Slowdown factor of the RRbot."
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "robot_controller",
            default_value="forward_velocity_controller",
            description="Robot controller to start.",
        )
    )

    # Initialize Arguments
    prefix = LaunchConfiguration("prefix")
    slowdown = LaunchConfiguration("slowdown")
    robot_controller = LaunchConfiguration("robot_controller")

    base_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([ThisLaunchFileDir(), "/rrbot_base.launch.py"]),
        launch_arguments={
            "controllers_file": "rrbot_multi_interface_forward_controllers.yaml",
            "description_file": "rrbot_system_multi_interface.urdf.xacro",
            "prefix": prefix,
            "use_fake_hardware": "false",
            "mock_sensor_commands": "false",
            "slowdown": slowdown,
            "robot_controller": robot_controller,
        }.items(),
    )

    return LaunchDescription(declared_arguments + [base_launch])
