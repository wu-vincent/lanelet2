cmake_minimum_required(VERSION 3.21)
project(lanelet2_maps)

###########
## Build ##
###########
add_custom_target(${PROJECT_NAME})
add_custom_command(
        TARGET ${PROJECT_NAME}
        COMMAND ${CMAKE_COMMAND} -E copy_directory "${CMAKE_CURRENT_SOURCE_DIR}" "${CMAKE_CURRENT_BINARY_DIR}"
)