import sys
import types

# 1. 定义 Tool ID (Python 3.12 允许 0-5 个 ID)
MY_DEBUGGER = sys.monitoring.DEBUGGER_ID
sys.monitoring.use_tool_id(MY_DEBUGGER, "MySimpleDebugger")
# 2. 定义回调函数
def on_line(code: types.CodeType, line_number: int):
    """每行代码执行时触发"""
    print(f"  [LINE] 执行行号: {line_number} | 函数: {code.co_name}")

def on_start(code: types.CodeType, instruction_offset: int):
    """进入函数时触发"""
    print(f"\n[START] >>> 进入函数: {code.co_name} (定义于 {code.co_filename})")

def on_return(code: types.CodeType, instruction_offset: int, retval: object):
    """函数返回时触发，可以看到返回值"""
    print(f"[RETURN] <<< 退出函数: {code.co_name} | 返回值: {retval}")

# 3. 注册回调
sys.monitoring.register_callback(MY_DEBUGGER, sys.monitoring.events.LINE, on_line)
sys.monitoring.register_callback(MY_DEBUGGER, sys.monitoring.events.PY_START, on_start)
sys.monitoring.register_callback(MY_DEBUGGER, sys.monitoring.events.PY_RETURN, on_return)

# 4. 开启监控事件
# 我们同时监听：行跳转、函数开始、函数返回
sys.monitoring.set_events(MY_DEBUGGER, 
    sys.monitoring.events.LINE | 
    sys.monitoring.events.PY_START | 
    sys.monitoring.events.PY_RETURN
)

# --- 被监控的测试代码 ---
def calculate_sum(a, b):
    result = a + b
    return result

def main():
    print("--- 逻辑开始 ---")
    val = calculate_sum(10, 20)
    print(f"--- 逻辑结束，结果: {val} ---")

# 执行测试
main()

# 5. 停止监控 (清理现场)
sys.monitoring.set_events(MY_DEBUGGER, 0)
