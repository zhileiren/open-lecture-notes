import sys
from sys import monitoring

ID = 1
# 维护全局缩进深度
class TraceState:
    depth = 0

state = TraceState()

# 1. 统一定义回调函数
def on_start(code, offset):
    indent = "│  " * state.depth
    frame = sys._getframe(1)
    
    # 捕获参数
    arg_names = code.co_varnames[:code.co_argcount]
    params = {name: frame.f_locals.get(name) for name in arg_names}
    
    # 捕获闭包变量 (Free Variables)
    free_vars = code.co_freevars
    closures = {name: frame.f_locals.get(name) for name in free_vars} if free_vars else {}

    print(f"{indent}├── ➔ {code.co_name}({params})")
    if closures:
        print(f"{indent}│   [闭包]: {closures}")
    
    state.depth += 1

def on_return(code, offset, retval):
    state.depth -= 1
    indent = "│  " * state.depth
    print(f"{indent}└── ⬅ {code.co_name} 返回: {retval}")

# 2. 初始化监控（只做一次）
try:
    monitoring.use_tool_id(ID, "debugger")
except ValueError:
    pass # 如果 ID 已被占用

monitoring.register_callback(ID, monitoring.events.PY_START, on_start)
monitoring.register_callback(ID, monitoring.events.PY_RETURN, on_return)

# 3. 定义装饰器
def trace(func):
    # 在装饰阶段就开启该函数的监控
    # 这样无论是直接调用还是递归，都能被捕获
    events = monitoring.events.PY_START | monitoring.events.PY_RETURN
    monitoring.set_local_events(ID, func.__code__, events)
    
    # 注意：这里我们不需要 inner 逻辑来开关监控了
    # 直接返回原函数即可，因为监控是挂在 code 对象上的
    return func

# --- 测试多个函数 ---

@trace
def multiply(a, b):
    return a * b

@trace
def factorial(n):
    if n <= 1:
        return multiply(1, 1)
    return multiply(n, factorial(n - 1))

def outer_wrapper(bonus):
    @trace
    def inner_calc(x):
        return x + bonus
    return inner_calc

# 执行测试
print("开始追踪多函数调用：")
calc_with_bonus = outer_wrapper(100)
factorial(3)
calc_with_bonus(5)

# 清理
# monitoring.free_tool_id(ID)
