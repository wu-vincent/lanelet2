#set(MRT_PKG_VERSION 4.0.0)
# Modify only if you know what you are doing!
cmake_minimum_required(VERSION 3.5.1)
project(lanelet2_routing)

###################
## Find packages ##
###################
#find_package(mrt_cmake_modules REQUIRED)
#include(UseMrtStdCompilerFlags)
#include(GatherDeps)

# You can add a custom.cmake in order to add special handling for this package. E.g. you can do:
# list(REMOVE_ITEM DEPENDEND_PACKAGES <package name 1> <package name 2> ...)
# To remove libs which cannot be found automatically. You can also "find_package" other, custom dependencies there.
# You can also set PROJECT_INSTALL_FILES to install files that are not installed by default.
#if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/custom.cmake")
#    include("${CMAKE_CURRENT_SOURCE_DIR}/custom.cmake")
#endif()
#
#find_package(AutoDeps REQUIRED COMPONENTS ${DEPENDEND_PACKAGES})
#
#mrt_parse_package_xml()

########################
## Add python modules ##
########################
# This adds a python module if located under src/{PROJECT_NAME)
#mrt_python_module_setup()
#
#mrt_glob_files(PROJECT_PYTHON_SOURCE_FILES_SRC "python_api/*.cpp")
#if (PROJECT_PYTHON_SOURCE_FILES_SRC)
#    # Add a cpp-python api library. Make sure there are no name collisions with python modules in this project
#    mrt_add_python_api( ${PROJECT_NAME}
#        FILES ${PROJECT_PYTHON_SOURCE_FILES_SRC}
#        )
#endif()

############################
## Read source code files ##
############################
#mrt_glob_files_recurse(PROJECT_HEADER_FILES_INC "include/*.h" "include/*.hpp" "include/*.cuh")
#mrt_glob_files(PROJECT_SOURCE_FILES_INC "src/*.h" "src/*.hpp" "src/*.cuh")
#mrt_glob_files(PROJECT_SOURCE_FILES_SRC "src/*.cpp" "src/*.cu")
file(GLOB PROJECT_SOURCE_FILES_SRC "${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp")

###########
## Build ##
###########
# Declare a cpp library
#mrt_add_library(${PROJECT_NAME}
#    INCLUDES ${PROJECT_HEADER_FILES_INC} ${PROJECT_SOURCE_FILES_INC}
#    SOURCES ${PROJECT_SOURCE_FILES_SRC}
#    )
find_package(Boost REQUIRED)
add_library(${PROJECT_NAME} SHARED ${PROJECT_SOURCE_FILES_SRC})
target_include_directories(${PROJECT_NAME} PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/include")
target_link_libraries(${PROJECT_NAME} PUBLIC lanelet2_core lanelet2_traffic_rules Boost::filesystem)

#############
## Install ##
#############
# Install all targets, headers by default and scripts and other files if specified (folders or files).
# This command also exports libraries and config files for dependent packages and this supersedes catkin_package.
#mrt_install(PROGRAMS scripts FILES res data ${PROJECT_INSTALL_FILES})
install(TARGETS ${PROJECT_NAME}
        ARCHIVE DESTINATION ${PROJECT_INSTALL_FILES}
        LIBRARY DESTINATION ${PROJECT_INSTALL_FILES}
        RUNTIME DESTINATION ${PROJECT_INSTALL_FILES})

#############
## Testing ##
#############
# Add test targets for cpp and python tests
#if (CATKIN_ENABLE_TESTING)
#    mrt_add_tests(test)
#    mrt_add_nosetests(test)
#endif()
if (LANELET2_ENABLE_TESTING)
    include(GoogleTest)
    find_package(GTest REQUIRED)
    file(GLOB PROJECT_SOURCE_FILES_TEST "${CMAKE_CURRENT_SOURCE_DIR}/test/*.cpp")
    add_executable("${PROJECT_NAME}_test" ${PROJECT_SOURCE_FILES_TEST})
    target_link_libraries("${PROJECT_NAME}_test" PRIVATE GTest::gtest_main ${PROJECT_NAME})

    add_custom_command(TARGET "${PROJECT_NAME}_test" POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E copy_if_different "$<TARGET_FILE:lanelet2_core>" "$<TARGET_FILE_DIR:${PROJECT_NAME}_test>"
            COMMAND ${CMAKE_COMMAND} -E copy_if_different "$<TARGET_FILE:lanelet2_traffic_rules>" "$<TARGET_FILE_DIR:${PROJECT_NAME}_test>")

    gtest_discover_tests("${PROJECT_NAME}_test")
    add_dependencies("${PROJECT_NAME}_test" lanelet2_maps)
endif ()