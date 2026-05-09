class TaskPlanner:
    def __init__(self, model="gemini-pro"):
        self.model = model

    def decompose(self, goal):
        # 模拟长链推理需求拆解
        return [
            f"步骤 1: 针对 '{goal}' 进行数据结构定义",
            f"步骤 2: 编写基于 Pandas 的数据清洗逻辑",
            f"步骤 3: 自动化生成单元测试脚本并验证结果"
        ]
