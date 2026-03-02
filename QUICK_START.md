# 网易 AIGW 快速上手

## 3 步开始使用

### 第 1 步：初始化

在 OpenCode 中执行：

```python
# 初始化（推荐方式）
exec(open(r'~/netease_aigw/skills/aigw_cmd.py', encoding='utf-8').read())

# 或直接导入客户端
from skills.scripts.netease_aigw_client import create_default_client
```

### 第 2 步：创建客户端

```python
client = create_default_client()
```

### 第 3 步：开始对话

```python
response = client.chat(
    model="claude-opus-4-6",
    messages=[{"role": "user", "content": "你好，请介绍一下你自己"}],
    max_tokens=1000
)
print(response["choices"][0]["message"]["content"])
```

---

## 常用示例

### 简单对话

```python
client = create_default_client()
response = client.chat(
    model="claude-opus-4-6",
    messages=[{"role": "user", "content": "你好"}],
    max_tokens=100
)
print(response["choices"][0]["message"]["content"])
```

### 代码生成

```python
code = client.generate_code(
    prompt="写一个 Python 快速排序函数，包含注释",
    max_tokens=500
)
print(code)
```

### 多轮对话

```python
messages = [
    {"role": "user", "content": "什么是装饰器？"}
]
response1 = client.chat(model="claude-opus-4-6", messages=messages, max_tokens=500)
messages.append({"role": "assistant", "content": response1["choices"][0]["message"]["content"]})
messages.append({"role": "user", "content": "能给我一个简单例子吗？"})
response2 = client.chat(model="claude-opus-4-6", messages=messages, max_tokens=500)
print(response2["choices"][0]["message"]["content"])
```

### 流式输出

```python
for chunk in client.chat_stream(
    model="claude-opus-4-6",
    messages=[{"role": "user", "content": "写一段自我介绍"}],
    max_tokens=500
):
    print(chunk, end='', flush=True)
print()
```

---

## /model 命令

### 初始化

```python
exec(open(r'~/netease_aigw/skills/aigw_cmd.py', encoding='utf-8').read())
```

### 命令列表

| 命令 | 说明 |
|------|------|
| `/model` | 查看当前模型 |
| `/model list` | 列出所有模型 |
| `/model claude` | Claude Opus |
| `/model sonnet` | Claude Sonnet |
| `/model deepseek` | DeepSeek |
| `/model gpt` | GPT 系列 |

### 快捷函数

```python
chat("你的问题")        # 当前模型对话
code("生成代码需求")    # Claude 生成代码
```

---

## 支持的模型

| 模型 ID | 用途 |
|---------|------|
| `claude-opus-4-6` | 高级推理、代码 |
| `claude-sonnet-4-6` | 平衡型对话 |
| `claude-haiku-4-6` | 轻量快速 |
| `deepseek-chat` | 高性价比对话 |
| `deepseek-reasoner` | 复杂推理 |

---

## 故障排除

**连接超时？**
```bash
curl -X POST https://aigw.netease.com/v1/chat/completions \
  -H "Authorization: Bearer your_app_id.your_app_key" \
  -H "Content-Type: application/json" \
  -d '{"model":"claude-opus-4-6","messages":[{"role":"user","content":"hi"}],"max_tokens":10}'
```

**认证失败？**
检查 App ID 和 App Key 是否正确。

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `README.md` | 完整使用文档 |
| `QUICK_START.md` | 快速开始 |
| `MODEL_GUIDE.md` | 模型命令 |
| `skills/` | 技能目录 |
