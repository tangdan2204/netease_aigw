#!/usr/bin/env pwsh
# ============================================
# NetEase AIGW OpenCode 技能安装脚本
# 适用于 Windows PowerShell
# ============================================

$ErrorActionPreference = "Stop"

# 颜色输出函数
function Write-Info { Write-Host "[INFO] $args" -ForegroundColor Blue }
function Write-Success { Write-Host "[OK] $args" -ForegroundColor Green }
function Write-Warning { Write-Host "[WARN] $args" -ForegroundColor Yellow }
function Write-Error { Write-Host "[ERROR] $args" -ForegroundColor Red }

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║       NetEase AIGW OpenCode 技能安装 v1.0            ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# 获取脚本目录
$ScriptDir = Split-Path -Parent -Path $MyInvocation.MyCommand.Path
$SkillName = "netease-aigw"

Write-Info "安装目录: $ScriptDir"

# 检查Python
Write-Info "检查 Python 环境..."
try {
    $pythonVersion = python --version 2>&1
    Write-Success "Python 已安装: $pythonVersion"
} catch {
    Write-Error "未找到 Python，请先安装 Python 3.8+"
    Write-Host "下载地址: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "按 Enter 退出"
    exit 1
}

# 检查requests库
Write-Info "检查 requests 库..."
try {
    python -c "import requests" 2>&1 | Out-Null
    Write-Success "requests 已安装"
} catch {
    Write-Warning "未找到 requests 库，正在安装..."
    try {
        pip install requests --quiet
        Write-Success "requests 安装成功"
    } catch {
        Write-Error "安装 requests 失败，请手动执行: pip install requests"
    }
}

# 获取用户目录
$UserProfile = [Environment]::GetEnvironmentVariable("USERPROFILE")
$AgentsDir = "$UserProfile\.agents"
$SkillsDir = "$AgentsDir\skills"
$SkillTargetDir = "$SkillsDir\$SkillName"

# 检查OpenCode技能目录
Write-Info "检查 OpenCode 技能目录..."
if (-not (Test-Path $AgentsDir)) {
    Write-Warning "未找到 .agents 目录，将创建"
    New-Item -ItemType Directory -Path $AgentsDir -Force | Out-Null
}

if (-not (Test-Path $SkillsDir)) {
    Write-Warning "未找到 skills 目录，将创建"
    New-Item -ItemType Directory -Path $SkillsDir -Force | Out-Null
}
Write-Success "技能目录已就绪"

# 复制技能文件
Write-Info "复制技能文件..."
try {
    Copy-Item -Path "$ScriptDir\skills\*" -Destination $SkillTargetDir -Recurse -Force
    Write-Success "技能文件已复制到: $SkillTargetDir"
} catch {
    Write-Error "复制文件失败，请检查权限: $_"
    Read-Host "按 Enter 退出"
    exit 1
}

# 更新skill-lock.json
Write-Info "更新 skill-lock.json..."
$LockFile = "$AgentsDir\.skill-lock.json"

if (-not (Test-Path $LockFile)) {
    Write-Warning "未找到 skill-lock.json，将创建"
    @{
        version = 3
        skills = @{}
        dismissed = @{}
    } | ConvertTo-Json -Depth 10 | Set-Content -Path $LockFile -Encoding UTF8
}

# 读取并更新JSON
try {
    $lockContent = Get-Content -Path $LockFile -Raw -Encoding UTF8
    $lockJson = $lockContent | ConvertFrom-Json

    if (-not $lockJson.skills.PSObject.Properties.Name -contains $SkillName) {
        $lockJson.skills | Add-Member -MemberType NoteProperty -Name $SkillName -Value @{
            source = "local"
            sourceType = "local"
            sourceUrl = "file:///local/$SkillName"
            skillFolderHash = ""
            installedAt = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss.fff") + "Z"
            updatedAt = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss.fff") + "Z"
        }
        $lockJson | ConvertTo-Json -Depth 10 | Set-Content -Path $LockFile -Encoding UTF8
        Write-Success "skill-lock.json 已更新"
    } else {
        Write-Info "技能已存在，跳过更新"
    }
} catch {
    Write-Warning "更新 skill-lock.json 失败: $_"
}

# 创建符号链接（可选）
Write-Info "创建符号链接（可选）..."
$AgentSkillsDir = "$UserProfile\.agent\skills"

if (Test-Path $AgentSkillsDir) {
    $LinkPath = "$AgentSkillsDir\$SkillName"
    if (-not (Test-Path $LinkPath)) {
        try {
            $shell = New-Object -ComObject WScript.Shell
            $link = $shell.CreateShortcut($LinkPath + ".lnk")
            $link.TargetPath = $SkillTargetDir
            $link.Save()
            Write-Success "符号链接已创建"
        } catch {
            Write-Warning "创建符号链接失败，可手动创建"
        }
    } else {
        Write-Info "符号链接已存在"
    }
} else {
    Write-Info ".agent\skills 目录不存在，跳过符号链接创建"
}

# 测试连接
Write-Info "正在测试 API 连接..."
Write-Host ""

try {
    $testResult = python "$SkillTargetDir\test_connection.py" 2>&1
    $testResult | ForEach-Object { Write-Host $_ }
} catch {
    Write-Warning "测试脚本执行失败: $_"
}

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                    安装完成！                          ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "[下一步]" -ForegroundColor Green
Write-Host "1. 重启 OpenCode"
Write-Host "2. 在 OpenCode 中使用以下代码测试:"
Write-Host ""
Write-Host '   from scripts.netease_aigw_client import create_default_client' -ForegroundColor Gray
Write-Host "   client = create_default_client()" -ForegroundColor Gray
Write-Host "   print(client.chat(model='claude-opus-4-6', messages=[{'role': 'user', 'content': 'Hello'}], max_tokens=50)['choices'][0]['message']['content'])" -ForegroundColor Gray
Write-Host ""
Write-Host "[注意]" -ForegroundColor Yellow
Write-Host "- 如果 API 连接超时，可能需要 VPN 或检查网络"
Write-Host "- 详细使用说明请查看 README.md"
Write-Host ""

Read-Host "按 Enter 退出"
