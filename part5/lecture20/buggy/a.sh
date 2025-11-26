#!/bin/bash

if [[ ! -e build ]]
then
    mkdir build
fi

cd build
cmake .. -DLLVM_DIR=/usr/lib/llvm-18/cmake/
make

csmith -s 23333 > a.c
clang -O0 -fpass-plugin=./BuggyReturnPass.so a.c -I /usr/include/csmith/ -o a 2> /dev/null
clang a.c -I /usr/include/csmith/ -o b 2> /dev/null
timeout 10 ./a > a.log
timeout 10 ./b > b.log
diff a.log b.log
