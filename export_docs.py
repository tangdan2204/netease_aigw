#!/usr/bin/env python3
"""
网易 AIGW 完整文档导出工具

功能:
- 自动发现网站所有文档页面
- 递归抓取所有目录和子页面
- 保存为统一 Markdown 文件

使用方法:
1. 确保已连接 VPN/内网
2. 运行: python3 export_docs.py
3. 文档将保存到 docs_export.md
"""

import requests
from bs4 import BeautifulSoup
import re
import os
import sys
from urllib.parse import urljoin, urlparse
from collections import deque


def get_all_page_urls(base_url):
    """发现网站所有文档页面"""
    print("🔍 正在发现网站结构...")
    
    discovered_urls = set()
    queue = deque([base_url])
    visited = set()
    
    # 常见文档目录结构
    doc_patterns = [
        "/25_AIGW功能指南/开放计费/",
        "/25_AIGW功能指南/快速接入/",
        "/25_AIGW功能指南/调用指南/",
        "/25_AIGW功能指南/认证说明/",
        "/25_AIGW功能指南/常见问题/",
    ]
    
    # 先添加已知目录
    for pattern in doc_patterns:
        url = base_url + pattern
        if url not in visited:
            queue.append(url)
    
    while queue:
        current_url = queue.popleft()
        
        if current_url in visited:
            continue
        visited.add(current_url)
        
        try:
            response = requests.get(current_url, timeout=15)
            response.encoding = "utf-8"
            
            if response.status_code != 200:
                continue
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # 查找所有链接
            for link in soup.find_all("a", href=True):
                href = link["href"]
                
                if not href:
                    continue
                
                # 转换为绝对 URL
                if href.startswith("/"):
                    full_url = urljoin(base_url, href)
                elif href.startswith(base_url):
                    full_url = href
                else:
                    continue
                
                # 只保留同域名下的 HTML 页面
                parsed = urlparse(full_url)
                if parsed.netloc != urlparse(base_url).netloc:
                    continue
                    
                if full_url.endswith(".html") or "/25_AIGW" in full_url:
                    if full_url not in discovered_urls:
                        discovered_urls.add(full_url)
                        if full_url not in visited:
                            queue.append(full_url)
            
            # 限制抓取数量
            if len(discovered_urls) > 100:
                print(f"⚠️  已发现 {len(discovered_urls)} 个页面，停止搜索")
                break
                
        except Exception:
            continue
    
    print(f"✅ 发现 {len(discovered_urls)} 个文档页面")
    return list(discovered_urls)


def fetch_page_content(url, base_url):
    """获取单个页面的标题和内容"""
    try:
        response = requests.get(url, timeout=30)
        response.encoding = "utf-8"
        
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 提取标题
        title = soup.find("title")
        title_text = title.get_text().strip() if title else "无标题"
        title_text = re.sub(r"\s*[-_|].*$", "", title_text).strip()
        
        # 提取主要内容
        content = (
            soup.find("div", class_="content")
            or soup.find("main")
            or soup.find("article")
            or soup.find("div", class_="docs")
            or soup.find("body")
        )
        
        if content:
            text = content.get_text(separator="\n", strip=True)
        else:
            text = soup.get_text(separator="\n", strip=True)
        
        # 清理文本
        lines = text.split("\n")
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if any(skip in line for skip in ["导航菜单", "返回顶部", "Copyright"]):
                continue
            cleaned_lines.append(line)
        
        text = "\n".join(cleaned_lines)
        text = re.sub(r"\n{3,}", "\n\n", text)
        
        return {
            "title": title_text,
            "url": url,
            "content": text,
            "char_count": len(text)
        }
        
    except Exception:
        return None


def fetch_all_docs():
    """获取所有文档"""
    base_url = "https://aigw.doc.nie.netease.com"
    
    urls = get_all_page_urls(base_url)
    
    if not urls:
        print("❌ 未能发现任何页面")
        urls = [base_url + "/25_AIGW功能指南/开放计费/1_使用文档.html"]
    
    all_content = []
    success_count = 0
    
    print(f"\n📥 开始抓取 {len(urls)} 个页面...\n")
    
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] {url}")
        
        result = fetch_page_content(url, base_url)
        
        if result:
            rel_path = url.replace(base_url, "").replace(".html", "").strip("/")
            section_title = rel_path.split("/")[-1] if rel_path else result["title"]
            
            content_block = f"""
================================================================================
📄 {section_title}
================================================================================
URL: {url}
字符数: {result["char_count"]}

{result["content"]}
"""
            all_content.append(content_block)
            success_count += 1
            print(f"  ✅ {result['char_count']} 字符")
        else:
            print(f"  ❌ 获取失败")
        
        import time
        time.sleep(0.3)
    
    print(f"\n✅ 成功获取 {success_count}/{len(urls)} 个页面")
    return "\n".join(all_content)


def save_to_markdown(content, filename="docs_export.md"):
    """保存为 Markdown 文件"""
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    return filepath


def main():
    print("=" * 70)
    print("  网易 AIGW 完整文档导出工具")
    print("=" * 70)
    print()
    print("⚠️  确保已连接 VPN/内网")
    print("📡 目标: aigw.doc.nie.netease.com")
    print()
    
    # 检查依赖
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        print("📦 安装依赖...")
        os.system("pip3 install requests beautifulsoup4")
    
    print()
    content = fetch_all_docs()
    
    if content:
        filepath = save_to_markdown(content)
        print(f"\n{'='*70}")
        print(f"✅ 完成!")
        print(f"📄 导出 {len(content):,} 字符")
        print(f"💾 保存到: {filepath}")
        print(f"{'='*70}")
        print()
        print("📖 使用方式:")
        print(f"   cat {filepath}")
        print(f"   或发送文件内容给 AI 分析")
        print()
    else:
        print("❌ 未能获取任何文档内容")
        sys.exit(1)


if __name__ == "__main__":
    main()
