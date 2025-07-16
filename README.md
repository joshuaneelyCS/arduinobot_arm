# arduinobot_arm
A robot arm visualized by RViz and simulated in Gazebo using ROS2

To run the simulation, cd into the project folder. 

Run the terminal command

```
colcon build
. install/setup.bash
ros2 launch arduinobot_bringup simulated_robot.launch.py 
```

![image alt](https://github.com/joshuaneelyCS/arduinobot_arm/blob/main/Screenshot%202025-07-16%20at%2012.07.27%20PM.png?raw=true)

After running these commands, two windows should appear.
In RViz, plan and execute movements by dragging the directional ball slider to the desired
location and then click "plan and execute" in the menu.

The Gazebo menu will then move the arm to the desired location.
