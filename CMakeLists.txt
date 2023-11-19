cmake_minimum_required(VERSION 3.5)
project(lanelet2)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED)

set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS TRUE)
if (MSVC)
    add_compile_definitions(_USE_MATH_DEFINES)
endif ()

option(LANELET2_ENABLE_TESTS "Build the testing tree." OFF)
if (LANELET2_ENABLE_TESTS)
    enable_testing()
endif ()


#include_directories(
#        lanelet2_core/include
#        lanelet2_io/include
#        lanelet2_projection/include
#        lanelet2_traffic_rules/include
#        lanelet2_routing/include
#        lanelet2_validation/include)

add_subdirectory(lanelet2_core)
add_subdirectory(lanelet2_io)
#add_subdirectory(lanelet2_projection)
#add_subdirectory(lanelet2_traffic_rules)
#add_subdirectory(lanelet2_routing)
#add_subdirectory(lanelet2_validation)
#add_subdirectory(lanelet2_examples)
#add_subdirectory(lanelet2_python)
#add_subdirectory(lanelet2_maps)
#add_subdirectory(lanelet2_matching)

#target_link_libraries(lanelet2_io PUBLIC lanelet2_core)
#target_link_libraries(lanelet2_projection PUBLIC lanelet2_core)
#target_link_libraries(lanelet2_traffic_rules PUBLIC lanelet2_core)
#target_link_libraries(lanelet2_routing PUBLIC lanelet2_core lanelet2_traffic_rules)
#target_link_libraries(lanelet2_matching PUBLIC lanelet2_core lanelet2_traffic_rules lanelet2_io lanelet2_projection lanelet2_maps)
#target_link_libraries(lanelet2_validation PUBLIC lanelet2_core lanelet2_io lanelet2_routing lanelet2_traffic_rules lanelet2_projection)
#target_link_libraries(lanelet2_examples_compiler_flags INTERFACE lanelet2_core lanelet2_io lanelet2_routing lanelet2_traffic_rules lanelet2_projection lanelet2_matching)
#target_link_libraries(lanelet2_python_compiler_flags INTERFACE lanelet2_core lanelet2_io lanelet2_routing lanelet2_traffic_rules lanelet2_projection lanelet2_matching)