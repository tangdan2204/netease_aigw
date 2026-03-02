#!/usr/bin/env python3
# ========================================
# 数据库初始化脚本
# ========================================
"""
数据库表创建脚本

用于初始化数据库表结构
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.config import load_config
from app.database import init_db, get_engine, Base
from app.models.user import User


def main():
    """主函数"""
    print("🚀 初始化数据库...")

    try:
        # 加载配置
        config = load_config()
        print(f"📦 数据库: {config.database.name}@{config.database.host}")

        # 初始化表
        init_db()
        print("✅ 数据库表创建成功!")

        # 显示创建的表
        print("\n📋 创建的表:")
        for table in Base.metadata.sorted_tables:
            print(f"   - {table.name}")

        return 0

    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
