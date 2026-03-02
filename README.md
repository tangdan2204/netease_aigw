# 网易 AIGW (AI Gateway) 接入指南

English | [中文](#中文)

---

## Table of Contents

- [Introduction](#introduction)
- [Quick Start](#quick-start)
- [Account Setup](#account-setup)
- [Installation](#installation)
- [Usage](#usage)
- [Model List](#model-list)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [API Reference](#api-reference)
- [Project Structure](#project-structure)

---

## Introduction

网易 AIGW (AI Gateway) 是网易内部统一的 AI 大模型 API 网关服务，提供对多种主流 AI 模型的统一接入能力。

### Features

- 多模型支持：Claude、DeepSeek、GPT、Qwen、 Gemini、豆包等
- OpenAI 兼容 API 格式
- 流式输出支持 (SSE)
- 完整的错误处理和重试机制
- 多种认证方式
- 成本使用量追踪

### Available Models

| Category | Models |
|----------|--------|
| Claude | opus-4-6, sonnet-4-6, haiku-4-6 |
| DeepSeek | chat, reasoner, v3.2 |
| Qwen | turbo, plus, max, qwen3-max |
| Gemini | 2.5-pro, 2.5-flash, 3-flash |
| Others | kimi-k2.5, doubao-seed, MiniMax-M1 |

---

## Quick Start

### 3 Steps to Get Started

#### Step 1: Clone or Copy the Project

```bash
git clone https://github.com/tangdan2204/netease_aigw.git
cd netease_aigw
```

Or copy the entire `netease_aigw` folder to your desired location.

#### Step 2: Configure Credentials

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# AIGW API Credentials
AIGW_API_KEY=your_app_id.your_app_key

# API Base URL
AIGW_BASE_URL=https://aigw.netease.com/v1
```

#### Step 3: Test Connection

```bash
python test_aigw_claude.py
```

---

## Account Setup

### Getting Credentials

1. Visit [ModelSpace](https://modelspace.netease.com/)
2. Login with your NetEase account
3. Go to "APP Management" (APP 管理)
4. Create a new APP or select an existing one
5. Get `App ID` and `App Key`

### Account Info Format

| Field | Description |
|-------|-------------|
| App ID | Application identifier (e.g., `0ge8s6xq3812chip`) |
| App Key | Application secret key |
| App Code | Application code (optional, e.g., `_codeclaude_model`) |

### Authorization Header Format

```
Authorization: Bearer {app_id}.{app_key}
```

Example:
```
Authorization: Bearer 0ge8s6xq3812chip.r5mmspoybhtuswsgh81wg8gecd6i0l2a
```

---

## Installation

### Environment Requirements

- Python 3.8+
- Network access to aigw.netease.com (or VPN for internal network)

### Install Dependencies

```bash
pip install requests
```

### OpenCode Integration

For OpenCode users, copy the entire `skills` folder to your OpenCode skills directory:

**Windows:**
```cmd
copy skills %USERPROFILE%\.agents\skills\netease_aigw
```

**macOS/Linux:**
```bash
cp -r skills ~/.agents/skills/netease_aigw
```

Or run the installation script:

```bash
# Windows
install.bat

# macOS/Linux
chmod +x install.sh && ./install.sh

# PowerShell
.\install.ps1
```

---

## Usage

### Basic Chat

```python
from skills.scripts.netease_aigw_client import create_default_client

# Create client with default config
client = create_default_client()

# Simple chat
response = client.chat(
    model="claude-sonnet-4-20250514",
    messages=[{"role": "user", "content": "Hello, how are you?"}],
    max_tokens=500
)

print(response["choices"][0]["message"]["content"])
```

### Code Generation

```python
response = client.chat(
    model="claude-opus-4-6",
    messages=[{
        "role": "user",
        "content": "Write a Python quicksort algorithm"
    }],
    max_tokens=1000,
    temperature=0.3  # Low temperature for stable code output
)
```

### Multi-turn Conversation

```python
messages = [
    {"role": "user", "content": "What is a Python decorator?"}
]

# First round
response1 = client.chat(model="claude-opus-4-6", messages=messages, max_tokens=500)
reply1 = response1["choices"][0]["message"]["content"]

# Add to context
messages.append({"role": "assistant", "content": reply1})
messages.append({"role": "user", "content": "Can you give me an example?"})

# Second round
response2 = client.chat(model="claude-opus-4-6", messages=messages, max_tokens=500)
```

### Stream Output

```python
print("AI Response:")
for chunk in client.chat_stream(
    model="claude-opus-4-6",
    messages=[{"role": "user", "content": "Write a story"}],
    max_tokens=1000
):
    print(chunk, end='', flush=True)
print()
```

### Using /model Command

```python
# Initialize model selector
exec(open(r'netease_aigw/skills/aigw_cmd.py', encoding='utf-8').read())

# List available models
/model list

# Switch model
/model claude
/model sonnet
/model deepseek
```

---

## Model List

### Claude Series (Recommended)

| Model ID | Context | Output | Description |
|----------|---------|--------|-------------|
| `claude-opus-4-6` | 200K | 128K | Best for complex reasoning |
| `claude-sonnet-4-20250514` | 200K | 64K | Balanced performance |
| `claude-haiku-4-5-20251001` | 200K | 64K | Fast response |

### DeepSeek Series

| Model ID | Context | Output | Description |
|----------|---------|--------|-------------|
| `deepseek-chat` | 128K | 65K | Cost-effective |
| `deepseek-reasoner` | 128K | 65K | Advanced reasoning |
| `deepseek-v3.2-think-bd-251201` | 128K | 65K | Chain of thought |

### Qwen Series

| Model ID | Context | Output | Description |
|----------|---------|--------|-------------|
| `qwen-turbo` | 128K | 8K | Fast version |
| `qwen-plus` | 128K | 8K | Enhanced version |
| `qwen-max` | 128K | 8K | Best quality |
| `qwen3-max-2026-01-23` | 128K | 8K | Qwen3 Max |

### Gemini Series

| Model ID | Context | Output | Description |
|----------|---------|--------|-------------|
| `gemini-3-flash` | 1M | 65K | Large context |
| `gemini-2.5-pro` | 1M | 65K | Best overall |
| `gemini-2.5-flash` | 1M | 65K | Fast & capable |

### Others

| Model ID | Provider | Description |
|----------|----------|-------------|
| `kimi-k2.5` | Moonshot | Chinese optimized |
| `doubao-seed-1.8` | ByteDance | Fast & cheap |
| `MiniMax-M1` | MiniMax | Balanced |

---

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AIGW_API_KEY` | App ID.App Key | - |
| `AIGW_BASE_URL` | API endpoint | https://aigw.netease.com/v1 |
| `DEFAULT_MODEL` | Default model | claude-sonnet-4-6 |

### Network Options

| Environment | URL | Notes |
|-------------|-----|-------|
| External | `https://aigw.netease.com` | No VPN needed |
| Internal | `https://aigw-int.netease.com` | Requires VPN |

### OpenCode Config Example

Add to your `opencode.json`:

```json
{
  "providers": {
    "netease-aigw": {
      "api_base": "https://aigw.netease.com/v1",
      "api_key": "your_app_id.your_app_key",
      "models": [
        "claude-opus-4-6",
        "claude-sonnet-4-20250514",
        "deepseek-chat"
      ]
    }
  }
}
```

---

## Troubleshooting

### Error: 403 Forbidden

**Cause**: Invalid credentials or IP not whitelisted

**Solution**:
1. Verify App ID and App Key are correct
2. Check if your IP is whitelisted in ModelSpace console

### Error: Connection Timeout

**Solution**:
1. Use external URL: `https://aigw.netease.com`
2. Check VPN settings (use internal URL with VPN)
3. Test network: `ping aigw.netease.com`

### Error: 401 Unauthorized

**Solution**:
1. Check credential format: `Bearer {app_id}.{app_key}`
2. Verify App Key has not expired
3. Ensure API service is enabled in console

### Error: 429 Rate Limited

**Solution**:
```python
import time

def chat_with_retry(client, messages, retries=3):
    for i in range(retries):
        try:
            return client.chat(messages=messages)
        except Exception as e:
            if "429" in str(e):
                wait_time = (i + 1) * 2
                print(f"Rate limited, waiting {wait_time}s...")
                time.sleep(wait_time)
```

---

## API Reference

### NetEaseAIGWClient

```python
NetEaseAIGWClient(
    app_id: str = None,
    app_key: str = None,
    base_url: str = "https://aigw.netease.com",
    timeout: int = 60,
    proxies: dict = None
)
```

### Methods

| Method | Description |
|--------|-------------|
| `chat()` | Send chat request |
| `chat_stream()` | Stream chat response |
| `get_models()` | List available models |
| `get_usage()` | Get usage statistics |

---

## Project Structure

```
netease_aigw/
├── README.md                    # This file
├── QUICK_START.md               # Quick start guide
├── MODEL_GUIDE.md               # Model selection guide
├── AIGW_COMPLETE_GUIDE.md      # Complete guide
├── CONFIG_TROUBLESHOOTING.md    # Troubleshooting
├── MODEL_TEST_RESULTS.md       # Model test results
├── .env.example                 # Environment template
├── config.yaml                  # Configuration
├── requirements.txt             # Python dependencies
│
├── skills/                      # OpenCode skills
│   ├── __init__.py              # Convenient API exports
│   ├── aigw_cmd.py             # /model command
│   ├── model_selector.py        # Interactive model selector
│   ├── examples.py              # Usage examples
│   ├── test_connection.py       # Connection test
│   ├── SKILL.md                 # Skill documentation
│   │
│   ├── scripts/
│   │   └── netease_aigw_client.py  # Core API client
│   │
│   └── references/
│       └── api-spec.md          # API specification
│
├── scripts/                     # Standalone scripts
│   └── netease_aigw_client.py  # API client
│
├── app/                         # Demo FastAPI app
│   ├── main.py                  # FastAPI app
│   ├── config.py                # Configuration
│   ├── models/                  # Database models
│   ├── routers/                 # API routes
│   └── services/                # Business logic
│
├── tests/                       # Unit tests
│   └── test_users.py
│
├── install.bat                  # Windows installer
├── install.ps1                  # PowerShell installer
└── install.sh                   # macOS/Linux installer
```

---

## License

MIT License

---

## Support

- [ModelSpace Console](https://modelspace.netease.com/)
- [Internal Docs](https://aigw.doc.nie.netease.com/) (requires internal network)

---

**Happy Coding!** 🎉

