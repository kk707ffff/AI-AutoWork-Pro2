class ResultValidator:
    def __init__(self, client):
        # 接收并存储来自 main.py 的 client 参数
        self.client = client

    def run_test(self, code):
        try:
            compile(code, '<string>', 'exec')
            return True, "Success"
        except Exception as e:
            return False, str(e)
