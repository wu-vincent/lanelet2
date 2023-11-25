cmake_minimum_required(VERSION 3.21)
project(lanelet2_examples)

###################
## Find packages ##
###################
find_package(lanelet2 CONFIG REQUIRED)

###########
## Build ##
###########
# Add executables in "src"
set(SRC_TARGETS)
file(GLOB SRC_DIRECTORIES RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}/src" "${CMAKE_CURRENT_SOURCE_DIR}/src/*")
foreach (SRC_DIR ${SRC_DIRECTORIES})
    if (IS_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/src/${SRC_DIR}")
        file(GLOB SRC_SOURCES_FILES "${CMAKE_CURRENT_SOURCE_DIR}/src/${SRC_DIR}/*.cpp")
        add_executable(${SRC_DIR} ${SRC_SOURCES_FILES})
        target_link_libraries(${SRC_DIR} PUBLIC lanelet2::lanelet2)
        list(APPEND SRC_TARGETS ${SRC_DIR})
    endif ()
endforeach ()

if (NOT SRC_TARGETS)
    # No subfolder found, add executable and python modules for src folder
    file(GLOB SRC_SOURCES_FILES "${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp")
    add_executable("${PROJECT_NAME}" ${SRC_SOURCES_FILES})
    target_link_libraries("${PROJECT_NAME}" PUBLIC lanelet2::lanelet2)
    list(APPEND SRC_TARGETS "${PROJECT_NAME}")
endif ()