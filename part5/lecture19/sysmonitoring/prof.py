import sys
import time
from collections import defaultdict

# 1. 准备工具 ID 和数据存储
PROF_ID = sys.monitoring.PROFILER_ID
stats = defaultdict(lambda: {"count": 0, "total_time": 0})
start_times = {}

# 2. 定义分析逻辑
def profile_start(code, instruction_offset):
    # 记录进入函数的时间
    # 使用 id(code) 作为 key 保证唯一性
    start_times[id(code)] = time.perf_counter_ns()

def profile_return(code, instruction_offset, retval):
    end_time = time.perf_counter_ns()
    start_time = start_times.pop(id(code), None)
    
    if start_time:
        duration = end_time - start_time
        name = code.co_name
        stats[name]["count"] += 1
        stats[name]["total_time"] += duration

# 3. 初始化监控
sys.monitoring.use_tool_id(PROF_ID, "MyProfiler")
sys.monitoring.register_callback(PROF_ID, sys.monitoring.events.PY_START, profile_start)
sys.monitoring.register_callback(PROF_ID, sys.monitoring.events.PY_RETURN, profile_return)

# 开启事件：函数开始、函数返回、以及 C 函数调用（可选）
sys.monitoring.set_events(PROF_ID, sys.monitoring.events.PY_START | sys.monitoring.events.PY_RETURN)

# --- 被测试的业务逻辑 ---
def heavy_task():
    time.sleep(0.1)
    return sum(range(10000))

def fast_task():
    return "done"

def main():
    for _ in range(3):
        heavy_task()
        fast_task()

main()

# 4. 关闭监控并打印结果
sys.monitoring.set_events(PROF_ID, 0)

print(f"{'函数名':<15} | {'调用次数':<10} | {'总耗时 (ms)':<10}")
print("-" * 40)
for func, data in stats.items():
    ms = data["total_time"] / 1_000_000
    print(f"{func:<15} | {data['count']:<10} | {ms:<10.2f}")

sys.monitoring.free_tool_id(PROF_ID)
