cmake_minimum_required(VERSION 3.5)
project(arduinobot_controller)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(trajectory_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)

add_executable(slider_control src/slider_control.cpp)
ament_target_dependencies(slider_control rclcpp trajectory_msgs sensor_msgs)

ament_python_install_package(${PROJECT_NAME})

install(
  DIRECTORY config launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()