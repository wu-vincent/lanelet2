cmake_minimum_required(VERSION 3.21)
project(lanelet2_validation)

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
file(GLOB_RECURSE PROJECT_SOURCE_FILES_SRC "${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp")

###########
## Build ##
###########
# Declare a cpp library
find_package(Boost REQUIRED)
add_library(${PROJECT_NAME} ${PROJECT_SOURCE_FILES_SRC})
target_include_directories(${PROJECT_NAME} PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/include")
target_link_libraries(${PROJECT_NAME} PUBLIC lanelet2_core lanelet2_io lanelet2_traffic_rules lanelet2_projection lanelet2_routing Boost::program_options)
if (NOT BUILD_SHARED_LIBS)
    set_target_properties(${PROJECT_NAME} PROPERTIES OUTPUT_NAME "${PROJECT_NAME}-static")
endif ()

# Add executables in "tools"
set(TOOL_TARGETS)
file(GLOB TOOL_DIRECTORIES RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}/tools" "${CMAKE_CURRENT_SOURCE_DIR}/tools/*")
foreach (TOOL_DIR ${TOOL_DIRECTORIES})
    if (IS_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/tools/${TOOL_DIR}")
        file(GLOB TOOL_SOURCES_FILES "${CMAKE_CURRENT_SOURCE_DIR}/tools/${TOOL_DIR}/*.cpp")
        add_executable(${TOOL_DIR} ${TOOL_SOURCES_FILES})
        target_link_libraries(${TOOL_DIR} PUBLIC lanelet2_validation)
        list(APPEND TOOL_TARGETS ${TOOL_DIR})
    endif ()
endforeach ()

if (NOT TOOL_TARGETS)
    # No subfolder found, add executable and python modules for tools folder
    file(GLOB TOOL_SOURCES_FILES "${CMAKE_CURRENT_SOURCE_DIR}/tools/*.cpp")
    add_executable("${PROJECT_NAME}_tool" ${TOOL_SOURCES_FILES})
    target_link_libraries("${PROJECT_NAME}_tool" PUBLIC lanelet2_validation)
    list(APPEND TOOL_TARGETS "${PROJECT_NAME}_tool")
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
    find_package(GTest REQUIRED)
    file(GLOB PROJECT_SOURCE_FILES_TEST "${CMAKE_CURRENT_SOURCE_DIR}/test/*.cpp")
    add_executable("${PROJECT_NAME}_test" ${PROJECT_SOURCE_FILES_TEST})
    target_link_libraries("${PROJECT_NAME}_test" PRIVATE GTest::gtest_main ${PROJECT_NAME})

    if (WIN32)
        add_custom_command(TARGET "${PROJECT_NAME}_test" POST_BUILD
                COMMAND ${CMAKE_COMMAND} -E copy_if_different "$<TARGET_RUNTIME_DLLS:${PROJECT_NAME}_test>" "$<TARGET_FILE_DIR:${PROJECT_NAME}_test>"
                COMMAND_EXPAND_LISTS)
    endif ()

    gtest_discover_tests("${PROJECT_NAME}_test")
    add_dependencies("${PROJECT_NAME}_test" lanelet2_maps)
endif ()