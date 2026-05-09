class CodeExecutor:
    def __init__(self, client):
        # 接收从 main.py 传来的客户端连接
        self.client = client

    def generate_code(self, task):
        # 构造 prompt，要求 AI 生成纯 Python 代码
        prompt = f"请根据以下步骤编写纯 Python 代码。不要包含 Markdown 标记，不要解释：\n{task}"
        try:
            response = self.client.chat.completions.create(
                model="deepseek-coder", 
                messages=[{"role": "user", "content": prompt}]
            )
            code = response.choices[0].message.content
            # 这里的 replace 逻辑已经帮你修正，不会再报 SyntaxError
            return code.replace("```python", "").replace("```", "").strip()
        except Exception as e:
            return f"# 报错：{str(e)}"

    def fix_code(self, code, feedback):
        # 修复代码的逻辑
        prompt = f"修复以下代码的错误 ({feedback})，仅返回代码：\n{code}"
        response = self.client.chat.completions.create(
            model="deepseek-coder",
            messages=[{"role": "user", "content": prompt}]
        )
        new_code = response.choices[0].message.content
        return new_code.replace("```python", "").replace("```", "").strip()