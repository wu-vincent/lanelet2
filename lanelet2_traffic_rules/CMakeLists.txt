cmake_minimum_required(VERSION 3.21)
project(lanelet2_traffic_rules)

###################
## Find packages ##
###################
find_package(GTest REQUIRED)

########################
## Add python modules ##
########################
# Add python modules if located under src/{PROJECT_NAME)

############################
## Read source code files ##
############################
file(GLOB PROJECT_SOURCE_FILES_SRC "${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp")

###########
## Build ##
###########
# Declare a cpp library
add_library(${PROJECT_NAME} ${PROJECT_SOURCE_FILES_SRC})
target_include_directories(${PROJECT_NAME} PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/include")
target_link_libraries(${PROJECT_NAME} PUBLIC lanelet2_core)
if (NOT BUILD_SHARED_LIBS)
    set_target_properties(${PROJECT_NAME} PROPERTIES OUTPUT_NAME "${PROJECT_NAME}-static")
endif ()

#############
## Install ##
#############
# Install all targets, headers by default and scripts and other files if specified (folders or files).
if (NOT DEFINED SKBUILD)
    include(GNUInstallDirs)
    install(TARGETS ${PROJECT_NAME}
            ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
            LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
            RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
    install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
endif ()

#############
## Testing ##
#############
# Add test targets for cpp and python tests
if (NOT BUILD_TESTING STREQUAL OFF)
    include(GoogleTest)
    file(GLOB PROJECT_SOURCE_FILES_TEST "${CMAKE_CURRENT_SOURCE_DIR}/test/*.cpp")
    add_executable("${PROJECT_NAME}_test" ${PROJECT_SOURCE_FILES_TEST})
    target_link_libraries("${PROJECT_NAME}_test" PRIVATE GTest::gtest_main ${PROJECT_NAME})

    if (WIN32)
        add_custom_command(TARGET "${PROJECT_NAME}_test" POST_BUILD
                COMMAND ${CMAKE_COMMAND} -E copy_if_different "$<TARGET_RUNTIME_DLLS:${PROJECT_NAME}_test>" "$<TARGET_FILE_DIR:${PROJECT_NAME}_test>"
                COMMAND_EXPAND_LISTS)
    endif ()

    gtest_discover_tests("${PROJECT_NAME}_test")
endif ()