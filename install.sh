#!/bin/bash
#
# 网易 AIGW OpenCode 技能安装脚本
# 
# 使用方法:
#   chmod +x install.sh
#   ./install.sh
#
# 或手动安装:
#   cd /Users/tangdan/Desktop/netease_aigw
#   npx skills add ./skills
#

set -e

echo "=========================================="
echo "  网易 AIGW OpenCode 技能安装"
echo "=========================================="
echo ""

# 检查 npx 是否可用
if ! command -v npx &> /dev/null; then
    echo "❌ 错误: npx 未安装，请先安装 Node.js"
    exit 1
fi

# 检查 skills 目录是否存在
if [ ! -d "skills" ]; then
    echo "❌ 错误: skills 目录不存在"
    exit 1
fi

echo "📦 安装 OpenCode 技能..."
echo ""

# 尝试安装技能
if npx skills add ./skills 2>&1; then
    echo ""
    echo "✅ 安装成功！"
else
    echo ""
    echo "⚠️  安装遇到问题，但这可能是正常的"
    echo "   在 OpenCode 中，你可能需要手动导入技能"
    echo ""
    echo "📁 技能位置: $(pwd)/skills"
    echo ""
fi

echo ""
echo "=========================================="
echo "  配置完成！"
echo "=========================================="
echo ""
echo "📝 下一步:"
echo "   1. 配置认证信息（环境变量或配置文件）"
echo "   2. 运行测试: python skills/test_connection.py"
echo "   3. 查看文档: cat README.md"
echo ""
echo "💡 认证配置:"
echo "   export NETEASE_APP_ID='your_app_id'"
echo "   export NETEASE_APP_KEY='your_app_key'"
echo ""
