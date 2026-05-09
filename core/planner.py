class TaskPlanner:
    def __init__(self, client):
        self.client = client  # 接收从 main.py 传来的 DeepSeek 客户端

    def decompose(self, user_goal):
        prompt = f"你是一个高级架构师，请将任务：'{user_goal}' 拆解为 3 个具体的 Python 开发步骤。"
        # 换成 DeepSeek 的调用方式
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}]
        )
        # 返回 AI 的文字内容
        return response.choices[0].message.content.split('\n')