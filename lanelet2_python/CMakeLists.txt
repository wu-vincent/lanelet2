cmake_minimum_required(VERSION 3.21)
project(lanelet2_python)

###################
## Find packages ##
###################
find_package(Boost REQUIRED COMPONENTS python)
find_package(Python REQUIRED COMPONENTS Interpreter Development.Module REQUIRED)

##########################
## Build python modules ##
##########################
set(PROJECT_PYTHON_TARGETS)
file(GLOB PROJECT_PYTHON_SOURCE_FILES_SRC "${CMAKE_CURRENT_SOURCE_DIR}/python_api/*.cpp")
foreach (PROJECT_PYTHON_SOURCE_FILE ${PROJECT_PYTHON_SOURCE_FILES_SRC})
    get_filename_component(PYTHON_MODULE_NAME ${PROJECT_PYTHON_SOURCE_FILE} NAME_WE)
    python_add_library(${PYTHON_MODULE_NAME} MODULE ${PROJECT_PYTHON_SOURCE_FILE} WITH_SOABI)
    list(APPEND PROJECT_PYTHON_TARGETS ${PYTHON_MODULE_NAME})

    target_compile_definitions(${PYTHON_MODULE_NAME} PRIVATE -DPYTHON_API_MODULE_NAME=${PYTHON_MODULE_NAME})
    target_include_directories(${PYTHON_MODULE_NAME} PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/include")
    target_include_directories(${PYTHON_MODULE_NAME} PRIVATE ${Python3_INCLUDE_DIRS})
    target_link_libraries(${PYTHON_MODULE_NAME} PUBLIC Boost::python lanelet2_core lanelet2_io lanelet2_projection lanelet2_traffic_rules lanelet2_routing lanelet2_matching)
endforeach ()

#############
## Install ##
#############
# Install all python modules into /lanelet2 if CMake is running inside scikit-build-core
if (DEFINED SKBUILD)
    install(TARGETS ${PROJECT_PYTHON_TARGETS} DESTINATION "lanelet2")

    # Install built targets to build/lib for repairing wheels with auditwheel and delocate
    install(TARGETS lanelet2_core lanelet2_io lanelet2_projection lanelet2_traffic_rules lanelet2_routing lanelet2_matching DESTINATION "${CMAKE_SOURCE_DIR}/build/lib")

    if (WIN32)
        # Bundle shared library dependencies on Windows
        foreach (PROJECT_PYTHON_TARGET ${PROJECT_PYTHON_TARGETS})
            install(FILES "$<TARGET_RUNTIME_DLLS:${PROJECT_PYTHON_TARGET}>" DESTINATION "bin")
        endforeach ()
    endif ()
else ()
    install(DIRECTORY scripts/ DESTINATION "scripts")
endif ()

