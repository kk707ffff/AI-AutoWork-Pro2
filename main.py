import os
from core.planner import TaskPlanner
from core.executor import CodeExecutor 
from core.validator import ResultValidator
from openai import OpenAI

# 配置 DeepSeek API Key
API_KEY = "sk-7e82aac1ed674afdb66bb08bc83ccb51"

# 初始化客户端
client = OpenAI(
    api_key=API_KEY, 
    base_url="https://api.deepseek.com"
)
def run_workflow(user_input):
    planner = TaskPlanner(client)
    executor = CodeExecutor(client)
    validator = ResultValidator(client)
    print(f"🚀 正在拆解任务...")
    tasks = planner.decompose(user_input) 
    for task in tasks:
        print(f"🛠️ 正在执行步骤: {task}")

    # 2. 执行 Agent
    executor = CodeExecutor(client)
    final_code = ""
    for task in tasks:
        print(f"\n⚙️ 正在执行: {task}")
        code = executor.generate_code(task)
        final_code += code + "\n\n"

    # 3. 验证 Agent
    validator = ResultValidator(client)
    print("\n🔍 正在进行自动化验证...")
    is_valid, feedback = validator.run_test(final_code)
    
    if not is_valid:
        print(f"❌ 验证失败: {feedback}")
        print("🔄 尝试修复...")
        final_code = executor.fix_code(final_code, feedback)
    else:
        print(f"✅ 代码语法验证通过！")
    
    # 4. 产出结果
    output_file = "generated_solution.py"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_code)
    
    print(f"\n✨ 任务成功闭环！最终脚本已保存至: {output_file}")

if __name__ == "__main__":
    if API_KEY == "在此处填入你的_API_KEY":
        print("⚠️ 请先在 main.py 中配置你的 Gemini API Key！")
    else:
        # 升级为交互模式
        print("--- AI-AutoWork-Pro 交互模式已启动 ---")
        while True:
            user_input = input("\n请输入你想生成的工具任务 (输入 'quit' 退出): ")
            if user_input.lower() == 'quit':
                break
            if user_input.strip():
                run_workflow(user_input)
            else:
                print("请输入有效任务！")