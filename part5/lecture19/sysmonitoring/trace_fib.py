#!/usr/bin/env python3
# coding: utf-8

from sys import monitoring
indent = 0

def on_start(code, offset):
    global indent
    indent += 1
    print(f"{indent * '>'} entering function: {code.co_name}")

def on_return(code, offset, retval):
    global indent
    print(f"{indent * '<'} leaving function: {code.co_name}, with return value: {retval}")
    indent -= 1

debugger = monitoring.use_tool_id(monitoring.DEBUGGER_ID, "debugger")
monitoring.register_callback(monitoring.DEBUGGER_ID, monitoring.events.PY_START, on_start)
monitoring.register_callback(monitoring.DEBUGGER_ID, monitoring.events.PY_RETURN, on_return)

def fib(bar):
    if bar <= 2:
        return 1
    else:
        return fib(bar - 1) + fib(bar - 2)

monitoring.set_events(monitoring.DEBUGGER_ID, monitoring.events.PY_START |
                                              monitoring.events.PY_RETURN)
fib(10)
monitoring.set_events(monitoring.DEBUGGER_ID, 0)
monitoring.free_tool_id(monitoring.DEBUGGER_ID)
