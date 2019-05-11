cmake_minimum_required(VERSION 2.8 FATAL_ERROR)
 
project(doStuff)
target_link_libraries (doStuff ${PCL_LIBRARIES})

#it seems it's needed only on OS X 10.9
#find_package(GLEW REQUIRED)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -I/usr/include -v")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x")
set (CMAKE_CXX_FLAGS "-std=gnu++0x")

find_package(PCL 1.7 REQUIRED)
 
include_directories(${PCL_INCLUDE_DIRS})
link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})

set(PCL_BUILD_TYPE Release)
 
file(GLOB PCL_openni_viewer_SRC
    "src/correspGroup/*.h"
    "src/correspGroup/*.cpp"
)

add_library(CorrespGroup SHARED src/correspGroup.cpp)

install(TARGETS CorrespGroup DESTINATION lib/)
install(FILES correspGroup.h DESTINATION include/)