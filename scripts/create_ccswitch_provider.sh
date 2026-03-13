#!/bin/bash
# create_ccswitch_provider.sh - 快速创建 CC Switch Provider
#
# 用法:
#   ./create_ccswitch_provider.sh <provider_id> <provider_name> <model_id> <api_key> <api_format>
#
# 示例:
#   ./create_ccswitch_provider.sh "aigw-codex" "AIGW Codex" "gpt-5.2-codex-2026-01-14" "appid.appkey" "openai_chat"
#   ./create_ccswitch_provider.sh "aigw-claude" "AIGW Claude" "claude-opus-4-6" "appid.appkey" "anthropic"
#
# apiFormat 说明:
#   - "anthropic"    : Claude 系列模型使用
#   - "openai_chat"  : 所有其他模型使用（GPT、Codex、DeepSeek、Qwen、Gemini 等）

set -e

PROVIDER_ID=$1
PROVIDER_NAME=$2
MODEL_ID=$3
API_KEY=$4
API_FORMAT=${5:-"openai_chat"}

DB_PATH="$HOME/.cc-switch/cc-switch.db"

if [ -z "$PROVIDER_ID" ] || [ -z "$PROVIDER_NAME" ] || [ -z "$MODEL_ID" ] || [ -z "$API_KEY" ]; then
    echo "用法: $0 <provider_id> <provider_name> <model_id> <api_key> [api_format]"
    echo ""
    echo "参数说明:"
    echo "  provider_id   : 唯一标识符，例如 aigw-codex"
    echo "  provider_name : 显示名称，例如 \"AIGW Codex\""
    echo "  model_id      : AIGW 模型代号，例如 gpt-5.2-codex-2026-01-14"
    echo "  api_key       : AIGW 凭证，格式为 AppID.AppKey"
    echo "  api_format    : 可选，默认 openai_chat（Claude 系列用 anthropic）"
    echo ""
    echo "示例:"
    echo "  $0 \"aigw-codex\" \"AIGW Codex\" \"gpt-5.2-codex-2026-01-14\" \"xxxx.yyyy\" \"openai_chat\""
    echo "  $0 \"aigw-claude\" \"AIGW Claude\" \"claude-opus-4-6\" \"xxxx.yyyy\" \"anthropic\""
    exit 1
fi

if [ ! -f "$DB_PATH" ]; then
    echo "错误: CC Switch 数据库不存在: $DB_PATH"
    echo "请确保已安装并运行过 CC Switch"
    exit 1
fi

# 检查 apiFormat 值
if [ "$API_FORMAT" != "openai_chat" ] && [ "$API_FORMAT" != "anthropic" ]; then
    echo "警告: apiFormat 值 '$API_FORMAT' 可能不正确"
    echo "  - Claude 系列: 使用 'anthropic'"
    echo "  - 其他模型:    使用 'openai_chat'"
    read -p "是否继续? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 检查是否已存在
EXISTING=$(sqlite3 "$DB_PATH" "SELECT count(*) FROM providers WHERE id = '$PROVIDER_ID' AND app_type = 'claude';")
if [ "$EXISTING" -gt 0 ]; then
    echo "Provider '$PROVIDER_ID' 已存在，正在更新..."
    sqlite3 "$DB_PATH" "UPDATE providers SET
        name = '$PROVIDER_NAME',
        settings_config = '{\"env\":{\"ANTHROPIC_AUTH_TOKEN\":\"$API_KEY\",\"ANTHROPIC_BASE_URL\":\"https://aigw.netease.com\",\"ANTHROPIC_MODEL\":\"$MODEL_ID\",\"ANTHROPIC_DEFAULT_HAIKU_MODEL\":\"$MODEL_ID\",\"ANTHROPIC_DEFAULT_SONNET_MODEL\":\"$MODEL_ID\",\"ANTHROPIC_DEFAULT_OPUS_MODEL\":\"$MODEL_ID\",\"ANTHROPIC_REASONING_MODEL\":\"$MODEL_ID\",\"ANTHROPIC_VERSION\":\"2023-06-01\"},\"includeCoAuthoredBy\":false}',
        meta = '{\"endpointAutoSelect\":true,\"apiFormat\":\"$API_FORMAT\"}'
    WHERE id = '$PROVIDER_ID' AND app_type = 'claude';"
    echo "已更新 Provider: $PROVIDER_NAME"
else
    sqlite3 "$DB_PATH" "INSERT INTO providers (id, app_type, name, settings_config, meta, is_current, provider_type) VALUES (
        '$PROVIDER_ID',
        'claude',
        '$PROVIDER_NAME',
        '{\"env\":{\"ANTHROPIC_AUTH_TOKEN\":\"$API_KEY\",\"ANTHROPIC_BASE_URL\":\"https://aigw.netease.com\",\"ANTHROPIC_MODEL\":\"$MODEL_ID\",\"ANTHROPIC_DEFAULT_HAIKU_MODEL\":\"$MODEL_ID\",\"ANTHROPIC_DEFAULT_SONNET_MODEL\":\"$MODEL_ID\",\"ANTHROPIC_DEFAULT_OPUS_MODEL\":\"$MODEL_ID\",\"ANTHROPIC_REASONING_MODEL\":\"$MODEL_ID\",\"ANTHROPIC_VERSION\":\"2023-06-01\"},\"includeCoAuthoredBy\":false}',
        '{\"endpointAutoSelect\":true,\"apiFormat\":\"$API_FORMAT\"}',
        0,
        NULL
    );"
    echo "已创建 Provider: $PROVIDER_NAME"
fi

echo ""
echo "配置详情:"
echo "  ID:        $PROVIDER_ID"
echo "  名称:      $PROVIDER_NAME"
echo "  模型:      $MODEL_ID"
echo "  API 格式:  $API_FORMAT"
echo ""
echo "下一步:"
echo "  1. 在 CC Switch 中切换到该 Provider"
echo "  2. 或执行: sqlite3 $DB_PATH \"UPDATE providers SET is_current = 0 WHERE app_type = 'claude' AND is_current = 1; UPDATE providers SET is_current = 1 WHERE id = '$PROVIDER_ID';\""
echo "  3. 重启 CC Switch"
