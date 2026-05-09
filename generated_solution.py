import json
import os
import re

# 步骤1: 定义数据模型和配置
class ProjectConfig:
    def __init__(self, config_data):
        self.name = config_data.get("name", "unnamed")
        self.version = config_data.get("version", "0.1.0")
        self.description = config_data.get("description", "")
        self.dependencies = config_data.get("dependencies", [])

class ProjectModel:
    def __init__(self, config: ProjectConfig):
        self.config = config
        self.files = {}
        self.tasks = []

    def add_file(self, path, content):
        self.files[path] = content

    def add_task(self, task):
        self.tasks.append(task)

# 步骤2: 实现数据序列化与验证
class ProjectSerializer:
    @staticmethod
    def serialize_to_json(model: ProjectModel, output_path):
        data = {
            "name": model.config.name,
            "version": model.config.version,
            "description": model.config.description,
            "dependencies": model.config.dependencies,
            "files": model.files,
            "tasks": model.tasks
        }
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return output_path

    @staticmethod
    def deserialize_from_json(input_path) -> ProjectModel:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        config = ProjectConfig(data)
        model = ProjectModel(config)
        model.files = data.get("files", {})
        model.tasks = data.get("tasks", [])
        return model

    @staticmethod
    def validate_model(model: ProjectModel) -> bool:
        if not model.config.name or not re.match(r'^[\w\-]+$', model.config.name):
            raise ValueError("Invalid project name")
        if not isinstance(model.config.version, str) or not re.match(r'^\d+\.\d+\.\d+$', model.config.version):
            raise ValueError("Invalid version format (expected x.y.z)")
        return True

# 步骤3: 实现业务逻辑 - 项目管理任务执行器
class ProjectTaskExecutor:
    def __init__(self, model: ProjectModel):
        self.model = model

    def run_task(self, task_name, context=None):
        context = context or {}
        task_found = False
        for task in self.model.tasks:
            if task.get("name") == task_name:
                task_found = True
                action = task.get("action", "")
                params = task.get("params", {})
                self._execute_action(action, params, context)
                break
        if not task_found:
            raise KeyError(f"Task '{task_name}' not found in project")

    def _execute_action(self, action, params, context):
        if action == "create_file":
            path = params.get("path")
            content = params.get("content", "")
            if path:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.model.add_file(path, content)
                print(f"[Task] Created file: {path}")
            else:
                raise ValueError("Missing 'path' parameter for create_file action")
        elif action == "print_message":
            message = params.get("message", "Hello from task!")
            print(f"[Task] Message: {message}")
        elif action == "update_config":
            key = params.get("key")
            value = params.get("value")
            if hasattr(self.model.config, key):
                setattr(self.model.config, key, value)
                print(f"[Task] Updated config: {key} = {value}")
            else:
                raise AttributeError(f"Config has no attribute '{key}'")
        else:
            raise NotImplementedError(f"Unknown action: {action}")

# 使用示例（可执行）
if __name__ == "__main__":
    # 创建配置和模型
    config_data = {
        "name": "my-package",
        "version": "1.0.0",
        "description": "A sample project",
        "dependencies": ["requests", "numpy"]
    }
    config = ProjectConfig(config_data)
    model = ProjectModel(config)

    # 添加文件和任务
    model.add_file("src/main.py", "print('Hello World')")
    model.add_task({"name": "init", "action": "print_message", "params": {"message": "Project initialized"}})

    # 序列化验证并保存
    serializer = ProjectSerializer()
    serializer.validate_model(model)
    output_file = "project_export.json"
    serializer.serialize_to_json(model, output_file)
    print(f"Project exported to {output_file}")

    # 反序列化并执行任务
    loaded_model = serializer.deserialize_from_json(output_file)
    executor = ProjectTaskExecutor(loaded_model)
    executor.run_task("init")

import math
import random
from typing import List, Tuple

def step1_get_user_input() -> Tuple[float, float, int]:
    """
    步骤1: 获取用户输入的三个参数：起始值、结束值、步数
    """
    start = float(input("请输入起始值: "))
    end = float(input("请输入结束值: "))
    steps = int(input("请输入步数(正整数): "))
    return start, end, steps

def step2_generate_range(start: float, end: float, steps: int) -> List[float]:
    """
    步骤2: 根据起始值、结束值、步数生成等差数列
    """
    if steps <= 0:
        raise ValueError("步数必须为正整数")
    if steps == 1:
        return [start]
    step_size = (end - start) / (steps - 1)
    return [start + i * step_size for i in range(steps)]

def step3_compute_sine(values: List[float]) -> List[float]:
    """
    步骤3: 对生成的数列每个值计算正弦值
    """
    return [math.sin(v) for v in values]

def step4_random_correction(values: List[float]) -> List[float]:
    """
    步骤4: 对每个正弦值加上一个在[-0.1,0.1]范围内的随机小数
    """
    correction = [random.uniform(-0.1, 0.1) for _ in values]
    return [v + c for v, c in zip(values, correction)]

def step5_compute_product(original: List[float], corrected: List[float]) -> List[float]:
    """
    步骤5: 对原始正弦值和修正后的值按对应位置相乘
    """
    if len(original) != len(corrected):
        raise ValueError("两个列表长度不一致")
    return [o * c for o, c in zip(original, corrected)]

def step6_standardize(data: List[float]) -> List[float]:
    """
    步骤6: 将得到的乘积数组进行标准化(减去均值除以标准差)
    """
    if not data:
        return []
    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    std = math.sqrt(variance)
    if std == 0:
        return [0.0 for _ in data]
    return [(x - mean) / std for x in data]

def main():
    """
    主函数: 串联所有步骤
    """
    # 步骤1: 获取输入
    start, end, steps = step1_get_user_input()
    
    # 步骤2: 生成等差数列
    range_values = step2_generate_range(start, end, steps)
    print(f"步骤2 等差数列: {range_values}")
    
    # 步骤3: 计算正弦
    sine_values = step3_compute_sine(range_values)
    print(f"步骤3 正弦值: {sine_values}")
    
    # 步骤4: 随机修正
    corrected_values = step4_random_correction(sine_values)
    print(f"步骤4 修正后值: {corrected_values}")
    
    # 步骤5: 乘积
    product_values = step5_compute_product(sine_values, corrected_values)
    print(f"步骤5 乘积: {product_values}")
    
    # 步骤6: 标准化
    standardized = step6_standardize(product_values)
    print(f"步骤6 标准化结果: {standardized}")
    
    return standardized

if __name__ == "__main__":
    main()

class WordDictionary:
    def __init__(self):
        self.word_list = []
        self.word_map = {}

dictionary = {
    "beautiful": "美丽的",
    "different": "不同的",
    "important": "重要的",
    "necessary": "必要的",
    "possible": "可能的"
}

import re

# Step 1: Define the base text
base_text = "Hello, World! This is a test. Hello again."

# Step 2: Define the find function
def find_all_occurrences(text, pattern):
    return [(m.start(), m.end()) for m in re.finditer(pattern, text)]

# Step 3: Define the replace function
def replace_substring(text, start, end, replacement):
    return text[:start] + replacement + text[end:]

# Step 4: Define the uppercase function
def to_uppercase(text):
    return text.upper()

# Step 5: Define the lowercase function
def to_lowercase(text):
    return text.lower()

# Step 6: Define the palindrome checker
def is_palindrome(s):
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
    return cleaned == cleaned[::-1]

# Step 7: Define the character count function
def count_characters(text, char):
    return text.count(char)

# Step 8: Define the word_count function
def word_count(text):
    words = re.findall(r'\b\w+\b', text)
    return len(words)

# Step 9: Execute and print results
print("Base text:", base_text)
print("Occurrences of 'Hello':", find_all_occurrences(base_text, "Hello"))
print("Replace 'World' with 'Python':", replace_substring(base_text, 7, 12, "Python"))
print("Uppercase:", to_uppercase(base_text))
print("Lowercase:", to_lowercase(base_text))
print("Is 'racecar' a palindrome?", is_palindrome("racecar"))
print("Count of 'l' in base_text:", count_characters(base_text, 'l'))
print("Word count:", word_count(base_text))

def generate_primes(n):
    primes = []
    for num in range(2, n + 1):
        is_prime = True
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes

def fibonacci(n):
    a, b = 0, 1
    result = []
    for _ in range(n):
        result.append(a)
        a, b = b, a + b
    return result

def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

def is_palindrome(s):
    s = str(s).lower().replace(' ', '')
    return s == s[::-1]

def sort_dict_by_value(d, reverse=False):
    return dict(sorted(d.items(), key=lambda x: x[1], reverse=reverse))

# 创建单词词典
word_dictionary = {}

# 添加单词及其定义
word_dictionary["python"] = "一种高级编程语言"
word_dictionary["dictionary"] = "字典，一种存储键值对的数据结构"
word_dictionary["algorithm"] = "算法，解决问题的步骤和方法"
word_dictionary["variable"] = "变量，用于存储数据的命名空间"

# 打印整个词典
print("单词词典内容:")
for word, definition in word_dictionary.items():
    print(f"{word}: {definition}")

# 查找特定单词
search_word = "python"
if search_word in word_dictionary:
    print(f"\n'{search_word}' 的定义是: {word_dictionary[search_word]}")
else:
    print(f"\n'{search_word}' 不在词典中")

# 更新单词定义
word_dictionary["python"] = "一种广泛使用的解释型高级通用编程语言"
print(f"\n更新后的 'python' 定义: {word_dictionary['python']}")

# 删除单词
del word_dictionary["variable"]
print(f"\n删除 'variable' 后的词典:")
print(word_dictionary)

# 获取词典长度
print(f"\n词典中的单词数量: {len(word_dictionary)}")

word_dict = {}

import json

def load_dictionary(filepath="dictionary.json"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_dictionary(dictionary, filepath="dictionary.json"):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=2)

def add_word(dictionary, english, chinese):
    dictionary[english] = chinese
    save_dictionary(dictionary)

def remove_word(dictionary, english):
    if english in dictionary:
        del dictionary[english]
        save_dictionary(dictionary)
        return True
    return False

def query_word(dictionary, english):
    return dictionary.get(english, None)

def list_words(dictionary):
    for eng, chn in dictionary.items():
        print(f"{eng}: {chn}")

def main():
    dictionary = load_dictionary()
    print("单词翻译字典")
    while True:
        print("\n1. 添加单词")
        print("2. 删除单词")
        print("3. 查询单词")
        print("4. 列出所有单词")
        print("5. 退出")
        choice = input("请选择操作: ")
        if choice == "1":
            eng = input("英文: ")
            chn = input("中文: ")
            add_word(dictionary, eng, chn)
            print("已添加")
        elif choice == "2":
            eng = input("英文: ")
            if remove_word(dictionary, eng):
                print("已删除")
            else:
                print("未找到")
        elif choice == "3":
            eng = input("英文: ")
            result = query_word(dictionary, eng)
            if result:
                print(f"{eng}: {result}")
            else:
                print("未找到")
        elif choice == "4":
            list_words(dictionary)
        elif choice == "5":
            break
        else:
            print("无效选择")

if __name__ == "__main__":
    main()

academic = "学术的"

access_code = "通道；接近"

# 步骤1：定义包含单词与中文翻译的字典
word_dict = {
    "accompany": "陪伴",
    "cherish": "珍惜",
    "adventure": "冒险",
    "journey": "旅程"
}

# 步骤2：打印字典内容
print("单词字典：")
for word, meaning in word_dict.items():
    print(f"{word}: {meaning}")

def accomplish():
    return "完成"

# Step 1: Define a function to get user name
def get_user_name():
    return input("Enter your name: ")

# Step 2: Define a function to get user age
def get_user_age():
    return int(input("Enter your age: "))

# Step 3: Define a function to check if user is adult
def is_adult(age):
    return age >= 18

# Step 4: Define main function
def main():
    name = get_user_name()
    age = get_user_age()
    if is_adult(age):
        print(f"{name} is an adult.")
    else:
        print(f"{name} is not an adult.")

# Step 5: Run the main function
if __name__ == "__main__":
    main()

import numpy as np

# Step 1: 创建一个包含10个随机整数的NumPy数组，取值范围0到100
np.random.seed(42)
arr = np.random.randint(0, 101, size=10)
print("原始数组:", arr)

# Step 2: 计算并打印数组的平均值、中位数和标准差
mean_val = np.mean(arr)
median_val = np.median(arr)
std_val = np.std(arr)
print(f"平均值: {mean_val}, 中位数: {median_val}, 标准差: {std_val}")

# Step 3: 找出数组中大于50的元素，并打印这些元素及其索引
indices = np.where(arr > 50)
values = arr[indices]
print("大于50的元素的索引:", indices[0])
print("大于50的元素:", values)

# Step 4: 将数组重塑为2行5列的矩阵，并打印结果
reshaped = arr.reshape(2, 5)
print("重塑后的矩阵:\n", reshaped)

# Step 5: 计算重塑后矩阵每一行的和，并打印
row_sums = np.sum(reshaped, axis=1)
print("每行的和:", row_sums)

# Step 6: 生成一个3x3的单位矩阵，并打印
identity = np.eye(3)
print("单位矩阵:\n", identity)

# Step 7: 生成一个5x5的随机矩阵（元素在0到1之间），并找出其最大值和最小值的位置
random_matrix = np.random.rand(5, 5)
print("5x5随机矩阵:\n", random_matrix)
max_pos = np.unravel_index(np.argmax(random_matrix), random_matrix.shape)
min_pos = np.unravel_index(np.argmin(random_matrix), random_matrix.shape)
print(f"最大值位置: {max_pos}, 最小值位置: {min_pos}")

# Step 8: 对原始数组进行降序排序，并打印排序后的结果
sorted_desc = np.sort(arr)[::-1]
print("降序排序后的数组:", sorted_desc)

# Step 9: 计算数组元素的正弦值，并打印结果（保留两位小数）
sin_values = np.round(np.sin(arr), 2)
print("正弦值:", sin_values)

# Step 10: 使用向量化操作计算数组元素的平方和平方根，并打印结果
squared = arr ** 2
sqrt_val = np.sqrt(arr)
print("平方:", squared)
print("平方根:", sqrt_val)

import re
import json
import math
import random
import collections
import itertools
import functools
import hashlib
import base64
import datetime
import time
import os
import sys
import csv
import io
import typing
from typing import List, Dict, Tuple, Optional, Any, Union, Callable, Iterable, Set, FrozenSet, Sequence, Mapping, Iterator, Generator, TypeVar, Generic, overload, no_type_check, Final, Literal, NewType, Protocol, runtime_checkable

# 步骤1: 定义基础数据结构和常量
T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class GraphNode:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors else []

# 步骤2: 常用工具函数
def list_to_linkedlist(arr: List[int]) -> Optional[ListNode]:
    dummy = ListNode()
    curr = dummy
    for val in arr:
        curr.next = ListNode(val)
        curr = curr.next
    return dummy.next

def linkedlist_to_list(head: Optional[ListNode]) -> List[int]:
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result

def list_to_tree(arr: List[Optional[int]]) -> Optional[TreeNode]:
    if not arr:
        return None
    nodes = [TreeNode(val) if val is not None else None for val in arr]
    for i in range(len(nodes)):
        if nodes[i] is not None:
            left_idx = 2 * i + 1
            right_idx = 2 * i + 2
            if left_idx < len(nodes):
                nodes[i].left = nodes[left_idx]
            if right_idx < len(nodes):
                nodes[i].right = nodes[right_idx]
    return nodes[0]

def tree_to_list(root: Optional[TreeNode]) -> List[Optional[int]]:
    if not root:
        return []
    result = []
    queue = [root]
    while queue:
        node = queue.pop(0)
        if node:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)
    while result and result[-1] is None:
        result.pop()
    return result

def print_matrix(matrix: List[List[Any]]) -> None:
    for row in matrix:
        print(row)

# 步骤3: 排序算法集合
def bubble_sort(arr: List[T]) -> List[T]:
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def selection_sort(arr: List[T]) -> List[T]:
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def insertion_sort(arr: List[T]) -> List[T]:
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def merge_sort(arr: List[T]) -> List[T]:
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    i = j = 0
    merged = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

def quick_sort(arr: List[T]) -> List[T]:
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def heap_sort(arr: List[T]) -> List[T]:
    def heapify(arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    return arr

# 步骤4: 搜索算法
def binary_search(arr: List[T], target: T) -> int:
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def dfs_graph(node: GraphNode, visited: Set[GraphNode] = None) -> None:
    if visited is None:
        visited = set()
    if node in visited:
        return
    visited.add(node)
    print(node.val)
    for neighbor in node.neighbors:
        dfs_graph(neighbor, visited)

def bfs_graph(start: GraphNode) -> None:
    visited = {start}
    queue = [start]
    while queue:
        node = queue.pop(0)
        print(node.val)
        for neighbor in node.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

def dfs_tree(root: Optional[TreeNode]) -> List[int]:
    result = []
    def helper(node):
        if not node:
            return
        result.append(node.val)
        helper(node.left)
        helper(node.right)
    helper(root)
    return result

def bfs_tree(root: Optional[TreeNode]) -> List[int]:
    if not root:
        return []
    result = []
    queue = [root]
    while queue:
        node = queue.pop(0)
        result.append(node.val)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return result

# 步骤5: 图算法
def dijkstra(graph: Dict[int, List[Tuple[int, int]]], start: int) -> Dict[int, int]:
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    visited = set()
    pq = [(0, start)]
    while pq:
        current_dist, current = heapq.heappop(pq)
        if current in visited:
            continue
        visited.add(current)
        for neighbor, weight in graph[current]:
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    return distances

import heapq
def kruskal_mst(edges: List[Tuple[int, int, int]], n: int) -> List[Tuple[int, int, int]]:
    parent = list(range(n))
    rank = [0] * n
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    def union(x, y):
        x_root, y_root = find(x), find(y)
        if x_root == y_root:
            return False
        if rank[x_root] < rank[y_root]:
            parent[x_root] = y_root
        elif rank[x_root] > rank[y_root]:
            parent[y_root] = x_root
        else:
            parent[y_root] = x_root
            rank[x_root] += 1
        return True
    edges.sort(key=lambda e: e[2])
    mst = []
    for u, v, w in edges:
        if union(u, v):
            mst.append((u, v, w))
    return mst

def topological_sort(graph: Dict[int, List[int]]) -> List[int]:
    in_degree = {u: 0 for u in graph}
    for u in graph:
        for v in graph[u]:
            in_degree[v] = in_degree.get(v, 0) + 1
    queue = [u for u in graph if in_degree[u] == 0]
    result = []
    while queue:
        u = queue.pop(0)
        result.append(u)
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    if len(result) != len(graph):
        return []
    return result

# 步骤6: 动态规划经典问题
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]

def knap_sack(weights: List[int], values: List[int], capacity: int) -> int:
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]
    return dp[n][capacity]

def longest_common_subsequence(text1: str, text2: str) -> int:
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]

def longest_increasing_subsequence(nums: List[int]) -> int:
    dp = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp) if dp else 0

def edit_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
    return dp[m][n]

# 步骤7: 字符串处理
def is_palindrome(s: str) -> bool:
    s = ''.join(c.lower() for c in s if c.isalnum())
    return s == s[::-1]

def longest_palindrome(s: str) -> str:
    if not s:
        return ''
    start, max_len = 0, 1
    def expand_around_center(left, right):
        nonlocal start, max_len
        while left >= 0 and right < len(s) and s[left] == s[right]:
            if right - left + 1 > max_len:
                start = left
                max_len = right - left + 1
            left -= 1
            right += 1
    for i in range(len(s)):
        expand_around_center(i, i)
        expand_around_center(i, i + 1)
    return s[start:start + max_len]

def kmp_search(text: str, pattern: str) -> int:
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    lps = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = lps[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
            lps[i] = j
    j = 0
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = lps[j - 1]
        if text[i] == pattern[j]:
            j += 1
        if j == m:
            return i - m + 1
    return -1

# 步骤8: 数学工具
def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a

def lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)

def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def sieve_of_eratosthenes(n: int) -> List[bool]:
    is_prime_list = [True] * (n + 1)
    is_prime_list[0:2] = [False, False]
    for i in range(2, int(n ** 0.5) + 1):
        if is_prime_list[i]:
            for j in range(i * i, n + 1, i):
                is_prime_list[j] = False
    return is_prime_list

def power_mod(base: int, exp: int, mod: int) -> int:
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp // 2
        base = (base * base) % mod
    return result

# 步骤9: 数据结构实现
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []
    def push(self, val: int) -> None:
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)
    def pop(self) -> None:
        if self.stack:
            val = self.stack.pop()
            if val == self.min_stack[-1]:
                self.min_stack.pop()
    def top(self) -> int:
        return self.stack[-1] if self.stack else None
    def get_min(self) -> int:
        return self.min_stack[-1] if self.min_stack else None

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True
    def search(self, word: str) -> bool:
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end
    def starts_with(self, prefix: str) -> bool:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True

class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    def union(self, x: int, y: int) -> bool:
        x_root, y_root = self.find(x), self.find(y)
        if x_root == y_root:
            return False
        if self.rank[x_root] < self.rank[y_root]:
            self.parent[x_root] = y_root
        elif self.rank[x_root] > self.rank[y_root]:
            self.parent[y_root] = x_root
        else:
            self.parent[y_root] = x_root
            self.rank[x_root] += 1
        return True
    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)

# 步骤10: 算法实现最终步骤 - 提供示例测试函数
def example_usage():
    # 排序测试
    arr = [64, 34, 25, 12, 22, 11, 90]
    print("Original:", arr)
    print("Bubble sort:", bubble_sort(arr.copy()))
    print("Merge sort:", merge_sort(arr.copy()))
    
    # 链表测试
    linked_list = list_to_linkedlist([1, 2, 3, 4, 5])
    print("Linked list to list:", linkedlist_to_list(linked_list))
    
    # 树测试
    tree = list_to_tree([1, 2, 3, None, 5, 6])
    print("Tree DFS:", dfs_tree(tree))
    print("Tree BFS:", bfs_tree(tree))
    
    # 图测试
    graph = {
        0: [(1, 4), (2, 1)],
        1: [(3, 1)],
        2: [(1, 2), (3, 5)],
        3: []
    }
    print("Dijkstra from 0:", dijkstra(graph, 0))
    
    # DP测试
    print("Fibonacci(10):", fibonacci(10))
    print("LCS of 'abcde' and 'ace':", longest_common_subsequence("abcde", "ace"))
    
    # 字符串测试
    print("KMP pattern 'abc' in 'abcabc':", kmp_search("abcabc", "abc"))
    
    # 数学测试
    print("GCD(24, 18):", gcd(24, 18))
    print("Is 17 prime:", is_prime(17))
    
    # 数据结构测试
    trie = Trie()
    trie.insert("hello")
    print("Trie search 'hello':", trie.search("hello"))
    print("Trie starts with 'hel':", trie.starts_with("hel"))
    
    uf = UnionFind(5)
    uf.union(0, 2)
    uf.union(1, 3)
    print("UnionFind connected(0,2):", uf.connected(0, 2))
    print("UnionFind connected(1,2):", uf.connected(1, 2))

if __name__ == "__main__":
    example_usage()

def process_data(input_data):
    # 步骤1：验证输入类型
    if not isinstance(input_data, (list, tuple)):
        raise TypeError("输入必须是列表或元组")
    
    # 步骤2：过滤非数字元素
    numeric_data = [x for x in input_data if isinstance(x, (int, float))]
    
    # 步骤3：计算平均值
    if len(numeric_data) == 0:
        avg = 0.0
    else:
        avg = sum(numeric_data) / len(numeric_data)
    
    # 步骤4：计算标准差
    if len(numeric_data) <= 1:
        std_dev = 0.0
    else:
        variance = sum((x - avg) ** 2 for x in numeric_data) / (len(numeric_data) - 1)
        std_dev = variance ** 0.5
    
    # 步骤5：找出异常值（超过2倍标准差的元素）
    if std_dev == 0:
        outliers = []
    else:
        lower_bound = avg - 2 * std_dev
        upper_bound = avg + 2 * std_dev
        outliers = [x for x in numeric_data if x < lower_bound or x > upper_bound]
    
    # 步骤6：移除异常值
    clean_data = [x for x in numeric_data if x not in outliers]
    
    # 步骤7：返回结果
    return {
        "original_count": len(input_data),
        "numeric_count": len(numeric_data),
        "average": round(avg, 4),
        "std_dev": round(std_dev, 4),
        "outliers": outliers,
        "cleaned_data": clean_data
    }


def main():
    test_samples = [
        [10, 20, 30, 40, 50],
        [1, 2, 3, 100, 5, 6],
        [0.5, 1.0, 1.5, 2.0],
        [],
        (5, 15, 25, 35, 200),
        ["a", 10, "b", 20, None, 30]
    ]
    
    for idx, sample in enumerate(test_samples):
        print(f"样本 {idx+1}: {sample}")
        try:
            result = process_data(sample)
            for key, value in result.items():
                print(f"  {key}: {value}")
        except Exception as e:
            print(f"  错误: {e}")
        print()


if __name__ == "__main__":
    main()

import requests
import random

def fetch_cet4_words():
    # 从开源词库获取常用四级词汇（此URL为示例，需替换为真实可用地址）
    url = "https://raw.githubusercontent.com/jiangyifan/cet4/master/cet4.txt"
    try:
        response = requests.get(url, timeout=10)
        response.encoding = 'utf-8'
        words = response.text.splitlines()
        # 过滤空行和注释
        words = [w.strip() for w in words if w.strip() and not w.startswith('#')]
        return words[:100]  # 返回前100个单词作为常用集合
    except:
        # 若网络请求失败，使用内置高频单词列表
        return default_cet4_words()

def default_cet4_words():
    # 内置50个真正常用的四级词汇
    return [
        "ability", "abroad", "accept", "achieve", "across",
        "action", "active", "actual", "address", "admit",
        "advance", "advantage", "advice", "affair", "affect",
        "afford", "agree", "ahead", "allow", "almost",
        "alone", "already", "also", "although", "amount",
        "ancient", "angle", "announce", "annual", "anxious",
        "apart", "apparent", "appeal", "appear", "apply",
        "approach", "approve", "area", "argue", "arise",
        "arrange", "arrest", "arrive", "article", "aspect",
        "assess", "assign", "assist", "assume", "atmosphere"
    ]

def main():
    words = fetch_cet4_words()
    print("=== 真正常用的四级英语单词 ===")
    for i, word in enumerate(words, 1):
        print(f"{i:4}. {word}")

if __name__ == "__main__":
    main()

# 保持字典键值对结构清晰的示例

my_dict = {
    "name": "张三",
    "age": 25,
    "city": "北京",
    "is_student": False,
    "hobbies": ["阅读", "游泳", "编程"],
    "contact": {
        "email": "zhangsan@example.com",
        "phone": "13800138000"
    }
}

# 访问字典
print(my_dict["name"])
print(my_dict["contact"]["email"])

# 添加新键值对
my_dict["gender"] = "男"

# 修改值
my_dict["age"] = 26

# 删除键值对
del my_dict["is_student"]

# 遍历字典
for key, value in my_dict.items():
    print(f"{key}: {value}")

# 检查键是否存在
if "city" in my_dict:
    print(f"城市: {my_dict['city']}")

# 使用 get 方法安全访问
email = my_dict.get("contact", {}).get("email", "未知")
print(f"邮箱: {email}")

def step1():
    print("确保中文翻译准确")

def step2():
    import re
    text = "请确保中文翻译准确"
    translated = "Please ensure Chinese translation is accurate"
    return text, translated

def step3():
    text = "这是一个测试字符串"
    translated = "This is a test string"
    return {"original": text, "translation": translated}

def step4():
    from googletrans import Translator
    translator = Translator()
    result = translator.translate("你好世界", dest='en')
    return result.text

def main():
    step1()
    step2()
    step3()
    print(step4())

if __name__ == "__main__":
    main()

# Step 1: 读取输入
n = int(input().strip())
arr = list(map(int, input().strip().split()))

# Step 2: 计算差值数组
diff = []
for i in range(1, n):
    diff.append(arr[i] - arr[i-1])

# Step 3: 贪心统计上升段（diff > 0）
total = 0
for d in diff:
    if d > 0:
        total += d

# Step 4: 输出结果
print(total)

import random

def select_random_word(words):
    if not words:
        return None
    return random.choice(words)

import random
import json

WORD_DICT = {
    "apple": "苹果",
    "banana": "香蕉",
    "cat": "猫",
    "dog": "狗",
    "elephant": "大象",
    "fish": "鱼",
    "grape": "葡萄",
    "house": "房子",
    "ice": "冰",
    "jungle": "丛林"
}

def get_random_word(word_dict):
    return random.choice(list(word_dict.keys()))

if __name__ == "__main__":
    word = get_random_word(WORD_DICT)
    print(f"请翻译这个单词: {word}")

import requests
from bs4 import BeautifulSoup

def get_webpage_title(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.title.string if soup.title else None
    return title

def get_all_links(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [a.get('href') for a in soup.find_all('a', href=True)]
    return links

def get_element_text_by_id(url, element_id):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    element = soup.find(id=element_id)
    return element.get_text(strip=True) if element else None

def get_element_text_by_class(url, class_name):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    elements = soup.find_all(class_=class_name)
    return [el.get_text(strip=True) for el in elements]

def get_page_text(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text(separator='\n', strip=True)

def solution(s: str) -> str:
    # Step 1: Determine if the length of s is even
    if len(s) % 2 == 1:
        return "no"

    # Step 2: Create a stack
    stack = []

    # Step 3: Define mapping of closing to opening brackets
    mapping = {')': '(', ']': '[', '}': '{'}

    # Step 4: Iterate through each character in s
    for char in s:
        # Step 5: If char is a closing bracket
        if char in mapping:
            # Step 6: Pop top element, if stack empty use placeholder
            top_element = stack.pop() if stack else '#'
            # Step 7: Check if mapping matches
            if mapping[char] != top_element:
                return "no"
        else:
            # Step 8: It's an opening bracket, push onto stack
            stack.append(char)

    # Step 9: After loop, check if stack is empty
    if not stack:
        return "yes"
    else:
        return "no"

import random

def main():
    pass

if __name__ == "__main__":
    main()

import heapq
from collections import deque, Counter
import random
import math

# 1. 实现一个函数，使用深度优先搜索遍历一个图（邻接表表示），返回所有节点访问顺序
def dfs(graph, start):
    visited = set()
    order = []
    def _dfs(node):
        if node in visited:
            return
        visited.add(node)
        order.append(node)
        for neighbor in graph.get(node, []):
            _dfs(neighbor)
    _dfs(start)
    return order

# 2. 实现一个函数，使用广度优先搜索遍历一个图，返回所有节点访问顺序
def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order

# 3. 实现一个函数，使用 dijkstra 算法找出图中从起点到所有节点的最短路径（非负权重）
def dijkstra(graph, start):
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, node = heapq.heappop(pq)
        if d > dist[node]:
            continue
        for neighbor, weight in graph.get(node, []):
            nd = d + weight
            if nd < dist[neighbor]:
                dist[neighbor] = nd
                heapq.heappush(pq, (nd, neighbor))
    return dist

# 4. 实现一个函数，使用 A* 算法寻找从起点到终点的最短路径，启发式函数使用曼哈顿距离
def a_star(grid, start, goal):
    # grid: 二维列表, 0 表示可通行, 1 表示障碍物
    rows, cols = len(grid), len(grid[0])
    def heuristic(a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])
    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    while open_set:
        current = heapq.heappop(open_set)[1]
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]
        x, y = current
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x+dx, y+dy
            neighbor = (nx, ny)
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0:
                temp_g = g_score[current] + 1
                if neighbor not in g_score or temp_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g
                    f_score[neighbor] = temp_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return None

# 5. 实现一个函数，使用快速排序算法对列表进行排序（原地排序）
def quicksort(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low < high:
        pivot_index = partition(arr, low, high)
        quicksort(arr, low, pivot_index-1)
        quicksort(arr, pivot_index+1, high)
    return arr

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i+1

# 6. 实现一个函数，使用归并排序算法对列表进行排序（返回新列表）
def mergesort(arr):
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = mergesort(arr[:mid])
    right = mergesort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# 7. 实现一个函数，使用二分查找在一个已排序列表中查找目标值，返回索引或-1
def binary_search(arr, target):
    left, right = 0, len(arr)-1
    while left <= right:
        mid = (left+right)//2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid+1
        else:
            right = mid-1
    return -1

# 8. 实现一个函数，使用动态规划解决斐波那契数列，返回第n个数（n>=0）
def fibonacci(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n+1):
        a, b = b, a+b
    return b

# 9. 实现一个函数，使用正则表达式验证邮箱格式（简单规则: 包含@和.且@在.之前）
def validate_email(email):
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

# 10. 实现一个函数，使用递归计算列表元素的所有排列
def permutations(elements):
    if len(elements) == 0:
        return [[]]
    result = []
    for i, elem in enumerate(elements):
        rest = elements[:i] + elements[i+1:]
        for p in permutations(rest):
            result.append([elem] + p)
    return result

import random

def get_random_word(word_dict):
    if not word_dict:
        return None
    word_list = list(word_dict.keys())
    return random.choice(word_list)

import random

def get_random_word(word_dict):
    """从字典中随机获取一个单词"""
    if not word_dict:
        return None
    return random.choice(list(word_dict.keys()))

import random

word = random.choice(list(word_dict.keys()))

import re
from collections import Counter

def analyze_text(text):
    """
    Analyzes a given text and returns a dictionary with word counts.
    
    Parameters:
    text (str): The input text to analyze.
    
    Returns:
    dict: A dictionary where keys are words (lowercase) and values are their counts.
    """
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    word_counts = Counter(words)
    return dict(word_counts)

def get_most_common_words(text, n=5):
    """
    Returns the n most common words from the text.
    
    Parameters:
    text (str): The input text.
    n (int): Number of top words to return.
    
    Returns:
    list: A list of tuples (word, count) sorted by count descending.
    """
    word_counts = analyze_text(text)
    most_common = Counter(word_counts).most_common(n)
    return most_common

def filter_words_by_length(text, min_len=3, max_len=10):
    """
    Returns a word count dictionary filtered by word length.
    
    Parameters:
    text (str): The input text.
    min_len (int): Minimum word length.
    max_len (int): Maximum word length.
    
    Returns:
    dict: Filtered word count dictionary.
    """
    full_counts = analyze_text(text)
    filtered = {word: count for word, count in full_counts.items() if min_len <= len(word) <= max_len}
    return filtered

def word_frequency_percentage(text):
    """
    Returns the percentage frequency of each word in the text.
    
    Parameters:
    text (str): The input text.
    
    Returns:
    dict: Dictionary with word as key and frequency percentage as value.
    """
    word_counts = analyze_text(text)
    total_words = sum(word_counts.values())
    if total_words == 0:
        return {}
    percentages = {word: (count / total_words) * 100 for word, count in word_counts.items()}
    return percentages

def remove_stopwords(text, stopwords=None):
    """
    Removes common stopwords from the word count dictionary.
    
    Parameters:
    text (str): The input text.
    stopwords (set): Set of stopwords to remove. If None, uses a default list.
    
    Returns:
    dict: Word counts without stopwords.
    """
    if stopwords is None:
        stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                     'have', 'has', 'had', 'do', 'does', 'did', 'shall', 'will', 'would',
                     'should', 'may', 'might', 'must', 'can', 'could', 'to', 'of', 'in',
                     'for', 'on', 'with', 'at', 'by', 'from', 'as', 'and', 'or', 'not',
                     'no', 'but', 'so', 'if', 'than', 'that', 'this', 'these', 'those',
                     'it', 'its', 'he', 'she', 'they', 'them', 'we', 'you', 'i', 'my',
                     'your', 'his', 'her', 'their', 'our', 'its', 'me', 'him', 'us'}
    full_counts = analyze_text(text)
    cleaned = {word: count for word, count in full_counts.items() if word not in stopwords}
    return cleaned

def export_word_counts_to_file(data, filename="word_counts.txt"):
    """
    Exports a word count dictionary to a text file.
    
    Parameters:
    data (dict): Word count dictionary.
    filename (str): Output filename.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for word, count in sorted(data.items(), key=lambda x: -x[1]):
            f.write(f"{word}: {count}\n")

from typing import Any, Dict, List, Optional

# Step 1: Define a function that returns a greeting
def get_greeting(name: str) -> str:
    return f"Hello, {name}!"

# Step 2: Define a function that adds two numbers
def add_numbers(a: float, b: float) -> float:
    return a + b

# Step 3: Define a function that processes a list of integers
def process_integers(numbers: List[int]) -> Dict[str, Any]:
    if not numbers:
        return {"sum": 0, "count": 0, "mean": None}
    total = sum(numbers)
    count = len(numbers)
    mean = total / count
    return {"sum": total, "count": count, "mean": mean}

# Step 4: Define a function that filters even numbers
def filter_even(numbers: List[int]) -> List[int]:
    return [n for n in numbers if n % 2 == 0]

# Step 5: Define a class for a simple counter
class Counter:
    def __init__(self, start: int = 0):
        self._value = start

    def increment(self, step: int = 1) -> None:
        self._value += step

    def decrement(self, step: int = 1) -> None:
        self._value -= step

    def current_value(self) -> int:
        return self._value

    def reset(self, new_start: int = 0) -> None:
        self._value = new_start

# Step 6: Define a function that uses the Counter class
def use_counter(initial: int = 0, operations: Optional[List[tuple]] = None) -> Counter:
    counter = Counter(initial)
    if operations:
        for operation, step in operations:
            if operation == "increment":
                counter.increment(step)
            elif operation == "decrement":
                counter.decrement(step)
            # ignore unknown operations
    return counter

# Step 7: Define a main function that demonstrates usage
def main() -> None:
    # Demonstration of get_greeting
    print(get_greeting("Alice"))

    # Demonstration of add_numbers
    print(add_numbers(3.14, 2.86))

    # Demonstration of process_integers
    sample_list = [1, 2, 3, 4, 5]
    result = process_integers(sample_list)
    print(result)

    # Demonstration of filter_even
    evens = filter_even([1, 2, 3, 4, 5, 6])
    print(evens)

    # Demonstration of Counter and use_counter
    counter = use_counter(10, [("increment", 5), ("decrement", 2), ("increment", 1)])
    print(f"Final counter value: {counter.current_value()}")

if __name__ == "__main__":
    main()

from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Question:
    question_text: str
    options: Optional[List[str]] = None
    correct_answer: Optional[str] = None

class Quiz:
    def __init__(self, title: str = "My Quiz"):
        self.title = title
        self.questions: List[Question] = []

    def add_question(self, question: Question) -> None:
        self.questions.append(question)

    def remove_question(self, index: int) -> None:
        if 0 <= index < len(self.questions):
            del self.questions[index]

    def get_total_questions(self) -> int:
        return len(self.questions)

    def take_quiz(self) -> float:
        if not self.questions:
            print("No questions in the quiz.")
            return 0.0

        score = 0
        for i, question in enumerate(self.questions, 1):
            print(f"\nQuestion {i}: {question.question_text}")
            if question.options:
                for idx, option in enumerate(question.options, 1):
                    print(f"  {idx}. {option}")
            user_answer = input("Your answer: ").strip()
            if question.correct_answer and user_answer.lower() == question.correct_answer.lower():
                print("Correct!")
                score += 1
            else:
                correct_display = question.correct_answer if question.correct_answer else "N/A"
                print(f"Wrong. Correct answer: {correct_display}")

        final_score = (score / len(self.questions)) * 100
        print(f"\nYour score: {score}/{len(self.questions)} ({final_score:.2f}%)")
        return final_score

# Example usage:
if __name__ == "__main__":
    quiz = Quiz("General Knowledge Quiz")
    q1 = Question("What is the capital of France?", ["Berlin", "Madrid", "Paris", "Rome"], "Paris")
    q2 = Question("What is 2 + 2?", ["3", "4", "5", "6"], "4")
    q3 = Question("What is the color of the sky?", ["Blue", "Green", "Red", "Yellow"], "Blue")

    quiz.add_question(q1)
    quiz.add_question(q2)
    quiz.add_question(q3)

    print(f"Quiz: {quiz.title}")
    print(f"Total questions: {quiz.get_total_questions()}")
    quiz.take_quiz()

import random

def get_random_word(word_dict):
    return random.choice(list(word_dict.keys()))

selected_word = get_random_word(word_dict)

import random

def select_word():
    words = ["apple", "banana", "cherry", "dragon", "eagle"]
    return random.choice(words)

def display_word(word):
    print(f"English word: {word}")

if __name__ == "__main__":
    selected_word = select_word()
    english_word = selected_word  # 要显示的英文
    display_word(english_word)

correct_answer = word_dict[selected_word]

import nltk
from nltk.probability import FreqDist
import random

# 第一步：获取或加载《老人与海》原始文本
def load_text():
    # 尝试从本地文件读取，如果不存在则从nltk语料库获取
    try:
        with open("老人与海.txt", "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        from nltk.corpus import gutenberg
        nltk.download('gutenberg', quiet=True)
        # 《老人与海》在古登堡语料库中ID为 'chesterton-thursday.txt' 仅为示例，实际无直接匹配，这里用其他文本替代演示
        text = gutenberg.raw('chesterton-thursday.txt')[:5000]  # 仅用于演示
    return text

# 第二步：文本预处理，将词汇归一化
def preprocess(text):
    # 转换为小写，按空格分词，去除标点
    tokens = nltk.word_tokenize(text.lower())
    # 过滤非字母单词
    words = [word for word in tokens if word.isalpha()]
    return words

# 第三步：统计词频并生成词云相关数据
def word_frequency(words):
    fdist = FreqDist(words)
    # 按频率排序的词列表
    sorted_words = sorted(fdist.items(), key=lambda x: x[1], reverse=True)
    return sorted_words

# 第四步：生成一个简单的词云效果（文本形式）
def generate_word_cloud_text(sorted_words, top_n=50):
    lines = []
    for word, count in sorted_words[:top_n]:
        # 模拟词云大小：频次越高，输出重复次数越多
        size = max(1, int(count / sorted_words[0][1] * 20))
        line = (word + " ") * size
        lines.append(line)
    return "\n".join(lines)

# 第五步：主程序入口
def main():
    text = load_text()
    words = preprocess(text)
    sorted_words = word_frequency(words)
    word_cloud = generate_word_cloud_text(sorted_words, top_n=30)
    print(word_cloud)

if __name__ == "__main__":
    main()

import random

def step1():
    print("步骤1：生成一个1到100之间的随机整数")
    return random.randint(1, 100)

def step2(target):
    print("步骤2：开始猜数字游戏")
    attempts = 0
    while True:
        try:
            guess = int(input("请输入你猜的数字（1-100）："))
            attempts += 1
            if guess < target:
                print("猜小了，再试试")
            elif guess > target:
                print("猜大了，再试试")
            else:
                print(f"猜对了！你用了{attempts}次尝试。")
                break
        except ValueError:
            print("输入无效，请输入一个整数。")

def main():
    target = step1()
    step2(target)

if __name__ == "__main__":
    main()

def analyze_key_design_points(requirements):
    """
    根据需求分析关键设计点
    
    Args:
        requirements: 需求描述文本或需求列表
    
    Returns:
        关键设计点列表
    """
    if isinstance(requirements, str):
        requirements = requirements.split('\n')
    
    design_points = []
    for req in requirements:
        req = req.strip()
        if not req:
            continue
            
        # 识别关键设计要素
        design_point = {
            'original_requirement': req,
            'design_considerations': [],
            'constraints': [],
            'priorities': []
        }
        
        # 分析性能要求
        if any(keyword in req.lower() for keyword in ['性能', '速度', '响应时间', '吞吐量']):
            design_point['design_considerations'].append('性能优化')
            design_point['constraints'].append('响应时间限制')
            design_point['priorities'].append('高')
        
        # 分析可扩展性
        if any(keyword in req.lower() for keyword in ['扩展', '伸缩', '模块化', '插件']):
            design_point['design_considerations'].append('模块化设计')
            design_point['constraints'].append('接口稳定性')
            design_point['priorities'].append('中')
        
        # 分析安全性
        if any(keyword in req.lower() for keyword in ['安全', '认证', '授权', '加密']):
            design_point['design_considerations'].append('安全防护')
            design_point['constraints'].append('合规要求')
            design_point['priorities'].append('高')
        
        # 分析可用性
        if any(keyword in req.lower() for keyword in ['可用', '可靠性', '容错', '故障转移']):
            design_point['design_considerations'].append('高可用架构')
            design_point['constraints'].append('SLA要求')
            design_point['priorities'].append('高')
        
        # 分析可维护性
        if any(keyword in req.lower() for keyword in ['维护', '调试', '日志', '监控']):
            design_point['design_considerations'].append('可观测性')
            design_point['constraints'].append('运营成本')
            design_point['priorities'].append('中')
        
        # 分析成本约束
        if any(keyword in req.lower() for keyword in ['成本', '预算', '资源', '效率']):
            design_point['design_considerations'].append('成本优化')
            design_point['constraints'].append('资源限制')
            design_point['priorities'].append('高')
        
        # 分析兼容性
        if any(keyword in req.lower() for keyword in ['兼容', '集成', 'API', '版本']):
            design_point['design_considerations'].append('向后兼容')
            design_point['constraints'].append('接口版本管理')
            design_point['priorities'].append('中')
        
        design_points.append(design_point)
    
    return design_points


def prioritize_design_points(design_points):
    """
    对关键设计点进行优先级排序
    
    Args:
        design_points: 设计点列表
    
    Returns:
        按优先级排序后的设计点
    """
    priority_order = {'高': 0, '中': 1, '低': 2}
    
    def sort_key(point):
        priorities = point.get('priorities', ['低'])
        min_priority = min(priority_order.get(p, 2) for p in priorities)
        return min_priority
    
    return sorted(design_points, key=sort_key)


def validate_design_points(design_points):
    """
    验证设计点的完整性和一致性
    
    Args:
        design_points: 设计点列表
    
    Returns:
        验证结果字典
    """
    validation_result = {
        'is_valid': True,
        'issues': [],
        'warnings': []
    }
    
    for i, point in enumerate(design_points):
        if not point.get('original_requirement'):
            validation_result['issues'].append(f"设计点 {i+1} 缺少原始需求描述")
            validation_result['is_valid'] = False
        
        if not point.get('design_considerations') and not point.get('constraints'):
            validation_result['warnings'].append(f"设计点 {i+1} 未识别任何设计考虑或约束")
        
        if not point.get('priorities'):
            validation_result['warnings'].append(f"设计点 {i+1} 未指定优先级")
    
    return validation_result


def generate_design_summary(design_points):
    """
    生成设计点总结报告
    
    Args:
        design_points: 设计点列表
    
    Returns:
        总结文本
    """
    summary_lines = []
    summary_lines.append("=" * 50)
    summary_lines.append("关键设计点分析报告")
    summary_lines.append("=" * 50)
    summary_lines.append("")
    
    sorted_points = prioritize_design_points(design_points)
    
    for i, point in enumerate(sorted_points, 1):
        summary_lines.append(f"{'─' * 40}")
        summary_lines.append(f"设计点 {i}：{point['original_requirement']}")
        summary_lines.append(f"设计考虑：{', '.join(point['design_considerations']) if point['design_considerations'] else '无'}")
        summary_lines.append(f"约束条件：{', '.join(point['constraints']) if point['constraints'] else '无'}")
        summary_lines.append(f"优先级：{', '.join(point['priorities']) if point['priorities'] else '未指定'}")
        summary_lines.append("")
    
    validation = validate_design_points(design_points)
    if not validation['is_valid'] or validation['warnings']:
        summary_lines.append("=" * 50)
        summary_lines.append("验证结果：")
        for issue in validation['issues']:
            summary_lines.append(f"  [错误] {issue}")
        for warning in validation['warnings']:
            summary_lines.append(f"  [警告] {warning}")
    
    return '\n'.join(summary_lines)


if __name__ == "__main__":
    # 示例使用
    sample_requirements = [
        "系统需要支持高并发访问，响应时间小于200ms",
        "支持水平扩展，增加节点可提升性能",
        "用户认证需要支持OAuth2.0",
        "系统可用性要求达到99.99%",
        "需要完整的日志和监控系统",
        "运行成本控制在预算范围内",
        "提供RESTful API供第三方集成"
    ]
    
    design_points = analyze_key_design_points(sample_requirements)
    summary = generate_design_summary(design_points)
    print(summary)

import random

def random_choice(seq):
    return random.choice(seq)

def get_word_and_translation(word, translations):
    if word in translations:
        return word, translations[word]
    return None, None

# 示例用法
translations_dict = {
    "apple": "苹果",
    "book": "书",
    "cat": "猫"
}

word, translation = get_word_and_translation("apple", translations_dict)
if word:
    print(f"单词: {word}, 翻译: {translation}")
else:
    print("未找到")

import random

def shuffle_words(text):
    """
    Shuffles all words in the given text while preserving the original order of spaces and punctuation.
    This function ensures each word is randomly repositioned with equal probability.
    """
    # Split text into tokens: words, spaces, punctuation
    tokens = []
    word_positions = []
    current_word = []
    i = 0
    while i < len(text):
        char = text[i]
        if char.isalnum() or char in ["'", "-"]:  # consider hyphenated and apostrophe words as part of the word
            current_word.append(char)
            i += 1
        else:
            if current_word:
                tokens.append(('word', ''.join(current_word)))
                word_positions.append(len(tokens) - 1)
                current_word = []
            # Capture all consecutive non-word characters as a token
            non_word = []
            while i < len(text) and not (text[i].isalnum() or text[i] in ["'", "-"]):
                non_word.append(text[i])
                i += 1
            if non_word:
                tokens.append(('separator', ''.join(non_word)))
    if current_word:
        tokens.append(('word', ''.join(current_word)))
        word_positions.append(len(tokens) - 1)

    # Extract words and shuffle them with full randomness
    words = [tokens[pos][1] for pos in word_positions]
    random.shuffle(words)

    # Place shuffled words back into their original positions
    for idx, pos in enumerate(word_positions):
        tokens[pos] = ('word', words[idx])

    # Reconstruct the string
    result = ''.join(token[1] for token in tokens)
    return result

def random_word_scramble(text):
    """
    Main function to scramble words randomly with full coverage.
    """
    if not text:
        return text
    return shuffle_words(text)

# Example usage (uncomment to test):
# test_string = "Hello, world! This is a test. Don't be afraid - it's fun."
# print(random_word_scramble(test_string))

import subprocess
import sys

def run_command(cmd, timeout=30):
    """运行 shell 命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)

def check_python_version():
    """检查 Python 版本"""
    return sys.version_info >= (3, 6)

def main():
    print("环境准备中...")
    
    # 1. 检查 Python 版本
    if not check_python_version():
        print("错误: 需要 Python 3.6 或更高版本")
        sys.exit(1)
    
    # 2. 安装/升级 pip
    print("更新 pip...")
    ret, out, err = run_command(f"{sys.executable} -m pip install --upgrade pip --quiet")
    if ret != 0:
        print(f"pip 更新警告: {err}")
    
    # 3. 安装必要的依赖
    print("安装基础依赖...")
    dependencies = [
        "setuptools>=58.0.0",
        "wheel>=0.37.0"
    ]
    
    for dep in dependencies:
        ret, out, err = run_command(
            f"{sys.executable} -m pip install {dep} --quiet"
        )
        if ret != 0:
            print(f"安装 {dep} 失败: {err}")
            sys.exit(1)
    
    # 4. 检查常见包是否正确安装
    print("检查依赖完整性...")
    ret, out, err = run_command(
        f"{sys.executable} -c \"import setuptools; import wheel; print('OK')\""
    )
    if ret != 0:
        print("核心依赖检查失败")
        sys.exit(1)
    
    print("环境准备完成")
    
    # 5. 简单的功能验证
    print("运行功能验证...")
    test_code = '''
# 基础模块测试
import json
import math
import os
import random
import re
import string
import sys
import time
from collections import defaultdict, Counter
from itertools import permutations, combinations

# 测试一些基础功能
print("基础库测试通过")
print(f"Python 版本: {sys.version}")
print(f"平台: {sys.platform}")
'''
    
    ret, out, err = run_command(
        f"{sys.executable} -c \"{test_code}\""
    )
    if ret != 0:
        print(f"功能验证失败: {err}")
        sys.exit(1)
    print(out)
    
    print("所有步骤完成 ✅")

if __name__ == "__main__":
    main()

def get_user_input(prompt):
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        return None

def display_message(message, message_type="info"):
    prefix_map = {
        "info": "[INFO]",
        "success": "[SUCCESS]",
        "warning": "[WARNING]",
        "error": "[ERROR]"
    }
    prefix = prefix_map.get(message_type, "[INFO]")
    print(f"{prefix} {message}")

def confirm_action(prompt="确认执行此操作？(y/n): "):
    while True:
        response = get_user_input(prompt)
        if response is None:
            return False
        response = response.strip().lower()
        if response in ("y", "yes"):
            return True
        elif response in ("n", "no"):
            return False
        else:
            display_message("请输入 y 或 n", "warning")

def select_option(options, prompt="请选择一个选项: "):
    if not options:
        display_message("没有可用的选项", "error")
        return None
    print("可用选项：")
    for idx, option in enumerate(options, 1):
        print(f"{idx}. {option}")
    while True:
        user_input = get_user_input(prompt)
        if user_input is None:
            return None
        try:
            choice = int(user_input.strip())
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                display_message(f"请输入 1 到 {len(options)} 之间的数字", "warning")
        except ValueError:
            display_message("请输入有效数字", "warning")

def interactive_loop():
    display_message("交互系统启动", "success")
    while True:
        print("\n--- 主菜单 ---")
        action = get_user_input("输入 'exit' 退出，'menu' 显示菜单: ")
        if action is None:
            break
        action = action.strip().lower()
        if action == "exit":
            if confirm_action("确定要退出吗？"):
                display_message("退出系统", "info")
                break
        elif action == "menu":
            display_message("当前在菜单中", "info")
            sample_options = ["功能A", "功能B", "功能C"]
            selected = select_option(sample_options, "请选择功能: ")
            if selected:
                display_message(f"您选择了: {selected}", "success")
        else:
            display_message(f"未知指令: {action}", "error")

def main():
    try:
        interactive_loop()
    except Exception as e:
        display_message(f"发生意外错误: {e}", "error")

if __name__ == "__main__":
    main()

def get_valid_input(prompt, validation_func, error_message):
    while True:
        user_input = input(prompt)
        if validation_func(user_input):
            return user_input
        print(error_message)

def is_positive_integer(value):
    try:
        num = int(value)
        return num > 0
    except ValueError:
        return False

def is_non_empty_string(value):
    return len(value.strip()) > 0

def is_yes_no(value):
    return value.lower() in ['y', 'n', 'yes', 'no']

def process_data():
    print("交互循环开始")
    while True:
        name = get_valid_input("请输入您的姓名: ", is_non_empty_string, "姓名不能为空，请重新输入。")
        age = get_valid_input("请输入您的年龄: ", is_positive_integer, "年龄必须是正整数，请重新输入。")
        
        print(f"\n您好，{name}！您今年 {age} 岁。")
        
        continue_input = get_valid_input("\n是否继续？(y/n): ", is_yes_no, "请输入 y 或 n。")
        if continue_input.lower() in ['n', 'no']:
            print("感谢使用，再见！")
            break
        print()

if __name__ == "__main__":
    process_data()

import json

# 示例输入数据
data = {
    "config": {
        "iterations": 100,
        "tolerance": 1e-6,
        "solver": "cg",
        "verbose": True
    },
    "mesh": {
        "type": "triangular",
        "nodes": 125,
        "elements": 200
    },
    "boundary_conditions": {
        "left": "fixed",
        "right": "roller",
        "temperature": 300.0
    }
}

# 步骤1: 读取 JSON 数据（如果从文件读取）
def read_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# 保存 JSON 数据到文件
def write_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

# 步骤2: 提取特定参数
def extract_parameters(data):
    params = {}
    params['iterations'] = data['config'].get('iterations')
    params['tolerance'] = data['config'].get('tolerance')
    params['solver'] = data['config'].get('solver')
    params['nodes'] = data['mesh'].get('nodes')
    params['temperature'] = data['boundary_conditions'].get('temperature')
    return params

# 步骤3: 修改配置参数
def modify_config(data, key, value):
    if 'config' in data:
        data['config'][key] = value
    else:
        raise KeyError("Config section missing")

# 步骤4: 使用修改后的数据重新写入 JSON
def update_json(original_data, modifications):
    import copy
    new_data = copy.deepcopy(original_data)
    for section, changes in modifications.items():
        if section in new_data:
            for key, value in changes.items():
                new_data[section][key] = value
    return new_data

# 测试函数调用
if __name__ == "__main__":
    # 提取参数
    result = extract_parameters(data)
    print("Extracted parameters:", result)
    
    # 修改配置（例如迭代次数）
    modify_config(data, "iterations", 200)
    modify_config(data, "tol", 1e-8)  # 添加新键
    
    write_json(data, "modified_simulation.json")
    
    # 手动创建修改字典
    mods = {"mesh": {"elements": 400}, "boundary_conditions": {"temperature": 350.0}}
    updated = update_json(data, mods)
    write_json(updated, "updated_simulation.json")
    
    print("Files written successfully")

import json
import csv
import os
from collections import defaultdict

def read_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json(data, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def read_csv(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def write_csv(data, filepath, fieldnames=None):
    if not data:
        return
    if fieldnames is None:
        fieldnames = data[0].keys()
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def flatten_dict(d, parent_key='', sep='_'):
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items

def unflatten_dict(d, sep='_'):
    result = {}
    for key, value in d.items():
        parts = key.split(sep)
        current = result
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value
    return result

def merge_dicts(base_dict, override_dict):
    result = base_dict.copy()
    for k, v in override_dict.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = merge_dicts(result[k], v)
        else:
            result[k] = v
    return result

def group_by(data, key_func):
    grouped = defaultdict(list)
    for item in data:
        group_key = key_func(item)
        grouped[group_key].append(item)
    return dict(grouped)

def chunk_list(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

def ensure_directory(path):
    os.makedirs(path, exist_ok=True)

def get_file_extension(filepath):
    _, ext = os.path.splitext(filepath)
    return ext.lower()

def list_files(directory, extension=None):
    files = []
    for f in os.listdir(directory):
        full_path = os.path.join(directory, f)
        if os.path.isfile(full_path):
            if extension is None or f.endswith(extension):
                files.append(full_path)
    return sorted(files)

import random

def run_quiz(word_dict):
    if not word_dict:
        print("No words in the dictionary.")
        return

    items = list(word_dict.items())
    random.shuffle(items)
    correct = 0
    total = len(items)

    print("Quiz started! Press Enter to skip a word.")
    print("Type 'exit' to quit early.\n")

    for i, (word, definition) in enumerate(items, 1):
        print(f"Word {i}/{total}: {word}")
        user_answer = input("Your definition: ").strip()

        if user_answer.lower() == 'exit':
            break

        if not user_answer:
            print(f"Skipped. Correct definition: {definition}\n")
            continue

        if user_answer.lower() == definition.lower():
            print("Correct!\n")
            correct += 1
        else:
            print(f"Incorrect. Correct definition: {definition}\n")

    print(f"Quiz finished. You got {correct}/{min(i, total)} correct.")

def run_word_test():
    import json, sys, random
    
    try:
        with open("words.json", "r", encoding="utf-8") as f:
            words = json.load(f)
    except:
        print("words.json 文件未找到或格式错误。")
        return

    while True:
        correct = 0
        wrong = 0
        length = len(words)
        if length == 0:
            print("单词列表为空。")
            return

        indices = list(range(length))
        random.shuffle(indices)
        for i in indices:
            word = words[i]
            if isinstance(word, dict) and 'english' in word and 'chinese' in word:
                eng = word['english']
                chn = word['chinese']
                ans = input(f"请输入 '{eng}' 的中文意思: ").strip()
                if ans == chn:
                    correct += 1
                else:
                    wrong += 1
                    print(f"正确答案: {chn}")
            else:
                print("单词格式有误，跳过。")
        
        total = correct + wrong
        if total > 0:
            print(f"\n测试完成！正确: {correct}, 错误: {wrong}, 正确率: {correct/total*100:.1f}%")
        else:
            print("\n没有有效的单词进行测试。")

        again = input("继续测试？(y/n): ").strip().lower()
        if again != 'y':
            break

import random

def choose_random_word(word_list):
    if not word_list:
        raise ValueError("单词列表不能为空")
    return random.choice(word_list)

import random

def get_random_word(word_dict):
    return random.choice(word_dict)

def look_up_word(word_dict, word):
    correct_answer = word_dict[word]
    return correct_answer

def traverse_grid(m, n):
    visited = set()
    result = []
    stack = [(0, 0)]

    while stack:
        i, j = stack.pop()
        if (i, j) in visited or i >= m or j >= n:
            continue
        visited.add((i, j))
        result.append((i, j))
        if i + 1 < m:
            stack.append((i + 1, j))
        if j + 1 < n:
            stack.append((i, j + 1))

    return result


def collect_path_sum(matrix, path):
    total = 0
    for i, j in path:
        total += matrix[i][j]
    return total


def min_path_sum(matrix, path):
    min_val = float('inf')
    min_pos = None
    for i, j in path:
        if matrix[i][j] < min_val:
            min_val = matrix[i][j]
            min_pos = (i, j)
    return min_val, min_pos


def max_path_sum(matrix, path):
    max_val = float('-inf')
    max_pos = None
    for i, j in path:
        if matrix[i][j] > max_val:
            max_val = matrix[i][j]
            max_pos = (i, j)
    return max_val, max_pos


if __name__ == "__main__":
    # Example usage
    grid = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    path = traverse_grid(3, 3)
    print("Traversal path:", path)

    total = collect_path_sum(grid, path)
    print("Sum of path:", total)

    min_val, min_pos = min_path_sum(grid, path)
    print("Minimum value:", min_val, "at", min_pos)

    max_val, max_pos = max_path_sum(grid, path)
    print("Maximum value:", max_val, "at", max_pos)

def show_problem_and_get_input():
    problem = input("请输入题目: ")
    user_input = input("请输入您的答案: ")
    return problem, user_input

if __name__ == "__main__":
    show_problem_and_get_input()

print(f"请翻译英文单词: {word}")

user_answer = input("请输入中文意思: ").strip()

import sys
import math
from collections import deque, defaultdict, Counter
from functools import lru_cache, reduce
from itertools import permutations, combinations, product, accumulate, chain

# ============ 0. 输入输出工具 ============
def read_ints():
    return list(map(int, sys.stdin.readline().split()))

def read_int():
    return int(sys.stdin.readline().strip())

def read_str():
    return sys.stdin.readline().strip()

def read_lines(n):
    return [sys.stdin.readline().strip() for _ in range(n)]

# ============ 1. 基本数学工具 ============
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a // gcd(a, b) * b

def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

def prime_factors(n):
    res = []
    i = 2
    while i * i <= n:
        while n % i == 0:
            res.append(i)
            n //= i
        i += 1 if i == 2 else 2
    if n > 1:
        res.append(n)
    return res

def divisors(n):
    res = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            res.append(i)
            if i != n // i:
                res.append(n // i)
        i += 1
    return sorted(res)

# ============ 2. 组合数学 ============
def comb(n, k, mod=None):
    if k < 0 or k > n:
        return 0
    if mod is None:
        import math
        return math.comb(n, k)
    k = min(k, n - k)
    num = den = 1
    for i in range(k):
        num = num * (n - i) % mod
        den = den * (i + 1) % mod
    return num * pow(den, mod - 2, mod) % mod

# ============ 3. 并查集 ============
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x
    def union(self, x, y):
        xr, yr = self.find(x), self.find(y)
        if xr == yr:
            return False
        if self.size[xr] < self.size[yr]:
            xr, yr = yr, xr
        self.parent[yr] = xr
        self.size[xr] += self.size[yr]
        return True
    def connected(self, x, y):
        return self.find(x) == self.find(y)

# ============ 4. 树状数组 BIT ============
class BIT:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)
    def add(self, idx, delta):
        while idx <= self.n:
            self.bit[idx] += delta
            idx += idx & -idx
    def sum(self, idx):
        res = 0
        while idx > 0:
            res += self.bit[idx]
            idx -= idx & -idx
        return res
    def range_sum(self, l, r):
        return self.sum(r) - self.sum(l - 1)

# ============ 5. 线段树 (点更新, 区间查询) ============
class SegTree:
    def __init__(self, data, combine=sum, default=0):
        self.n = len(data)
        self.default = default
        self.combine = combine
        self.size = 1
        while self.size < self.n:
            self.size <<= 1
        self.tree = [default] * (2 * self.size)
        for i, v in enumerate(data):
            self.tree[self.size + i] = v
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = self.combine(self.tree[2*i], self.tree[2*i+1])
    def update(self, idx, value):
        idx += self.size
        self.tree[idx] = value
        idx >>= 1
        while idx:
            self.tree[idx] = self.combine(self.tree[2*idx], self.tree[2*idx+1])
            idx >>= 1
    def query(self, l, r):
        res_l = self.default
        res_r = self.default
        l += self.size
        r += self.size + 1
        while l < r:
            if l & 1:
                res_l = self.combine(res_l, self.tree[l])
                l += 1
            if r & 1:
                r -= 1
                res_r = self.combine(self.tree[r], res_r)
            l >>= 1
            r >>= 1
        return self.combine(res_l, res_r)

# ============ 6. 图论 - 拓扑排序 ============
def topological_sort(n, edges, indeg):
    from collections import deque
    q = deque([i for i in range(n) if indeg[i] == 0])
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in edges[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == n else []

# ============ 7. 图论 - Dijkstra ============
def dijkstra(n, graph, start):
    import heapq
    INF = 10**18
    dist = [INF] * n
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist

# ============ 8. 数论 - 素数筛 ============
def sieve(n):
    is_prime = [True] * (n+1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5)+1):
        if is_prime[i]:
            step = i
            start = i*i
            is_prime[start:n+1:step] = [False] * (((n - start)//step)+1)
    return [i for i, v in enumerate(is_prime) if v]

# ============ 9. 数论 - 扩展欧几里得 ============
def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

# ============ 10. 二分搜索 (标准) ============
def lower_bound(arr, target):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo

def upper_bound(arr, target):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo

# ============ 11. 字符串 - 前缀函数 (KMP) ============
def prefix_function(s):
    n = len(s)
    pi = [0] * n
    for i in range(1, n):
        j = pi[i-1]
        while j > 0 and s[i] != s[j]:
            j = pi[j-1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j
    return pi

def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0:
        return [0]
    pi = prefix_function(pattern)
    res = []
    j = 0
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = pi[j-1]
        if text[i] == pattern[j]:
            j += 1
        if j == m:
            res.append(i - m + 1)
            j = pi[j-1]
    return res

# ============ 12. 矩阵快速幂 ============
def mat_mul(A, B, mod=10**9+7):
    n = len(A)
    m = len(B[0])
    k = len(B)
    C = [[0]*m for _ in range(n)]
    for i in range(n):
        for p in range(k):
            if A[i][p]:
                aip = A[i][p]
                for j in range(m):
                    C[i][j] = (C[i][j] + aip * B[p][j]) % mod
    return C

def mat_pow(mat, exp, mod=10**9+7):
    n = len(mat)
    res = [[1 if i==j else 0 for j in range(n)] for i in range(n)]
    while exp:
        if exp & 1:
            res = mat_mul(res, mat, mod)
        mat = mat_mul(mat, mat, mod)
        exp >>= 1
    return res

# ============ 13. 快速幂 ============
def fast_pow(a, b, mod=None):
    res = 1
    while b:
        if b & 1:
            res = res * a
            if mod:
                res %= mod
        a = a * a
        if mod:
            a %= mod
        b >>= 1
    return res

# ============ 14. Z函数 (Z algorithm) ============
def z_function(s):
    n = len(s)
    z = [0]*n
    l = r = 0
    for i in range(1, n):
        if i <= r:
            z[i] = min(r-i+1, z[i-l])
        while i+z[i] < n and s[z[i]] == s[i+z[i]]:
            z[i] += 1
        if i+z[i]-1 > r:
            l, r = i, i+z[i]-1
    return z

# ============ 15. 单调队列 ============
def monotonic_queue_max(arr, k):
    from collections import deque
    dq = deque()
    res = []
    for i, v in enumerate(arr):
        while dq and arr[dq[-1]] < v:
            dq.pop()
        dq.append(i)
        if dq[0] == i - k:
            dq.popleft()
        if i >= k-1:
            res.append(arr[dq[0]])
    return res

def monotonic_queue_min(arr, k):
    from collections import deque
    dq = deque()
    res = []
    for i, v in enumerate(arr):
        while dq and arr[dq[-1]] > v:
            dq.pop()
        dq.append(i)
        if dq[0] == i - k:
            dq.popleft()
        if i >= k-1:
            res.append(arr[dq[0]])
    return res

# ============ 16. 进制转换 ============
def to_base(num, base):
    digits = []
    while num > 0:
        digits.append(num % base)
        num //= base
    return digits[::-1] if digits else [0]

def from_base(digits, base):
    num = 0
    for d in digits:
        num = num * base + d
    return num

# ============ 17. 滑动窗口 / 双指针 ============
def fixed_sliding_window(arr, k, func=sum):
    # 示例：固定长度滑动窗口求和的另一种通用写法（对任意可加函数）
    # 更常用的直接循环即可
    pass

# ============ 18. 坐标压缩 ============
def compress(arr):
    sorted_unique = sorted(set(arr))
    rank = {v:i for i,v in enumerate(sorted_unique)}
    return [rank[x] for x in arr], sorted_unique

# ============ 19. 最长上升子序列 (LIS) ============
def LIS(arr):
    import bisect
    tails = []
    for x in arr:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)

# ============ 20. 树的重心 / 直径 (递归DFS) ============
def tree_diameter(n, adj):
    # 返回直径长度和路径端点
    def dfs(u, p):
        farthest = u
        maxd = 0
        for v in adj[u]:
            if v == p:
                continue
            vf, d = dfs(v, u)
            d += 1
            if d > maxd:
                maxd = d
                farthest = vf
        return farthest, maxd
    node1, _ = dfs(0, -1)
    node2, diam = dfs(node1, -1)
    return diam, node1, node2

# ============ 21. 拓扑排序 (另一种写法, 基于 defaultdict) ============
def topological_sort_dict(n, edges):
    from collections import defaultdict, deque
    indeg = [0]*n
    g = defaultdict(list)
    for u,v in edges:
        g[u].append(v)
        indeg[v] += 1
    q = deque([i for i in range(n) if indeg[i]==0])
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order)==n else []

# ============ 22. 字典树 (Trie) ============
class TrieNode:
    __slots__ = ('children', 'is_end')
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True
    def search(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end
    def starts_with(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True

# ============ 23. 随机工具 / 快筛 (可选) ============
import random
def random_partition(arr, l, r):
    # 快排分区 (随机轴)
    pivot_idx = random.randint(l, r)
    arr[pivot_idx], arr[r] = arr[r], arr[pivot_idx]
    pivot = arr[r]
    i = l
    for j in range(l, r):
        if arr[j] <= pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[r] = arr[r], arr[i]
    return i

# ============ 24. 主函数入口示例 (使用时需自行编写) ============
def main():
    # 示例: 读取两个整数并求和
    # a, b = read_ints()
    # print(a + b)
    pass

if __name__ == '__main__':
    main()

def judge_and_feedback(value, threshold=10):
    if value > threshold:
        return f"{value} 大于阈值 {threshold}"
    elif value < threshold:
        return f"{value} 小于阈值 {threshold}"
    else:
        return f"{value} 等于阈值 {threshold}"

if __name__ == "__main__":
    test_value = 15
    print(judge_and_feedback(test_value))

if user_answer == correct_answer:
    print("Correct!")

def main():
    print("✓ 回答正确！")

if __name__ == "__main__":
    main()

def check_conditions():
    return True

def process_data(data):
    if len(data) == 0:
        return []
    else:
        result = [x * 2 for x in data if x > 0]
        return result

def get_user_input(prompt):
    return input(prompt)

def check_answer(user_answer, correct_answer):
    if user_answer == correct_answer:
        print("✓ 回答正确！")
        return True
    else:
        print(f"✗ 回答错误！正确答案是: {correct_answer}")
        return False

if __name__ == "__main__":
    correct_answer = "42"
    user_answer = get_user_input("请输入答案: ")
    check_answer(user_answer, correct_answer)

def your_function_name():
    return False

import math
import random
import sys

def step1_get_primes_and_pairs(limit=500):
    """生成小于 limit 的素数列表和所有素数对 (p, p+2)"""
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit+1, i):
                is_prime[j] = False
    primes = [i for i, val in enumerate(is_prime) if val]
    twin_primes = [(p, p+2) for p in primes if p+2 <= limit and is_prime[p+2]]
    return primes, twin_primes, is_prime

def step2_goldbach_check(n, primes_set):
    """验证哥德巴赫猜想：偶数 n 可以表示为两个素数之和（n>=4）"""
    for p in primes_set:
        if p > n/2:
            break
        if (n - p) in primes_set:
            return True
    return False

def step3_riemann_zeta(s, terms=100000):
    """近似计算黎曼ζ(s) 对于 Re(s)>1"""
    total = 0.0
    for n in range(1, terms+1):
        total += 1.0 / (n**s)
    return total

def step4_mobius_mertens(n):
    """计算莫比乌斯函数 μ(n) 和梅滕斯函数 M(n)"""
    mu = [1] * (n+1)
    is_prime = [True] * (n+1)
    primes = []
    for i in range(2, n+1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > n:
                break
            is_prime[i*p] = False
            if i % p == 0:
                mu[i*p] = 0
                break
            else:
                mu[i*p] = -mu[i]
    mertens = [0] * (n+1)
    for i in range(1, n+1):
        mertens[i] = mertens[i-1] + mu[i]
    return mu, mertens

def step5_twin_prime_density(N, primes_set):
    """计算孪生素数密度：π2(N)/N"""
    count = 0
    for p in primes_set:
        if p+2 > N:
            break
        if (p+2) in primes_set:
            count += 1
    return count / N

def main():
    # step1
    primes, twin_primes, is_prime = step1_get_primes_and_pairs(500)
    print("素数（前10个）:", primes[:10])
    print("孪生素数对（前5个）:", twin_primes[:5])
    
    # step2 验证偶数 4 到 100
    primes_set = set(primes)
    goldbach_ok = True
    for even in range(4, 101, 2):
        if not step2_goldbach_check(even, primes_set):
            goldbach_ok = False
            break
    print("哥德巴赫猜想 (4-100) 验证通过:", goldbach_ok)
    
    # step3 计算 ζ(2)
    zeta2 = step3_riemann_zeta(2)
    print("ζ(2) ≈", zeta2, "  理论值 π²/6 ≈", math.pi**2/6)
    
    # step4 计算 Mertens 函数在 100 处的值
    mu, mertens = step4_mobius_mertens(100)
    print("M(100) =", mertens[100])
    
    # step5 密度
    N = 1000
    primes_all, _, _ = step1_get_primes_and_pairs(N)
    primes_all_set = set(primes_all)
    density = step5_twin_prime_density(N, primes_all_set)
    print(f"孪生素数密度 π2({N})/{N} =", density)
    
    # 额外：计算 ζ(3)
    zeta3 = step3_riemann_zeta(3)
    print("ζ(3) ≈", zeta3, "  阿佩里常数 ≈ 1.2020569")

if __name__ == "__main__":
    main()

import unittest
import sys
import os

# ---------- 测试目标函数 ----------
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

# ---------- 测试类 ----------
class TestMathOperations(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(0, 0), 0)

    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(0, 5), -5)
        self.assertEqual(subtract(-1, -1), 0)

# ---------- 运行单个测试 ----------
if __name__ == "__main__":
    # 如果你要运行所有测试：unittest.main()
    # 运行单个测试示例：
    suite = unittest.TestSuite()
    suite.addTest(TestMathOperations('test_add'))   # 只运行 test_add
    runner = unittest.TextTestRunner()
    runner.run(suite)

import json
import sys

def main():
    input_data = sys.stdin.read().strip()
    if not input_data:
        print("[]")
        return
    try:
        data = json.loads(input_data)
    except json.JSONDecodeError:
        print("[]")
        return
    if not isinstance(data, list):
        print("[]")
        return
    result = []
    for item in data:
        try:
            value = float(item)
            if value.is_integer():
                result.append(int(value))
            else:
                result.append(value)
        except (ValueError, TypeError):
            result.append(item)
    print(json.dumps(result))

if __name__ == "__main__":
    main()

word_dict = {}

abandon = "放弃"

def get_academic_translation():
    return "学术的"

print("access: 通道；接近")

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import random

def set_seed(seed=42):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

set_seed()

class Attention(nn.Module):
    def __init__(self, hidden_dim):
        super(Attention, self).__init__()
        self.attn = nn.Linear(hidden_dim, 1, bias=False)

    def forward(self, x):
        weights = torch.softmax(self.attn(x), dim=1)
        return torch.sum(weights * x, dim=1)

class BiLSTMAttention(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, num_layers, num_classes, dropout_prob=0.5):
        super(BiLSTMAttention, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, num_layers, batch_first=True, bidirectional=True, dropout=dropout_prob if num_layers > 1 else 0)
        self.attention = Attention(hidden_dim * 2)
        self.fc = nn.Linear(hidden_dim * 2, num_classes)
        self.dropout = nn.Dropout(dropout_prob)

    def forward(self, x):
        x = self.embedding(x)
        lstm_out, _ = self.lstm(x)
        attn_out = self.attention(lstm_out)
        out = self.dropout(attn_out)
        out = self.fc(out)
        return out

def train_model(model, train_loader, val_loader, num_epochs, learning_rate, device):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    model.to(device)

    for epoch in range(num_epochs):
        model.train()
        total_loss = 0
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        avg_train_loss = total_loss / len(train_loader)
        print(f"Epoch {epoch+1}/{num_epochs}, Train Loss: {avg_train_loss:.4f}")

        model.eval()
        val_loss = 0
        correct = 0
        total = 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                val_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        avg_val_loss = val_loss / len(val_loader)
        val_accuracy = 100 * correct / total
        print(f"Epoch {epoch+1}/{num_epochs}, Val Loss: {avg_val_loss:.4f}, Val Accuracy: {val_accuracy:.2f}%")

    return model

def predict(model, test_loader, device):
    model.eval()
    all_predictions = []
    with torch.no_grad():
        for inputs, _ in test_loader:
            inputs = inputs.to(device)
            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, 1)
            all_predictions.extend(predicted.cpu().numpy())
    return np.array(all_predictions)

def generate_synthetic_data(num_samples=1000, seq_length=20, vocab_size=100, num_classes=2):
    X = np.random.randint(0, vocab_size, (num_samples, seq_length))
    y = np.random.randint(0, num_classes, num_samples)
    return X, y

def run_example():
    num_samples = 500
    seq_length = 15
    vocab_size = 50
    num_classes = 3
    embedding_dim = 64
    hidden_dim = 128
    num_layers = 2
    dropout_prob = 0.5
    batch_size = 32
    num_epochs = 5
    learning_rate = 0.001
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    X, y = generate_synthetic_data(num_samples, seq_length, vocab_size, num_classes)
    split_idx = int(0.8 * len(X))
    X_train, X_val = X[:split_idx], X[split_idx:]
    y_train, y_val = y[:split_idx], y[split_idx:]

    train_dataset = TensorDataset(torch.LongTensor(X_train), torch.LongTensor(y_train))
    val_dataset = TensorDataset(torch.LongTensor(X_val), torch.LongTensor(y_val))
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    model = BiLSTMAttention(vocab_size, embedding_dim, hidden_dim, num_layers, num_classes, dropout_prob)

    trained_model = train_model(model, train_loader, val_loader, num_epochs, learning_rate, device)

    test_samples = 100
    X_test, _ = generate_synthetic_data(test_samples, seq_length, vocab_size, num_classes)
    test_dataset = TensorDataset(torch.LongTensor(X_test), torch.LongTensor(np.zeros(test_samples)))
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    preds = predict(trained_model, test_loader, device)
    print("Predictions shape:", preds.shape)
    print("Sample predictions:", preds[:10])

if __name__ == "__main__":
    run_example()

def accomplish_task():
    pass

accomplish_task()

import json
import os

def step1_prompt_user():
    print("欢迎使用Python代码生成器!")
    name = input("请输入您的名字: ")
    print(f"你好, {name}!")
    return name

def step2_load_data(filename="data.json"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        print("数据加载成功")
        return data
    else:
        print("文件不存在，返回空列表")
        return []

def step3_process_numbers():
    try:
        n = int(input("请输入一个整数: "))
        result = n ** 2
        print(f"{n} 的平方是 {result}")
        return result
    except ValueError:
        print("输入无效，请输入整数")
        return None

def step4_write_file(content, filename="output.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"内容已写入 {filename}")

def step5_read_and_display(filename="output.txt"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        print("文件内容:")
        print(content)
        return content
    else:
        print("文件不存在")
        return ""

def main():
    name = step1_prompt_user()
    data = step2_load_data()
    square = step3_process_numbers()
    if square is not None:
        step4_write_file(f"用户: {name}\n平方结果: {square}\n数据量: {len(data)}")
    step5_read_and_display()

if __name__ == "__main__":
    main()

import sys

# 步骤 1: 定义加密函数
def encrypt(text: str, shift: int) -> str:
    result = []
    for char in text:
        if 'A' <= char <= 'Z':
            result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
        elif 'a' <= char <= 'z':
            result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
        else:
            result.append(char)
    return ''.join(result)

# 步骤 2: 定义解密函数
def decrypt(text: str, shift: int) -> str:
    return encrypt(text, -shift)

# 步骤 3: 主程序入口
if __name__ == "__main__":
    # 步骤 4: 获取用户输入
    mode = input("选择模式 (encrypt/decrypt): ").strip().lower()
    message = input("输入消息: ")
    shift = int(input("输入移位值 (整数): "))

    # 步骤 5: 执行加密或解密
    if mode == "encrypt":
        output = encrypt(message, shift)
    elif mode == "decrypt":
        output = decrypt(message, shift)
    else:
        print("无效模式，请使用 'encrypt' 或 'decrypt'")
        sys.exit(1)

    # 步骤 6: 输出结果
    print("结果:", output)

def run_quiz(word_dict):
    if not word_dict:
        print("No words in the dictionary.")
        return
    correct = 0
    total = len(word_dict)
    for word, meaning in word_dict.items():
        answer = input(f"What is the meaning of '{word}'? ").strip()
        if answer.lower() == meaning.lower():
            print("Correct!")
            correct += 1
        else:
            print(f"Wrong. The correct answer is: {meaning}")
    print(f"\nYou got {correct} out of {total} correct.")

import numpy as np

def step1():
    return np.zeros((4, 4))

def step2(matrix):
    return matrix + 1

def step3(matrix):
    matrix[1:-1, 1:-1] = -1
    return matrix

def step4(matrix):
    diagonal_sum = np.trace(matrix)
    return diagonal_sum

result = step1()
result = step2(result)
result = step3(result)
diag_sum = step4(result)
print(diag_sum)

import random

def generate_random_list(length, min_val=0, max_val=100):
    return [random.randint(min_val, max_val) for _ in range(length)]

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]

        merge_sort(left)
        merge_sort(right)

        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
    return arr

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def linear_search(arr, target):
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1

def main():
    random_list = generate_random_list(10, 0, 50)
    print("原始列表:", random_list)

    sorted_bubble = bubble_sort(random_list.copy())
    print("冒泡排序:", sorted_bubble)

    sorted_selection = selection_sort(random_list.copy())
    print("选择排序:", sorted_selection)

    sorted_insertion = insertion_sort(random_list.copy())
    print("插入排序:", sorted_insertion)

    sorted_merge = merge_sort(random_list.copy())
    print("归并排序:", sorted_merge)

    sorted_quick = quick_sort(random_list.copy())
    print("快速排序:", sorted_quick)

    target = random.choice(sorted_bubble)
    idx = binary_search(sorted_bubble, target)
    print(f"二分查找元素 {target}: 索引 {idx}")

    target2 = random.choice(random_list)
    idx2 = linear_search(random_list, target2)
    print(f"线性查找元素 {target2}: 索引 {idx2}")

if __name__ == "__main__":
    main()

import sys
import json
from typing import Any, Dict, List, Optional

class KeyDesignPoint:
    """
    关键设计点：使用策略模式 + 责任链模式 + 插件化架构
    设计目标：高内聚低耦合、易扩展、可配置
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self._plugins = []
        self._init_plugins()
    
    def _init_plugins(self):
        """初始化插件链"""
        plugin_configs = self.config.get("plugins", [])
        for plugin_cfg in plugin_configs:
            plugin = self._create_plugin(plugin_cfg)
            if plugin:
                self._plugins.append(plugin)
    
    def _create_plugin(self, plugin_cfg: Dict[str, Any]) -> Optional[object]:
        """根据配置创建插件实例"""
        plugin_type = plugin_cfg.get("type")
        if plugin_type == "validator":
            return ValidatorPlugin(plugin_cfg.get("params", {}))
        elif plugin_type == "transformer":
            return TransformerPlugin(plugin_cfg.get("params", {}))
        elif plugin_type == "reporter":
            return ReporterPlugin(plugin_cfg.get("params", {}))
        return None
    
    def process(self, data: Any) -> Any:
        """责任链处理入口"""
        result = data
        for plugin in self._plugins:
            result = plugin.handle(result)
            if result is None:
                break
        return result


class BasePlugin:
    """插件基类 - 策略接口"""
    
    def __init__(self, params: Dict[str, Any]):
        self.params = params
        self.next_plugin = None
    
    def set_next(self, plugin: "BasePlugin") -> "BasePlugin":
        self.next_plugin = plugin
        return plugin
    
    def handle(self, data: Any) -> Any:
        if self.next_plugin:
            return self.next_plugin.handle(data)
        return data


class ValidatorPlugin(BasePlugin):
    """校验插件 - 具体策略"""
    
    def handle(self, data: Any) -> Any:
        if data is None:
            print("[Validator] Data is None, skipping")
            return None
        if not isinstance(data, dict):
            print("[Validator] Invalid data type, expected dict")
            return None
        required_fields = self.params.get("required_fields", [])
        for field in required_fields:
            if field not in data:
                print(f"[Validator] Missing required field: {field}")
                return None
        print(f"[Validator] Validation passed for fields: {list(data.keys())}")
        return super().handle(data)


class TransformerPlugin(BasePlugin):
    """转换插件 - 具体策略"""
    
    def handle(self, data: Any) -> Any:
        if data is None:
            return None
        mapping = self.params.get("field_mapping", {})
        new_data = {}
        for old_key, new_key in mapping.items():
            if old_key in data:
                new_data[new_key] = data[old_key]
        for key, value in data.items():
            if key not in mapping:
                new_data[key] = value
        print(f"[Transformer] Transformed data keys: {list(new_data.keys())}")
        return super().handle(new_data)


class ReporterPlugin(BasePlugin):
    """报告插件 - 具体策略"""
    
    def handle(self, data: Any) -> Any:
        if data is None:
            return None
        print(f"[Reporter] Reporting data: {json.dumps(data, indent=2)}")
        # 模拟输出到文件或数据库
        if self.params.get("output_file"):
            with open(self.params["output_file"], "w") as f:
                json.dump(data, f, indent=2)
            print(f"[Reporter] Data written to {self.params['output_file']}")
        return super().handle(data)


class PluginChainBuilder:
    """责任链构建器 - 建造者模式"""
    
    def __init__(self):
        self._first = None
        self._last = None
    
    def add_plugin(self, plugin: BasePlugin) -> "PluginChainBuilder":
        if self._first is None:
            self._first = plugin
            self._last = plugin
        else:
            self._last.set_next(plugin)
            self._last = plugin
        return self
    
    def build(self) -> BasePlugin:
        return self._first


def main():
    """主函数 - 演示关键设计点的使用"""
    # 配置文件（可以通过YAML/JSON外部化）
    config = {
        "plugins": [
            {
                "type": "validator",
                "params": {
                    "required_fields": ["name", "age", "email"]
                }
            },
            {
                "type": "transformer",
                "params": {
                    "field_mapping": {
                        "name": "full_name",
                        "age": "years_old"
                    }
                }
            },
            {
                "type": "reporter",
                "params": {
                    "output_file": "output.json"
                }
            }
        ]
    }
    
    # 方式1：通过配置自动构建
    system = KeyDesignPoint(config)
    
    test_data = {
        "name": "Alice",
        "age": 30,
        "email": "alice@example.com",
        "extra_field": "some value"
    }
    
    print("=== Processing via config-based chain ===")
    result = system.process(test_data)
    print(f"Final result: {result}")
    
    print("\n=== Processing via manual chain builder ===")
    # 方式2：手动构建责任链
    validator = ValidatorPlugin({"required_fields": ["name", "email"]})
    transformer = TransformerPlugin({"field_mapping": {"name": "username"}})
    reporter = ReporterPlugin({"output_file": "manual_output.json"})
    
    chain = PluginChainBuilder()
    chain.add_plugin(validator).add_plugin(transformer).add_plugin(reporter)
    head = chain.build()
    
    result2 = head.handle(test_data)
    print(f"Final result from manual chain: {result2}")
    
    # 验证可扩展性：添加自定义插件只需继承BasePlugin
    print("\n=== Demonstrating extensibility ===")
    class LoggingPlugin(BasePlugin):
        def handle(self, data):
            print(f"[Logging] Received data: {type(data).__name__}")
            return super().handle(data)
    
    logging_plugin = LoggingPlugin({})
    chain_with_logging = PluginChainBuilder()
    chain_with_logging.add_plugin(logging_plugin).add_plugin(validator).add_plugin(reporter)
    head_logging = chain_with_logging.build()
    head_logging.handle(test_data)


if __name__ == "__main__":
    main()

user_input = input()

def main():
    user_input = input("请输入内容：")
    stripped = user_input.strip()
    print(stripped)

if __name__ == "__main__":
    main()

def compare_answers(user_answer, correct_answer):
    return user_answer == correct_answer

def get_feedback(is_correct):
    if is_correct:
        return "✅ 正确！"
    else:
        return "❌ 错误！"

if __name__ == "__main__":
    test_cases = [True, False]
    for case in test_cases:
        print(get_feedback(case))

from typing import Callable, Any
import inspect

# Step 1: 定义一个装饰器，用于记录函数调用信息
def log_calls(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        # 获取函数签名
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        
        # 准备调用信息
        arg_list = []
        for name, value in bound_args.arguments.items():
            arg_list.append(f"{name}={value!r}")
        
        arg_str = ", ".join(arg_list)
        print(f"Calling {func.__name__}({arg_str})")
        
        # 调用原函数
        result = func(*args, **kwargs)
        print(f"Returned from {func.__name__}: {result!r}")
        
        return result
    return wrapper

# Step 2: 定义一个计算器类，包含加、减、乘、除方法
class Calculator:
    @log_calls
    def add(self, a: float, b: float) -> float:
        return a + b
    
    @log_calls
    def subtract(self, a: float, b: float) -> float:
        return a - b
    
    @log_calls
    def multiply(self, a: float, b: float) -> float:
        return a * b
    
    @log_calls
    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

# Step 3: 创建一个实例并执行所有方法
if __name__ == "__main__":
    calc = Calculator()
    
    # 执行加、减、乘、除操作
    print("=== Calculator Operations ===")
    result1 = calc.add(10, 5)
    result2 = calc.subtract(10, 5)
    result3 = calc.multiply(10, 5)
    result4 = calc.divide(10, 5)
    
    print("\nResults:")
    print(f"add: {result1}")
    print(f"subtract: {result2}")
    print(f"multiply: {result3}")
    print(f"divide: {result4}")

# 第一步：数据准备
# 创建一个包含英语单词和对应中文释义的字典
word_data = {
    "apple": "苹果",
    "book": "书",
    "cat": "猫",
    "dog": "狗",
    "elephant": "大象",
    "flower": "花",
    "garden": "花园",
    "house": "房子",
    "ice": "冰",
    "juice": "果汁"
}

# 第二步：逻辑处理
# 定义测试函数，随机选择单词并判断答案是否正确
import random

def run_test(words_dict):
    words = list(words_dict.keys())
    correct_count = 0
    total_count = 5  # 每次测试5个单词
    
    print("欢迎参加英语单词测试！")
    print(f"你将随机测试 {total_count} 个单词。\n")
    
    # 随机选择要测试的单词
    test_words = random.sample(words, min(total_count, len(words)))
    
    for word in test_words:
        correct_answer = words_dict[word]
        print(f"请输入 '{word}' 的中文意思：")
        user_answer = input().strip()
        
        if user_answer == correct_answer:
            print("回答正确！\n")
            correct_count += 1
        else:
            print(f"回答错误。正确答案是：{correct_answer}\n")
    
    return correct_count, len(test_words)

# 第三步：用户交互
# 让用户选择是否开始测试，并显示测试结果
def main():
    print("===== 英语单词测试程序 =====")
    while True:
        print("请选择操作：")
        print("1. 开始测试")
        print("2. 退出程序")
        choice = input("请输入选择 (1 或 2): ").strip()
        
        if choice == "1":
            correct, total = run_test(word_data)
            print(f"测试完成！你的成绩：{correct}/{total}")
            if correct == total:
                print("太棒了，全部正确！")
            elif correct >= total * 0.6:
                print("不错，继续加油！")
            else:
                print("需要多练习哦！")
            print()
        elif choice == "2":
            print("感谢使用，再见！")
            break
        else:
            print("无效选择，请重新输入。\n")

if __name__ == "__main__":
    main()

