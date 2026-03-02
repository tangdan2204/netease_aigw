@echo off
chcp 65001 >nul
REM ============================================
REM NetEase AIGW OpenCode 技能安装脚本
REM 适用于 Windows
REM ============================================

setlocal

REM 颜色定义
set RED=[0;31m
set GREEN=[0;32m
set YELLOW=[1;33m
set BLUE=[0;34m
set NC=[0m

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║       NetEase AIGW OpenCode 技能安装 v1.0              ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM 获取当前目录
set "SCRIPT_DIR=%~dp0"
set "SKILL_NAME=netease-aigw"

echo [INFO] 安装目录: %SCRIPT_DIR%
echo.

REM 检查Python
echo [INFO] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] 未找到 Python，请先安装 Python 3.8+
    echo         下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python 已安装

REM 检查requests库
echo [INFO] 检查 requests 库...
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo [WARN] 未找到 requests 库，正在安装...
    pip install requests
    if errorlevel 1 (
        echo [ERROR] 安装 requests 失败，请手动执行: pip install requests
    ) else (
        echo [OK] requests 安装成功
    )
) else (
    echo [OK] requests 已安装
)

REM 获取用户目录
for /f "tokens=*" %%i in ('powershell -Command "[Environment]::GetEnvironmentVariable('USERPROFILE')"') do set "USERPROFILE_DIR=%%i"
set "AGENTS_DIR=%USERPROFILE_DIR%\.agents"
set "SKILLS_DIR=%AGENTS_DIR%\skills"
set "SKILL_TARGET_DIR=%SKILLS_DIR%\%SKILL_NAME%"

REM 检查OpenCode技能目录
echo.
echo [INFO] 检查 OpenCode 技能目录...
if not exist "%AGENTS_DIR%" (
    echo [WARN] 未找到 .agents 目录，将创建
    mkdir "%AGENTS_DIR%"
)

if not exist "%SKILLS_DIR%" (
    echo [WARN] 未找到 skills 目录，将创建
    mkdir "%SKILLS_DIR%"
)
echo [OK] 技能目录已就绪

REM 复制技能文件
echo.
echo [INFO] 复制技能文件...
xcopy "%SCRIPT_DIR%skills\*" "%SKILL_TARGET_DIR%\" /E /I /Q
if errorlevel 1 (
    echo [ERROR] 复制文件失败，请检查权限
    pause
    exit /b 1
)
echo [OK] 技能文件已复制到: %SKILL_TARGET_DIR%

REM 更新 skill-lock.json
echo.
echo [INFO] 更新 skill-lock.json...
set "LOCK_FILE=%AGENTS_DIR%\.skill-lock.json"

if not exist "%LOCK_FILE%" (
    echo [WARN] 未找到 skill-lock.json，将创建
    echo { "version": 3, "skills": {}, "dismissed": {} } > "%LOCK_FILE%"
)

REM 使用PowerShell更新JSON
powershell -Command ^
    $lockFile = '%LOCK_FILE%'; ^
    $skillName = '%SKILL_NAME%'; ^
    $content = Get-Content $lockFile -Raw -Encoding UTF8; ^
    $json = $content | ConvertFrom-Json; ^
    if (-not $json.skills.($skillName)) { ^
        $json.skills | Add-Member -NotePropertyName $skillName -NotePropertyValue @{ ^
            source = 'local'; ^
            sourceType = 'local'; ^
            sourceUrl = 'file:///local/' + $skillName; ^
            skillFolderHash = ''; ^
            installedAt = (Get-Date -Format 'yyyy-MM-ddTHH:mm:ss.fff') + 'Z'; ^
            updatedAt = (Get-Date -Format 'yyyy-MM-ddTHH:mm:ss.fff') + 'Z' ^
        }; ^
        $json | ConvertTo-Json -Depth 10 | Set-Content $lockFile -Encoding UTF8; ^
        Write-Host '[OK] skill-lock.json 已更新'; ^
    } else { ^
        Write-Host '[INFO] 技能已存在，跳过更新'; ^
    }

REM 创建符号链接（可选）
echo.
echo [INFO] 创建符号链接（可选）...
set "AGENT_SKILLS_DIR=%USERPROFILE_DIR%\.agent\skills"

if exist "%AGENT_SKILLS_DIR%" (
    if not exist "%AGENT_SKILLS_DIR%\%SKILL_NAME%" (
        mklink /D "%AGENT_SKILLS_DIR%\%SKILL_NAME%" "%SKILL_TARGET_DIR%" >nul 2>&1
        if errorlevel 1 (
            echo [WARN] 创建符号链接失败，可手动创建
        ) else (
            echo [OK] 符号链接已创建
        )
    ) else (
        echo [INFO] 符号链接已存在
    )
) else (
    echo [INFO] .agent\skills 目录不存在，跳过符号链接创建
)

REM 测试连接
echo.
echo [INFO] 正在测试 API 连接...
python "%SKILL_TARGET_DIR%\test_connection.py" > "%TEMP%\netease_test.log" 2>&1

if exist "%TEMP%\netease_test.log" (
    type "%TEMP%\netease_test.log"
)

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║                    安装完成！                          ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo [下一步]
echo 1. 重启 OpenCode
echo 2. 在 OpenCode 中使用以下代码测试:
echo.
echo    from scripts.netease_aigw_client import create_default_client
echo    client = create_default_client()
echo    print(client.chat(model="claude-opus-4-6", messages=[{"role": "user", "content": "Hello"}], max_tokens=50)["choices"][0]["message"]["content"])
echo.
echo [注意]
echo - 如果 API 连接超时，可能需要 VPN 或检查网络
echo - 详细使用说明请查看 README.md
echo.

pause
endlocal
