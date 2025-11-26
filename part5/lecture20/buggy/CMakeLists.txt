cmake_minimum_required(VERSION 3.13)
project(BuggyReturnPass)

find_package(LLVM REQUIRED CONFIG)
list(APPEND CMAKE_MODULE_PATH "${LLVM_CMAKE_DIR}")
include_directories(${LLVM_INCLUDE_DIRS})
add_definitions(${LLVM_DEFINITIONS})

add_library(BuggyReturnPass MODULE BuggyReturnPass.cpp)
set_target_properties(BuggyReturnPass PROPERTIES
  PREFIX ""  # so it produces 'BuggyReturnPass.so' instead of 'lib...so'
)
llvm_map_components_to_libnames(llvm_libs)
target_link_libraries(BuggyReturnPass PRIVATE ${llvm_libs})

