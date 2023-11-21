cmake_minimum_required(VERSION 3.5.1)
project(lanelet2_maps)

###########
## Build ##
###########
add_custom_target(${PROJECT_NAME})
add_custom_command(
        TARGET ${PROJECT_NAME}
        COMMAND ${CMAKE_COMMAND} -E copy_directory "${CMAKE_CURRENT_SOURCE_DIR}" "${CMAKE_CURRENT_BINARY_DIR}"
)

#############
## Install ##
#############
# Install all targets, headers by default and scripts and other files if specified (folders or files).
# This command also exports libraries and config files for dependent packages and this supersedes catkin_package.
install(DIRECTORY res/ DESTINATION "res/")
install(DIRECTORY josm/ DESTINATION "res/" PATTERN ".gitignore" EXCLUDE)
