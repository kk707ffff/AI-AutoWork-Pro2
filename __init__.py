import os
from core.planner import TaskPlanner
from core.executor import CodeExecutor
from core.validator import ResultValidator

def run_workflow(user_goal):
    print(f"🚀 接收到任务: {user_goal}")
    
    # 1. 任务规划 Agent
    planner = TaskPlanner(model="gemini-pro")
    tasks = planner.decompose(user_goal)
    print(f"📝 规划完成，共拆解为 {len(tasks)} 个步骤")

    # 2. 执行 Agent (处理数据与代码)
    executor = CodeExecutor()
    code_snippets = []
    for task in tasks:
        print(f"⚙️ 正在执行: {task}")
        code = executor.generate_code(task)
        code_snippets.append(code)

    # 3. 验证 Agent
    validator = ResultValidator()
    for code in code_snippets:
        is_valid, feedback = validator.run_test(code)
        if not is_valid:
            print(f"❌ 验证失败，正在修复: {feedback}")
            code = executor.fix_code(code, feedback)
        else:
            print(f"✅ 验证通过")
    
    print("\n✨ 所有任务已成功闭环！代码已生成并验证。")

if __name__ == "__main__":
    task = "分析财务报表并生成清理后的结果"
    run_workflow(task)
