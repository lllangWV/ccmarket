# ROS 2 with Pixi Reference

## Project Setup

Initialize a ROS 2 workspace with RoboStack channels:

```bash
pixi init my_ros2_project -c robostack-humble -c conda-forge
cd my_ros2_project
```

## Adding Dependencies

### Core ROS 2 Packages

```bash
pixi add ros-humble-desktop ros-humble-turtlesim
```

### Python Development

```bash
pixi add colcon-common-extensions "setuptools<=58.2.0"
```

### C++ Development

```bash
pixi add ros-humble-ament-cmake-auto compilers pkg-config cmake ninja
```

## Configuration

### Basic pixi.toml

```toml
[workspace]
channels = ["robostack-humble", "conda-forge"]
platforms = ["linux-64", "osx-arm64", "win-64"]

[dependencies]
ros-humble-desktop = "*"
ros-humble-turtlesim = "*"
colcon-common-extensions = "*"
"setuptools<=58.2.0" = "*"
```

### Activation Scripts (After Colcon Build)

**Linux/macOS:**
```toml
[activation]
scripts = ["install/setup.sh"]
```

**Windows:**
```toml
[activation]
scripts = ["install/setup.bat"]
```

**Cross-platform:**
```toml
[target.linux.activation]
scripts = ["install/setup.sh"]

[target.osx.activation]
scripts = ["install/setup.sh"]

[target.win.activation]
scripts = ["install/setup.bat"]
```

## Running Applications

```bash
# Direct execution
pixi run ros2 run turtlesim turtlesim_node

# Interactive shell
pixi shell
ros2 run turtlesim turtlesim_node
```

## Task Management

### Define Tasks

```bash
pixi task add sim "ros2 run turtlesim turtlesim_node"
pixi task add build "colcon build --symlink-install"
pixi task add hello "ros2 run my_package my_node"
```

### Advanced Task Configuration

```toml
[tasks]
build = "colcon build --symlink-install"
build-ninja = "colcon build --cmake-args -G Ninja"

[tasks.hello]
cmd = "ros2 run my_package my_node"
depends-on = ["build"]

[tasks.test]
cmd = "colcon test"
cwd = "src"
inputs = ["src/**/*.py", "src/**/*.cpp"]
outputs = ["build/", "install/"]
```

## Creating Custom Packages

### Python Package

```bash
pixi run ros2 pkg create --build-type ament_python --destination-directory src my_package
pixi run colcon build
```

### C++ Package

```bash
pixi run ros2 pkg create --build-type ament_cmake --destination-directory src my_cpp_package
pixi run colcon build --cmake-args -G Ninja
```

## Important Notes

- **rosdep unavailable:** Pixi doesn't support `rosdep` - add packages manually via `pixi add`
- **Channel order matters:** Always list `robostack-humble` before `conda-forge`
- **RoboStack docs:** See [robostack.github.io](https://robostack.github.io/) for package availability

## Troubleshooting

### Package Not Found

Search for the correct package name:
```bash
pixi search ros-humble-*
```

RoboStack packages follow the pattern: `ros-{distro}-{package-name}`

### Build Failures

Ensure colcon and build tools are installed:
```bash
pixi add colcon-common-extensions cmake ninja
```

### Environment Not Activated

After building, register the setup script in `pixi.toml` activation section to auto-source your workspace.
