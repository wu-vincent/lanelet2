cmake_minimum_required(VERSION 3.21)
project(lanelet2_python)

###################
## Find packages ##
###################
find_package(Boost REQUIRED COMPONENTS python)
find_package(PythonLibs REQUIRED)

########################
## Build python modules ##
########################
file(GLOB PROJECT_PYTHON_SOURCE_FILES_SRC "${CMAKE_SOURCE_DIR}/python_api/*.cpp")
foreach (PROJECT_PYTHON_SOURCE_FILE ${PROJECT_PYTHON_SOURCE_FILES_SRC})
    get_filename_component(PYTHON_MODULE_NAME ${PROJECT_PYTHON_SOURCE_FILE} NAME_WE)
    add_library(${PYTHON_MODULE_NAME} SHARED ${PROJECT_PYTHON_SOURCE_FILE})
    target_include_directories(${PYTHON_MODULE_NAME} PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/include")
    set_target_properties(${PYTHON_MODULE_NAME} PROPERTIES PREFIX "")
endforeach ()

#############
## Install ##
#############
# Install all targets, headers by default and scripts and other files if specified (folders or files).


#############
## Testing ##
#############
# Add test targets for cpp and python tests
