set(PCL_DIR "/path/to/PCLConfig.cmake")

cmake_minimum_required(VERSION 2.6 FATAL_ERROR)

project(correspondence_grouping)

find_package(PCL 1.5 REQUIRED)
find_package (Qt4 REQUIRED)
find_package (VTK REQUIRED)

include_directories(${PCL_INCLUDE_DIRS})
link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})

set (project_SOURCES main.cpp pclviewer.cpp keypoints.cpp CubeCreator.cpp)
set (project_HEADERS pclviewer.h keypoints.h CubeCreator.h)
set (project_FORMS pclviewer.ui)
set (VTK_LIBRARIES vtkRendering vtkGraphics vtkHybrid QVTK)

QT4_WRAP_CPP (project_HEADERS_MOC   ${project_HEADERS})
QT4_WRAP_UI (project_FORMS_HEADERS ${project_FORMS})


INCLUDE         (${QT_USE_FILE})
ADD_DEFINITIONS (${QT_DEFINITIONS})


#ADD_EXECUTABLE  (correspondence_grouping ${project_SOURCES}
#        ${project_FORMS_HEADERS}
#        ${project_HEADERS_MOC})

add_executable (correspondence_grouping correspondence_grouping.cpp correspGroup.cpp correspGroup.h test_class.cpp)
target_link_libraries (correspondence_grouping ${PCL_LIBRARIES})