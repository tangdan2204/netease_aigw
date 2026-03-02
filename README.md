# 网易 AIGW (AI Gateway) 接入指南

网易 AIGW 是网易内部统一的 AI 大模型 API 网关服务，提供对 Claude、DeepSeek、GPT、Qwen、 Gemini、豆包等主流 AI 模型的统一接入能力。

---

## 目录

- [快速开始](#快速开始)
- [账号申请与配置](#账号申请与配置)
- [环境要求](#环境要求)
- [安装部署](#安装部署)
- [配置说明](#配置说明)
- [使用示例](#使用示例)
- [模型列表](#模型列表)
- [API 参考](#api-参考)
- [故障排除](#故障排除)
- [项目结构](#项目结构)

---

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/tangdan2204/netease_aigw.git
cd netease_aigw
```

### 2. 配置凭证

创建 `.env` 文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 AIGW 凭证：

```env
# AIGW API 凭证（必填）
# 格式：{AppID}.{AppKey}
AIGW_API_KEY=your_app_id.your_app_key

# API 地址（可选，默认使用外网地址）
AIGW_BASE_URL=https://aigw.netease.com/v1
```

### 3. 测试连接

```bash
python test_aigw_claude.py
```

---

## 账号申请与配置

### 获取凭证步骤

1. 访问 [ModelSpace 控制台](https://modelspace.netease.com/)
2. 使用网易内部账号登录
3. 进入「APP 管理」
4. 创建新 APP 或选择已有 APP
5. 获取 `App ID` 和 `App Key`

### 凭证格式说明

| 字段 | 说明 | 示例 |
|------|------|------|
| App ID | 应用标识符 | `0ge8s6xq3812chip` |
| App Key | 应用密钥 | `r5mmspoybhtuswsgh81wg8gecd6i0l2a` |
| App Code | 应用代码（可选） | `_codeclaude_model` |

### 认证头格式

```
Authorization: Bearer {AppID}.{AppKey}
```

**示例：**
```
Authorization: Bearer 0ge8s6xq3812chip.r5mmspoybhtuswsgh81wg8gecd6i0l2a
```

### 网络环境选择

| 环境 | 地址 | 说明 |
|------|------|------|
| 外网 | `https://aigw.netease.com` | 无需 VPN，办公网可直接访问 |
| 内网 | `https://aigw-int.netease.com` | 需要 VPN 连接 |

---

## 环境要求

### Python 环境

- Python 3.8+
- requests 库

```bash
pip install requests
```

### 网络要求

- 能够访问 `aigw.netease.com`（外网环境）
- 或通过 VPN 访问 `aigw-int.netease.com`（内网环境）

---

## 安装部署

### 方式一：OpenCode 集成

将 `skills` 文件夹复制到 OpenCode 技能目录：

**Windows:**
```cmd
copy skills %USERPROFILE%\.agents\skills\netease_aigw
```

**macOS/Linux:**
```bash
cp -r skills ~/.agents/skills/netease_aigw
```

### 方式二：运行安装脚本

```bash
# Windows
install.bat

# macOS/Linux
chmod +x install.sh && ./install.sh

# PowerShell
.\install.ps1
```

### 方式三：独立 Python 脚本使用

将项目路径添加到 Python 路径或直接引用：

```python
import sys
sys.path.insert(0, '/path/to/netease_aigw')

from skills.scripts.netease_aigw_client import create_default_client
```

---

## 配置说明

### 环境变量配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `AIGW_API_KEY` | App ID.App Key 凭证 | - |
| `AIGW_BASE_URL` | API 端点地址 | `https://aigw.netease.com/v1` |
| `DEFAULT_MODEL` | 默认模型 | `claude-sonnet-4-6` |

### OpenCode 配置模板

如果你使用 OpenCode，可以在 `opencode.json` 中添加以下配置：

```json
{
  "providers": {
    "netease-aigw": {
      "api_base": "https://aigw.netease.com/v1",
      "api_key": "your_app_id.your_app_key",
      "models": [
        "claude-opus-4-6",
        "claude-sonnet-4-20250514",
        "claude-haiku-4-5-20251001",
        "deepseek-chat",
        "deepseek-reasoner",
        "qwen-turbo",
        "qwen-plus",
        "qwen-max",
        "gemini-2.5-pro",
        "gemini-2.5-flash"
      ]
    }
  }
}
```

### 配置文件优先级

1. 代码中直接传入参数（最高优先级）
2. 环境变量
3. 配置文件
4. 默认值（最低优先级）

---

## 使用示例

### 基础对话

```python
from skills.scripts.netease_aigw_client import create_default_client

# 创建客户端（会自动读取环境变量）
client = create_default_client()

# 简单对话
response = client.chat(
    model="claude-sonnet-4-20250514",
    messages=[{"role": "user", "content": "你好，请介绍一下你自己"}],
    max_tokens=500
)

print(response["choices"][0]["message"]["content"])
```

### 代码生成

```python
response = client.chat(
    model="claude-opus-4-6",
    messages=[{
        "role": "user",
        "content": "写一个 Python 类，实现二叉搜索树的基本操作（插入、查找、删除）"
    }],
    max_tokens=2000,
    temperature=0.3  # 低温度，更稳定的代码输出
)

print(response["choices"][0]["message"]["content"])
```

### 多轮对话

```python
messages = [
    {"role": "user", "content": "什么是 Python 装饰器？"}
]

# 第一轮
response1 = client.chat(model="claude-opus-4-6", messages=messages, max_tokens=500)
reply1 = response1["choices"][0]["message"]["content"]

# 添加到上下文
messages.append({"role": "assistant", "content": reply1})
messages.append({"role": "user", "content": "能给我一个简单例子吗？"})

# 第二轮
response2 = client.chat(model="claude-opus-4-6", messages=messages, max_tokens=500)
print(response2["choices"][0]["message"]["content"])
```

### 流式输出

```python
print("AI 回复：")
for chunk in client.chat_stream(
    model="claude-opus-4-6",
    messages=[{"role": "user", "content": "请写一段 500 字的自我介绍"}],
    max_tokens=1000
):
    print(chunk, end='', flush=True)
print()
```

### 使用 /model 命令

```python
# 初始化模型选择器
exec(open(r'netease_aigw/skills/aigw_cmd.py', encoding='utf-8').read())

# 查看可用模型
/model list

# 切换模型
/model claude
/model sonnet
/model deepseek
```

### 命令行测试

```bash
# 测试连接
python test_aigw_claude.py

# 快速对话
python test_aigw_claude.py "你好，请介绍一下你自己"
```

---

## 模型列表

### Claude 系列（推荐）

| 模型 ID | 上下文长度 | 输出长度 | 适用场景 |
|---------|-----------|---------|----------|
| `claude-opus-4-6` | 200K | 128K | 最强推理、复杂任务 |
| `claude-sonnet-4-20250514` | 200K | 64K | 平衡性能与速度 |
| `claude-haiku-4-5-20251001` | 200K | 64K | 快速响应 |
| `claude-3-7-sonnet-20250219` | 200K | 64K | Claude 3.7 |
| `claude-3-5-sonnet-20241022` | 200K | 8K | Claude 3.5 |
| `claude-3-5-haiku-20241022` | 200K | 8K | 轻量快速 |

### DeepSeek 系列

| 模型 ID | 上下文长度 | 输出长度 | 适用场景 |
|---------|-----------|---------|----------|
| `deepseek-chat` | 128K | 65K | 通用对话、高性价比 |
| `deepseek-reasoner` | 128K | 65K | 复杂推理任务 |
| `deepseek-v3.2-think-bd-251201` | 128K | 65K | 思维链模型 |

### Qwen 系列

| 模型 ID | 上下文长度 | 输出长度 | 适用场景 |
|---------|-----------|---------|----------|
| `qwen-turbo` | 128K | 8K | 快速版 |
| `qwen-plus` | 128K | 8K | 增强版 |
| `qwen-max` | 128K | 8K | 高级版 |
| `qwen3-max-2026-01-23` | 128K | 8K | Qwen3 Max |

### Gemini 系列

| 模型 ID | 上下文长度 | 输出长度 | 适用场景 |
|---------|-----------|---------|----------|
| `gemini-3-flash` | 1M | 65K | 超大上下文 |
| `gemini-2.5-pro` | 1M | 65K | 综合能力最强 |
| `gemini-2.5-flash` | 1M | 65K | 快速且能力强 |

### 其他模型

| 模型 ID | 提供商 | 上下文长度 | 说明 |
|---------|--------|-----------|------|
| `kimi-k2.5` | 月之暗面 | 262K | 中文优化 |
| `doubao-seed-1.8` | 字节豆包 | 256K | 快速便宜 |
| `MiniMax-M1` | MiniMax | 128K | 平衡型 |

### 模型选择建议

| 场景 | 推荐模型 | 温度 |
|------|---------|------|
| 代码生成 | `claude-opus-4-6` | 0.2-0.3 |
| 通用对话 | `claude-sonnet-4-20250514` | 0.7 |
| 创意写作 | `claude-sonnet-4-20250514` | 0.8-0.9 |
| 成本敏感 | `deepseek-chat` | 0.7 |
| 中文优化 | `qwen-max` | 0.7 |
| 超长文档 | `gemini-3-flash` | 0.5 |

---

## API 参考

### NetEaseAIGWClient 类

```python
NetEaseAIGWClient(
    app_id: str = None,          # App ID
    app_key: str = None,         # App Key
    base_url: str = "https://aigw.netease.com",  # API 地址
    timeout: int = 60,           # 超时时间（秒）
    proxies: dict = None         # 代理配置
)
```

### 方法说明

| 方法 | 说明 |
|------|------|
| `chat()` | 发送聊天请求，返回完整响应 |
| `chat_stream()` | 流式聊天响应，逐块返回 |
| `get_models()` | 获取可用模型列表 |
| `get_usage()` | 获取使用量统计 |

### chat() 方法参数

```python
client.chat(
    model: str,                  # 模型 ID
    messages: list,               # 消息列表
    max_tokens: int = 1000,      # 最大输出 tokens
    temperature: float = 0.7,    # 温度参数 (0-2)
    stream: bool = False,         # 是否流式输出
    top_p: float = 1.0,          # top_p 采样
    stop: list = None            # 停止词列表
)
```

### 消息格式

```python
messages = [
    {"role": "system", "content": "你是一个专业编程助手"},
    {"role": "user", "content": "用户问题"},
    {"role": "assistant", "content": "AI 回复"},  # 可选，历史对话
    {"role": "user", "content": "追问"}
]
```

---

## 故障排除

### 问题 1：403 Forbidden

**原因：**
- 凭证无效或过期
- IP 未在白名单中
- API 服务未开通

**解决方案：**
1. 登录 [ModelSpace 控制台](https://modelspace.netease.com/) 确认凭证正确
2. 检查是否配置了 IP 白名单
3. 确认 APP 已开通 API 服务权限

### 问题 2：连接超时

**原因：**
- 网络不通
- 代理配置错误

**解决方案：**
1. 确认使用正确的网络环境（外网/内网）
2. 检查网络连通性：`ping aigw.netease.com`
3. 如需代理，配置代理：

```python
client = NetEaseAIGWClient(
    app_id="your_app_id",
    app_key="your_app_key",
    proxies={
        "http": "http://proxy:port",
        "https": "http://proxy:port"
    }
)
```

### 问题 3：401 Unauthorized

**原因：**
- 认证头格式错误
- App Key 已过期

**解决方案：**
1. 确认认证头格式：`Bearer {app_id}.{app_key}`
2. 在控制台重新生成 App Key

### 问题 4：429 Rate Limited（限流）

**原因：**
- 请求频率过高
- 超出配额

**解决方案：**
```python
import time

def chat_with_retry(client, messages, retries=3):
    for i in range(retries):
        try:
            return client.chat(messages=messages)
        except Exception as e:
            if "429" in str(e):
                wait_time = (i + 1) * 2
                print(f"限流，等待 {wait_time} 秒...")
                time.sleep(wait_time)
            else:
                raise e
```

### 快速测试命令

```bash
# 使用 curl 测试
curl -X POST "https://aigw.netease.com/v1/chat/completions" \
  -H "Authorization: Bearer your_app_id.your_app_key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-opus-4-6",
    "messages": [{"role": "user", "content": "hi"}],
    "max_tokens": 10
  }'
```

---

## 项目结构

```
netease_aigw/
├── README.md                    # 本文件
├── QUICK_START.md               # 快速开始指南
├── MODEL_GUIDE.md               # 模型选择指南
├── AIGW_COMPLETE_GUIDE.md       # 完整接入指南
├── CONFIG_TROUBLESHOOTING.md    # 故障排查指南
├── MODEL_TEST_RESULTS.md        # 模型测试结果
├── .env.example                 # 环境变量模板
├── config.yaml                  # 配置文件
├── requirements.txt             # Python 依赖
│
├── skills/                      # OpenCode 技能
│   ├── __init__.py              # 便捷 API 导出
│   ├── aigw_cmd.py              # /model 命令
│   ├── model_selector.py        # 交互式模型选择器
│   ├── examples.py              # 使用示例
│   ├── test_connection.py        # 连接测试
│   ├── SKILL.md                 # 技能文档
│   │
│   ├── scripts/
│   │   └── netease_aigw_client.py  # 核心 API 客户端
│   │
│   └── references/
│       └── api-spec.md          # API 规范
│
├── scripts/                     # 独立脚本
│   └── netease_aigw_client.py  # API 客户端
│
├── app/                         # Demo FastAPI 应用
│   ├── main.py                  # FastAPI 主程序
│   ├── config.py                # 配置
│   ├── models/                  # 数据模型
│   ├── routers/                 # API 路由
│   └── services/                # 业务逻辑
│
├── tests/                       # 单元测试
│   └── test_users.py
│
├── install.bat                  # Windows 安装脚本
├── install.ps1                  # PowerShell 安装脚本
├── install.sh                   # macOS/Linux 安装脚本
└── test_aigw_claude.py          # 测试脚本
```

---

## 相关资源

- [ModelSpace 控制台](https://modelspace.netease.com/) - APP 管理
- [内部文档](https://aigw.doc.nie.netease.com/) - 官方文档（需内网访问）

---

**祝你使用愉快！** 🎉
