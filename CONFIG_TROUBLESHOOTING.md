# OpenCode AIGW 配置故障排除指南

> **创建时间**: 2025年2月13日  
> **目的**: 记录配置过程中遇到的问题和解决方案，方便在其他电脑上参考

---

## 目录

1. [常见问题](#常见问题)
2. [问题1：Bedrock 配置导致 Claude 调用失败](#问题1bedrock-配置导致-claude-调用失败)
3. [问题2：模型权限不足](#问题2模型权限不足)
4. [问题3：模型代码不正确](#问题3模型代码不正确)
5. [问题4：JSON 语法错误](#问题4json-语法错误)
6. [配置验证步骤](#配置验证步骤)
7. [快速测试命令](#快速测试命令)
8. [其他常见问题](#其他常见问题)

---

## 常见问题

### 问题分类

| 问题类型 | 错误信息 | 解决方案 |
|---------|---------|----------|
| Bedrock 配置 | "invalid json format in [bedrock]" | 移除 Bedrock 配置 |
| 权限不足 | "no available resource for this model" | 在控制台开通权限 |
| 模型代码错误 | "model is not supported" | 检查正确的模型代码 |
| JSON 语法错误 | "JSON parse error" | 修复 JSON 格式 |
| 认证失败 | "401 Unauthorized" | 检查 API Key 格式 |

---

## 问题1：Bedrock 配置导致 Claude 调用失败

### 错误信息
```
invalid json format in [bedrock]
```

### 问题原因
OpenCode 配置中包含了 `bedrock` provider 配置，但 bedrock 的配置格式不正确，导致整个配置文件解析失败。

### 错误配置示例
```json
{
  "bedrock": {
    "npm": "@ai-sdk/bedrock",
    "options": {
      "region": "us-east-1",
      "accessKeyId": "xxx",
      "secretAccessKey": "xxx"
    }
  }
}
```

### 解决方案

#### 方法1：完全移除 Bedrock 配置（推荐）

如果不需要使用 AWS Bedrock，直接移除整个 `bedrock` provider：

```json
{
  "provider": {
    "openai": {
      // ... AIGW 配置
    },
    // 移除 bedrock 配置
  }
}
```

#### 方法2：修复 Bedrock 配置

如果需要使用 Bedrock，确保配置格式正确：

```json
{
  "bedrock": {
    "npm": "@ai-sdk/bedrock",
    "options": {
      "region": "us-east-1",
      "awsAccessKeyId": "your-access-key",
      "awsSecretAccessKey": "your-secret-key"
    }
  }
}
```

### 验证步骤

1. **检查配置是否存在 Bedrock**
   ```bash
   grep -n "bedrock" ~/.config/opencode/opencode.json
   ```

2. **验证 JSON 格式**
   ```bash
   cat ~/.config/opencode/opencode.json | python3 -m json.tool > /dev/null && echo "JSON 格式正确" || echo "JSON 格式错误"
   ```

3. **测试 Claude 调用**
   ```bash
   curl -X POST "https://aigw.netease.com/v1/chat/completions" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_APP_ID.YOUR_APP_KEY" \
     -d '{"model": "claude-opus-4-6", "messages": [{"role": "user", "content": "hi"}], "max_tokens": 10}'
   ```

### 预防措施

- **不使用 Bedrock 时**：直接移除配置，不要留空配置
- **使用 Bedrock 时**：确保使用正确的字段名（`awsAccessKeyId` 而不是 `accessKeyId`）
- **配置前先测试**：使用 curl 测试 API 调用是否正常

---

## 问题2：模型权限不足

### 错误信息
```
no available resource for this model
```

或

```
insufficient quota
```

### 问题原因
- 项目未开通该模型的访问权限
- 账户积分不足
- 超过限流限制

### 解决方案

#### 步骤1：检查控制台权限

1. 访问 [AIGW 控制台](https://aigw.console.nie.netease.com)
2. 登录账号
3. 进入"项目管理"页面
4. 检查项目是否开通了该模型的权限

#### 步骤2：检查积分余额

1. 在控制台中查看"积分余额"
2. 如果积分不足，需要充值

#### 步骤3：检查限流配置

1. 在控制台中查看"限流配置"
2. 确认 RPM/TPM 设置足够

### 常用模型的权限要求

| 模型 | 默认 RPM | 默认 TPM | 是否需要特殊权限 |
|------|---------|---------|-----------------|
| Kimi K2.5 | 120 | 480K | 无 |
| Qwen3 Max | 120 | 300K | 无 |
| Claude Opus 4.6 | 120 | 1M | 可能需要申请 |
| GLM-5 | 60 | 500K | 可能需要申请 |

### 验证步骤

1. **测试不需要权限的模型**
   ```bash
   curl -X POST "https://aigw.netease.com/v1/chat/completions" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_APP_ID.YOUR_APP_KEY" \
     -d '{"model": "kimi-k2.5", "messages": [{"role": "user", "content": "hi"}], "max_tokens": 10}'
   ```

2. **如果 Kimi 可用但其他模型不可用**
   - 说明其他模型需要额外开通权限
   - 访问控制台申请权限

---

## 问题3：模型代码不正确

### 错误信息
```
model is not supported
```

或

```
Unknown model: xxx
```

### 问题原因
- 模型代码拼写错误
- 模型已下架或重命名
- 使用了错误的分隔符（下划线 `-` vs 句点 `.`）

### 解决方案

#### 步骤1：检查正确的模型代码

1. 访问 [ModelSpace](https://modelspace.netease.com/model_app)
2. 搜索需要的模型
3. 查看模型的"模型代号"

#### 步骤2：常见的模型代码错误

| 错误写法 | 正确写法 | 说明 |
|---------|---------|------|
| `claude.opus.4.6` | `claude-opus-4-6` | 使用连字符 `-` |
| `GPT-5.2-Codex` | `gpt-5-2-codex-2026-01-14` | 全部小写，添加日期 |
| `deepseek.v3.2` | `deepseek-chat` 或 `deepseek-v3-2` | 检查官方代码 |

#### 步骤3：验证模型代码

```bash
# 测试模型是否存在
curl -X POST "https://aigw.netease.com/v1/models" \
  -H "Authorization: Bearer YOUR_APP_ID.YOUR_APP_KEY" \
  | grep "model-id"
```

### 常用模型代码速查

| 模型 | 正确代码 | 说明 |
|------|---------|------|
| Claude Opus 4.6 | `claude-opus-4-6` | Anthropic 最新旗舰 |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | Anthropic 平衡模型 |
| Claude Haiku 4.6 | `claude-haiku-4-6` | Anthropic 快速模型 |
| GPT-5.2 Codex | `gpt-5-2-codex-2026-01-14` | OpenAI 编码优化 |
| Kimi K2.5 | `kimi-k2-5` | 月之暗面最新 |
| Qwen3 Max | `qwen3-max-2026-01-23` | 阿里通义千问3 |
| GLM-5 | `glm-5` | 智谱最新旗舰 |
| DeepSeek Chat | `deepseek-chat` | DeepSeek 对话 |
| Doubao Seed 1.8 | `doubao-seed-1-8` | 字节最新 |
| Gemini 3 Flash | `gemini-3-flash` | Google 高效模型 |

---

## 问题4：JSON 语法错误

### 错误信息
```
JSON parse error
```

或

```
Unexpected token
```

### 常见错误

#### 1. 逗号错误
```json
// ❌ 错误：最后一个元素后面有逗号
{
  "model": "test",
}

// ✅ 正确：最后一个元素后面没有逗号
{
  "model": "test"
}
```

#### 2. 引号错误
```json
// ❌ 错误：使用了中文引号
{
  "name": "测试模型"，  // 这里是中文逗号
}

// ✅ 正确：使用英文标点
{
  "name": "测试模型",
}
```

#### 3. 括号不匹配
```json
// ❌ 错误：括号不匹配
{
  "models": {
    "test": { }
  }  // 缺少 }
```

#### 4. 多余的字符
```json
// ❌ 错误：JSON 后面有多余字符
{ ... }
extra text
```

### 验证和修复

#### 方法1：使用 Python 验证
```bash
cat ~/.config/opencode/opencode.json | python3 -m json.tool > /dev/null && echo "✅ JSON 格式正确" || echo "❌ JSON 格式错误"
```

#### 方法2：使用在线工具
- 访问 https://jsonlint.com/
- 粘贴 JSON 内容
- 检查错误并修复

#### 方法3：格式化后检查
```bash
# 格式化 JSON（会显示错误位置）
python3 -m json.tool ~/.config/opencode/opencode.json
```

### 预防措施

1. **使用代码编辑器**（VS Code、Sublime Text）
   - 自动语法高亮
   - 实时错误提示

2. **使用配置文件模板**
   - 不要手动编写 JSON
   - 复制模板后修改

3. **分步测试**
   - 先测试小部分配置
   - 确认无误后再添加更多内容

---

## 配置验证步骤

### 步骤1：验证 JSON 格式

```bash
# 1. 检查文件存在
test -f ~/.config/opencode/opencode.json && echo "✅ 文件存在" || echo "❌ 文件不存在"

# 2. 验证 JSON 格式
cat ~/.config/opencode/opencode.json | python3 -m json.tool > /dev/null && echo "✅ JSON 格式正确" || echo "❌ JSON 格式错误"

# 3. 检查关键配置
grep -q "aigw.netease.com" ~/.config/opencode/opencode.json && echo "✅ AIGW URL 存在" || echo "❌ AIGW URL 不存在"
grep -q "Authorization" ~/.config/opencode/opencode.json && echo "✅ Authorization 存在" || echo "❌ Authorization 不存在"
```

### 步骤2：测试 API 连接

```bash
# 测试基本连接
curl -s "https://aigw.netease.com/v1/models" \
  -H "Authorization: Bearer YOUR_APP_ID.YOUR_APP_KEY" | head -5

# 应该返回模型列表，例如：
# {
#   "object": "list",
#   "data": [...]
# }
```

### 步骤3：测试模型调用

```bash
# 测试 Kimi K2.5（通常权限较宽松）
curl -X POST "https://aigw.netease.com/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_APP_ID.YOUR_APP_KEY" \
  -d '{"model": "kimi-k2-5", "messages": [{"role": "user", "content": "hi"}], "max_tokens": 10}'
```

### 步骤4：检查 OpenCode 启动

1. 重启 OpenCode 应用
2. 查看控制台日志是否有错误
3. 在模型选择器中查看是否能正常显示模型列表

---

## 快速测试命令

### 测试所有已配置模型的命令

```bash
#!/bin/bash

# 测试 Claude Opus 4.6
echo "=== 测试 Claude Opus 4.6 ==="
curl -s -X POST "https://aigw.netease.com/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_APP_ID.YOUR_APP_KEY" \
  -d '{"model": "claude-opus-4-6", "messages": [{"role": "user", "content": "hi"}], "max_tokens": 10}' \
  | python3 -c "import sys, json; print(json.load(sys.stdin)['choices'][0]['message']['content'] if json.load(sys.stdin).get('choices') else '❌ 调用失败')"

# 测试 Kimi K2.5
echo "=== 测试 Kimi K2.5 ==="
curl -s -X POST "https://aigw.netease.com/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_APP_ID.YOUR_APP_KEY" \
  -d '{"model": "kimi-k2-5", "messages": [{"role": "user", "content": "hi"}], "max_tokens": 10}' \
  | python3 -c "import sys, json; print(json.load(sys.stdin)['choices'][0]['message']['content'] if json.load(sys.stdin).get('choices') else '❌ 调用失败')"

# 测试 Qwen3 Max
echo "=== 测试 Qwen3 Max ==="
curl -s -X POST "https://aigw.netease.com/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_APP_ID.YOUR_APP_KEY" \
  -d '{"model": "qwen3-max-2026-01-23", "messages": [{"role": "user", "content": "hi"}], "max_tokens": 10}' \
  | python3 -c "import sys, json; print(json.load(sys.stdin)['choices'][0]['message']['content'] if json.load(sys.stdin).get('choices') else '❌ 调用失败')"
```

### 一键验证配置

```bash
# 保存为 test-aigw.sh，然后运行
bash test-aigw.sh
```

---

## 其他常见问题

### 问题5：认证失败

#### 错误信息
```
401 Unauthorized
```

#### 原因和解决

1. **API Key 格式错误**
   ```bash
   # 正确格式
   Authorization: Bearer APP_ID.APP_KEY
   
   # 例如
   Authorization: Bearer abc123def456.ghi789jkl012
   ```

2. **API Key 已过期**
   - 访问控制台检查 Key 是否有效
   - 如果过期，创建新的 Key

3. **项目被禁用**
   - 检查控制台中项目状态
   - 如果被禁用，需要重新激活

### 问题6：网络连接问题

#### 错误信息
```
Connection timeout
```

或

```
Network error
```

#### 解决

1. **检查网络连接**
   ```bash
   ping -c 3 aigw.netease.com
   ```

2. **检查代理设置**
   - 如果需要代理，确保配置正确
   ```bash
   export HTTP_PROXY="http://proxy:port"
   export HTTPS_PROXY="http://proxy:port"
   ```

3. **检查防火墙**
   - 确保没有阻止到 aigw.netease.com 的连接

### 问题7：限流错误

#### 错误信息
```
429 Too Many Requests
Rate limit exceeded
```

#### 解决

1. **降低请求频率**
   - 添加请求间隔
   - 使用批量处理

2. **调整限流配置**
   - 访问控制台
   - 申请提高限流配额

3. **实现重试机制**
   ```python
   import time
   
   for i in range(3):
       try:
           response = make_request()
           break
       except RateLimitError:
           print(f"限流，等待 30 秒...")
           time.sleep(30)
   ```

### 问题8：OpenCode 无法启动

#### 症状
- OpenCode 启动后立即崩溃
- 控制台显示配置错误

#### 解决

1. **检查配置文件权限**
   ```bash
   chmod 600 ~/.config/opencode/opencode.json
   ```

2. **备份并重新创建配置**
   ```bash
   cp ~/.config/opencode/opencode.json ~/.config/opencode/opencode.json.backup
   # 重新创建配置文件
   ```

3. **查看错误日志**
   ```bash
   # macOS
   ~/Library/Logs/OpenCode/log.txt
   
   # Linux
   ~/.config/opencode/logs/
   ```

---

## 快速参考

### 常用命令

```bash
# 1. 检查配置文件
cat ~/.config/opencode/opencode.json

# 2. 验证 JSON 格式
cat ~/.config/opencode/opencode.json | python3 -m json.tool > /dev/null && echo "✅ 正确" || echo "❌ 错误"

# 3. 测试 API 连接
curl -s "https://aigw.netease.com/v1/models" \
  -H "Authorization: Bearer YOUR_APP_ID.YOUR_APP_KEY"

# 4. 测试模型调用
curl -X POST "https://aigw.netease.com/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_APP_ID.YOUR_APP_KEY" \
  -d '{"model": "kimi-k2-5", "messages": [{"role": "user", "content": "hi"}], "max_tokens": 10}'
```

### 重要链接

| 用途 | 链接 |
|------|------|
| AIGW 控制台 | https://aigw.console.nie.netease.com |
| ModelSpace | https://modelspace.netease.com/model_app |
| API 文档 | https://aigw.doc.nie.netease.com |

### 配置文件位置

```bash
# macOS/Linux
~/.config/opencode/opencode.json

# Windows
C:\Users\<USERNAME>\.config\opencode\opencode.json
```

---

## 预防性维护

### 1. 定期检查配置

```bash
# 每月检查一次
# 1. 验证 JSON 格式
# 2. 测试 API 连接
# 3. 检查控制台权限
```

### 2. 备份配置

```bash
# 每次修改前备份
cp ~/.config/opencode/opencode.json ~/.config/opencode/opencode.json.backup-$(date +%Y%m%d)
```

### 3. 记录修改日志

```markdown
# 配置修改日志

## 2025-02-13
- 添加 Claude Opus 4.6, Kimi K2.5, Qwen3 Max 等模型
- 修复 Bedrock 配置问题
- 验证所有模型可用

## 2025-02-14
- 添加 Gemini 3 系列
- 添加 Doubao Seedream 4.5
```

---

## 总结

### 遇到问题的排查步骤

1. **检查 JSON 格式**
   - 使用 `python3 -m json.tool` 验证

2. **测试 API 连接**
   - 使用 curl 测试基本连接

3. **检查权限**
   - 访问控制台确认已开通权限

4. **检查模型代码**
   - 从 ModelSpace 获取正确代码

5. **查看错误信息**
   - 根据错误信息定位问题

### 求助渠道

1. **查看官方文档**
   - https://aigw.doc.nie.netease.com

2. **检查控制台**
   - 查看项目状态和权限

3. **搜索错误信息**
   - 在搜索引擎中查找解决方案

---

**文档版本**: 1.0.0  
**创建时间**: 2025年2月13日  
**最后更新**: 2025年2月13日
