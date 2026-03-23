This folder is a copy of the urdf folder given BY Génération robot but translated into .sdf format. It use xacro too.

But this convertion is not fully terminated :

- First, the ```xml <pose></pose>``` tag for all visual and collision are not setup. This poses are not relative like in urdf format and by lack of time we have decided to simplify the model to only necessary elements.
- Second, only a few files have been converted:
  - a part of gr_p347.sdf.xacro
  - agilex/scout/scout_mini_wheel.sdf.xacro
  - agilex/scout/scout_mini.gazebo
  - agilex/scout/scout _mini.sdf
  - accessories/_d435.gazebo.xacro
  - accessories/_d435.sdf.xacro
  - accessories/gr_ros_kit.sdf.xacro
  - accessories/gps.sdf.xacro
  - accessories/helios_16.sdf.xacro
  - accessories/phidget_spatial.sdf.xacro

To Convert a file in sdf or urdf you can look at the following .md file: [Notes.md](../../../Notes.md)
