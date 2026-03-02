# 网易 AIGW 模型完整指南

> 基于 AIGW 官方文档 v2026.02

## 目录

- [快速开始](#快速开始)
- [支持的语言模型](#支持的语言模型)
- [支持的视觉模型](#支持的视觉模型)
- [支持的生图/生视频模型](#支持的生图生视频模型)
- [支持的语音模型](#支持的语音模型)
- [支持的 3D/数字人模型](#支持的-3d数字人模型)
- [模型选择建议](#模型选择建议)
- [特殊功能](#特殊功能)

---

## 快速开始

### /model 命令使用

#### 初始化

```python
exec(open(r'~/netease_aigw/skills/aigw_cmd.py', encoding='utf-8').read())
```

#### 命令列表

| 命令 | 模型 | 说明 |
|------|------|------|
| `/model` | - | 查看当前模型 |
| `/model list` | - | 列出所有模型 |
| `/model claude` | Claude Opus 4.6 | 高级推理 |
| `/model sonnet` | Claude Sonnet 4.6 | 平衡对话 |
| `/model haiku` | Claude Haiku 4.6 | 轻量快速 |
| `/model deepseek` | DeepSeek Chat | 高性价比 |
| `/model reasoner` | DeepSeek Reasoner | 复杂推理 |

#### 快捷函数

```python
chat("问题")       # 当前模型对话
code("需求")       # Claude 生成代码
```

---

## 支持的语言模型

### Anthropic Claude

| 模型 ID | 描述 | 特点 |
|---------|------|------|
| `claude-opus-4-6` | Claude Opus 4.6 | 高级推理、复杂任务 |
| `claude-sonnet-4-6` | Claude Sonnet 4.6 | 平衡性能与速度 |
| `claude-haiku-4-6` | Claude Haiku 4.6 | 轻量快速响应 |

**特点：**
- 支持 Prompt 缓存
- 支持工具调用
- 支持思维链模式

---

### DeepSeek

| 模型 ID | 描述 | 特点 |
|---------|------|------|
| `deepseek-chat` | DeepSeek Chat | 通用对话、高性价比 |
| `deepseek-reasoner` | DeepSeek Reasoner | 复杂推理任务 |
| `deepseek-v3-latest` | DeepSeek V3 最新版 | 增强推理能力 |

**特点：**
- 思维链模式支持
- 工具调用支持
- 联网搜索支持

---

### OpenAI

| 模型 ID | 描述 | 特点 |
|---------|------|------|
| `gpt-4o` | GPT-4 Omni | 多模态、平衡性能 |
| `gpt-4o-mini` | GPT-4o Mini | 轻量、成本低 |
| `o1` | GPT o1 | 深度推理 |
| `o3-mini` | GPT o3-mini | 快速推理 |

---

### 字节跳动 豆包

| 模型 ID | 描述 | 特点 |
|---------|------|------|
| `doubao-pro-32k` | 豆包 Pro 32K | 中文优化 |
| `doubao-pro-128k` | 豆包 Pro 128K | 长上下文 |
| `doubao-thinking` | 豆包思考版 | 推理增强 |

---

### Google Gemini

| 模型 ID | 描述 | 特点 |
|---------|------|------|
| `gemini-2-0-flash` | Gemini 2.0 Flash | 快速响应 |
| `gemini-2-0-flash-thinking` | Gemini 2.0 思考版 | 推理增强 |
| `gemini-1-5-pro` | Gemini 1.5 Pro | 长上下文（200万 token） |
| `gemini-1-5-flash` | Gemini 1.5 Flash | 轻量快速 |

---

### 阿里 通义千问

| 模型 ID | 描述 | 特点 |
|---------|------|------|
| `qwen-turbo` | 通义千问 Turbo | 快速响应 |
| `qwen-plus` | 通义千问 Plus | 平衡性能 |
| `qwen-max` | 通义千问 Max | 高质量输出 |
| `qwen-long` | 通义千问 Long | 超长上下文 |

---

### Moonshot Kimi

| 模型 ID | 描述 | 特点 |
|---------|------|------|
| `kimi2-5-thinking` | Kimi 2.5 思考版 | 推理增强 |
| `kimi-a14b` | Kimi A14B | 学术研究 |

---

### 智谱 ChatGLM

| 模型 ID | 描述 | 特点 |
|---------|------|------|
| `glm-4-plus` | GLM-4 Plus | 高质量对话 |
| `glm-4v` | GLM-4V | 视觉理解 |

---

### MiniMax

| 模型 ID | 描述 | 特点 |
|---------|------|------|
| `abab6-5s-chat` | MiniMax 6.5B | 快速响应 |
| `abab6-5s-thinking` | MiniMax 6.5B 思考 | 推理增强 |

---

### 百度 ERNIE

| 模型 ID | 描述 | 特点 |
|---------|------|------|
| `ernie-4-5-turbo` | 文心 4.5 Turbo | 中文优化 |
| `ernie-x1` | 文心 X1 | 深度推理 |

---

### 有道

| 模型 ID | 描述 | 特点 |
|---------|------|------|
| `deepseek-chat-yd` | 有道 DeepSeek | 深度推理 |
| `hanyu-a13b` | 翰宇 | 学术研究 |

---

### Tmax

| 模型 ID | 描述 | 特点 |
|---------|------|------|
| `qwq-32b` | QwQ 32B | 推理增强 |
| `gemma-27b-it` | Gemma 27B | 指令遵循 |

---

## 支持的视觉模型

### Claude 视觉

| 模型 ID | 描述 | 输入限制 |
|---------|------|----------|
| `claude-opus-4-6` | 高级视觉理解 | 图片/文档 |
| `claude-sonnet-4-6` | 平衡视觉 | 图片/文档 |

---

### GPT 视觉

| 模型 ID | 描述 | 输入限制 |
|---------|------|----------|
| `gpt-4o` | 多模态理解 | 图片/文档/视频 |
| `gpt-4o-mini` | 轻量视觉 | 图片 |

---

### Gemini 视觉

| 模型 ID | 描述 | 特点 |
|---------|------|------|
| `gemini-1-5-pro` | 多模态理解 | 长上下文 |
| `gemini-2-0-flash` | 快速视觉 | 低延迟 |

---

### 豆包视觉

| 模型 ID | 描述 | 特点 |
|---------|------|------|
| `doubao-vision-pro` | 豆包视觉 | 中文优化 |

---

### 通义千问 VL

| 模型 ID | 描述 | 特点 |
|---------|------|------|
| `qwen-vl-max` | 通义千问 VL | 视觉理解 |

---

### 方舟视觉

| 模型 ID | 描述 | 特点 |
|---------|------|------|
| `doubao-seedream-4-0` | 方舟视觉 4.0 | 高质量 |

---

## 支持的生图/生视频模型

### 智能绘图（字节方舟）

| 模型 ID | 描述 | 特点 |
|---------|------|------|
| `doubao-seedream-4-0-i2i` | 图生图 | 图片编辑 |
| `doubao-seedream-4-0-t2i` | 文生图 | 高质量生成 |

---

### 豆包生图

| 模型 ID | 描述 | 特点 |
|---------|------|------|
| `doubao-i2v-1-0` | 图生视频 | 视频生成 |
| `doubao-t2v-1-0` | 文生视频 | 视频生成 |

---

### Google Veo

| 模型 ID | 描述 | 特点 |
|---------|------|------|
| `veo-2` | Veo 2 | 高质量视频 |
| `veo-3` | Veo 3 | 视频+音频 |

---

### MiniMax 海螺

| 模型 ID | 描述 | 特点 |
|---------|------|------|
| `hailuo-i2v` | 海螺图生视频 | 高流畅度 |

---

### Runway

| 模型 ID | 描述 | 特点 |
|---------|------|------|
| `gen-3-alpha-turbo` | Gen-3 | 视频生成 |

---

### Midjourney 悠船

| 模型 ID | 描述 | 特点 |
|---------|------|------|
| `悠船` | Midjourney 中文版 | 艺术风格 |

---

### 可灵 AI

| 模型 ID | 描述 | 特点 |
|---------|------|------|
| `kling-1-0` | 可灵 | 视频生成 |
| `kling-1-0-pro` | 可灵专业版 | 高质量 |

---

### Black Forest Labs

| 模型 ID | 描述 | 特点 |
|---------|------|------|
| `flux-1-pro` | FLUX Pro | 高质量生图 |
| `flux-schnell` | FLUX Schnell | 快速生图 |

---

### Tripo

| 模型 ID | 描述 | 特点 |
|---------|------|------|
| `tripo-3d` | Tripo 3D | 3D 模型生成 |

---

## 支持的语音模型

### 豆包语音

| 模型 ID | 描述 | 特点 |
|---------|------|------|
| `doubao-asr` | 语音识别 | 多语言 |
| `doubao-tts` | 语音合成 | 自然流畅 |
| `doubao-tts-pro` | TTS 专业版 | 多音色 |

---

### MiniMax 语音

| 模型 ID | 描述 | 特点 |
|---------|------|------|
| `minimax-asr` | 语音识别 | 实时转写 |
| `minimax-tts` | 语音合成 | 高保真 |

---

### 通义千问 ASR/Omni

| 模型 ID | 描述 | 特点 |
|---------|------|------|
| `qwen-asr` | 语音识别 | 实时转写 |
| `qwen-omni` | 全能语音 | 语音交互 |

---

## 支持的 3D/数字人模型

### Rodin 数字人

| 模型 ID | 描述 | 特点 |
|---------|------|------|
| `rodin-1-0` | 数字人生成 | 3D 数字人 |

---

### Hitem 3D

| 模型 ID | 描述 | 特点 |
|---------|------|------|
| `hitem-3d-1` | 3D 建模 | 3D 模型 |

---

## 模型选择建议

### 按场景选择

| 场景 | 推荐模型 | 温度 |
|------|---------|------|
| 代码生成 | `claude-opus-4-6` | 0.2-0.3 |
| 代码审查 | `claude-opus-4-6` | 0.3 |
| 日常对话 |onnet-4- `claude-s6` | 0.7 |
| 成本敏感 | `deepseek-chat` | 0.7 |
| 复杂推理 | `deepseek-reasoner` | 0.1 |
| 长上下文 | `doubao-pro-128k` | 0.7 |
| 中文优化 | `doubao-pro-32k` | 0.7 |
| 超长文本 | `gemini-1-5-pro` | 0.7 |

---

### 按预算选择

| 预算 | 推荐模型 |
|------|---------|
| 高预算 | Claude Opus / GPT-4o |
| 中预算 | Claude Sonnet / DeepSeek |
| 低预算 | Claude Haiku / GPT-4o-mini |

---

## 特殊功能

### Prompt 缓存

支持 Prompt 缓存的模型（减少重复上下文费用）：

| 供应商 | 模型 |
|--------|------|
| Claude | 所有模型 |
| DeepSeek | deepseek-chat |
| GLM | glm-4-plus |

**使用方法：** 传 `cache_control` 参数

```python
response = client.chat(
    model="claude-opus-4-6",
    messages=messages,
    max_tokens=1000,
)
```

---

### 工具调用

支持工具调用的模型：

| 供应商 | 工具类型 |
|--------|----------|
| Claude | 函数调用 |
| GPT-4o | 函数调用 |
| DeepSeek | 工具调用 |
| Gemini | 工具调用 |

---

### 联网搜索

支持联网搜索的模型：

| 模型 | 说明 |
|------|------|
| `deepseek-chat` | 支持 |
| `deepseek-reasoner` | 支持 |
| `gemini-1-5-pro` | 支持 |
| `doubao-thinking` | 支持 |

---

### 思维链模式

支持思维链（CoT）的模型：

| 模型 | 启用方式 |
|------|----------|
| `deepseek-reasoner` | 默认启用 |
| `gemini-2-0-flash-thinking` | `thinking.type: enabled` |
| `claude-opus-4-6` | 默认支持 |

---

## 相关资源

- **ModelSpace**: https://modelspace.netease.com/
- **AIGW 文档**: https://aigw.doc.nie.netease.com/
- **Auth 控制台**: https://console-auth.nie.netease.com/mymessage/mymessage

---

*最后更新时间: 2026-02-12* |
