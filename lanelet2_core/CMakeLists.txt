cmake_minimum_required(VERSION 3.21)
project(lanelet2_core)

###################
## Find packages ##
###################
find_package(Boost REQUIRED)
find_package(Eigen3 REQUIRED)
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
add_library(${PROJECT_NAME} SHARED ${PROJECT_SOURCE_FILES_SRC})
target_include_directories(${PROJECT_NAME} PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/include")
target_link_libraries(${PROJECT_NAME} PUBLIC Boost::headers Eigen3::Eigen)

#############
## Install ##
#############
# Install all targets, headers by default and scripts and other files if specified (folders or files).
include(GNUInstallDirs)
install(TARGETS ${PROJECT_NAME}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
install(DIRECTORY doc/ DESTINATION "doc/${PROJECT_NAME}")
install(DIRECTORY scripts/ DESTINATION "scripts/")

#############
## Testing ##
#############
# Add test targets for cpp and python tests
if (LANELET2_ENABLE_TESTING)
    include(GoogleTest)
    file(GLOB PROJECT_SOURCE_FILES_TEST "${CMAKE_CURRENT_SOURCE_DIR}/test/*.cpp")
    add_executable("${PROJECT_NAME}_test" ${PROJECT_SOURCE_FILES_TEST})
    target_link_libraries("${PROJECT_NAME}_test" PRIVATE GTest::gtest_main ${PROJECT_NAME})
    gtest_discover_tests("${PROJECT_NAME}_test")
endif ()
