# 网易 AIGW 开放计费完整指南

## 目录

- [概述](#概述)
- [使用流程](#使用流程)
- [认证配置](#认证配置)
- [接口说明](#接口说明)
- [字段格式规范](#字段格式规范)
- [错误码处理](#错误码处理)
- [常见问题](#常见问题)
- [完整示例](#完整示例)

---

## 概述

开放计费是 AIGW 提供的计费能力，允许业务线实现自定义的计费模式，适用于需要：
- 按用户维度进行费用分摊
- 自定义计费策略
- 精细化的用量统计

### 核心概念

| 概念 | 说明 |
|------|------|
| **虚拟模型代号** | 表示业务线的虚拟模型，如 `__aigw_virtual_open_bill_dm` |
| **token_type** | 计费类型，用于区分不同的计费场景 |
| **billing_trace_id** | 任务追踪 ID，用于关联多次计费记录 |
| **预扣费** | 预先冻结积分，完成后确认或回滚 |

---

## 使用流程

### 步骤 1：开通权限

联系 AIGW 管理员，按业务线开通权限，获取虚拟模型代号。

**示例虚拟模型代号：**
```
__aigw_virtual_open_bill_dm
```

### 步骤 2：创建 token_type

业务线根据场景创建 token_type，并设置对应的价格。

**示例 token_type：**
```
_3D_gen_image      # 3D 图片生成
_3D_render         # 3D 渲染
_text-to-speech    # 语音合成
```

### 步骤 3：选择计费策略

根据场景选取合适的上报策略：

| 场景 | 推荐策略 | 说明 |
|------|----------|------|
| 语言类对话 | 直接上报 | 价格低、响应快 |
| 生图/生视频 | 预扣费 | 价格高、执行时间长 |
| 批量任务 | 混合策略 | 部分预扣、部分上报 |

---

## 认证配置

所有开放计费接口需要在请求头中携带访问令牌：

```bash
X-Access-Token: <your_access_token>
```

**获取方式：**
1. 访问 [Auth 控制台](https://console-auth.nie.netease.com/mymessage/mymessage)
2. 获取 v2 Token（七天有效期）

**示例请求头：**
```http
X-Access-Token: your_auth_token_here
Content-Type: application/json
```

---

## 接口说明

### 基础路径

```
/aigw/v1/open-bill
```

### 1. 查询配置

查询指定 model 下的 token_type 和价格配置。

**请求：**
```http
GET /aigw/v1/open-bill?model=__aigw_virtual_open_bill_dm
```

**查询参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| model | string | 是 | 虚拟模型代号 |
| token_types | string | 否 | 过滤指定的 token_type，多个用逗号分隔 |

**响应示例：**
```json
{
  "model": "__aigw_virtual_open_bill_dm",
  "token_type_configs": [
    {
      "token_type": "_3D_gen_image",
      "unit_price": "0.50",
      "billing_mode": "pre_deduct",
      "enabled": true
    }
  ]
}
```

**响应字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| model | string | 虚拟模型代号 |
| token_type_configs | array | token_type 配置列表 |
| token_type_configs.token_type | string | 计费类型 |
| token_type_configs.unit_price | decimal | 单价（千 tokens） |
| token_type_configs.billing_mode | string | 计费模式：pre_deduct/real_time |
| token_type_configs.enabled | boolean | 是否启用 |

---

### 2. 上报计费数据

上报单条计费数据。

**请求：**
```http
POST /aigw/v1/open-bill/report
Content-Type: application/json

{
  "billing_trace_id": "task_123456789012",
  "app_code": "your_app_code",
  "model": "__aigw_virtual_open_bill_dm",
  "token_type": "_3D_gen_image",
  "token_amount": 1000,
  "billing_stage": 1
}
```

**请求字段说明：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| billing_trace_id | string | 是 | 任务追踪 ID |
| app_code | string | 是 | 应用代码 |
| model | string | 是 | 虚拟模型代号 |
| token_type | string | 是 | 计费类型 |
| token_amount | int | 是 | token 数量 |
| billing_stage | int | 是 | 价格版本：0-预扣/1-实际 |

**响应示例：**
```json
{
  "success": true,
  "billing_record_id": "bill_abc123",
  "amount": "0.50"
}
```

---

### 3. 批量上报计费数据

批量上报多条计费数据。

**请求：**
```http
POST /aigw/v1/open-bill/batch_report
Content-Type: application/json

{
  "records": [
    {
      "billing_trace_id": "task_123456789012",
      "app_code": "your_app_code",
      "model": "__aigw_virtual_open_bill_dm",
      "token_type": "_3D_gen_image",
      "token_amount": 1000,
      "billing_stage": 1
    }
  ]
}
```

**批量限制：**
- 单次最多 100 条记录
- 总 token_amount 不超过 1,000,000

**响应示例：**
```json
{
  "success_count": 2,
  "fail_count": 0,
  "results": [
    {
      "billing_record_id": "bill_001",
      "success": true,
      "amount": "0.50"
    }
  ]
}
```

---

### 4. 预扣费确认

确认预扣的积分，生成正式计费记录。

**请求：**
```http
POST /aigw/v1/open-bill/commit
Content-Type: application/json

{
  "billing_trace_id": "task_123456789012",
  "app_code": "your_app_code",
  "model": "__aigw_virtual_open_bill_dm",
  "token_type": "_3D_render",
  "token_amount": 2000,
  "billing_stage": 0
}
```

**说明：**
- 用于确认预扣的积分
- billing_stage 从 0 变为 1

**响应示例：**
```json
{
  "success": true,
  "billing_record_id": "bill_commit_001",
  "amount": "1.00"
}
```

---

### 5. 预扣费回滚

回滚预扣的积分，释放冻结的额度。

**请求：**
```http
POST /aigw/v1/open-bill/rollback
Content-Type: application/json

{
  "billing_trace_id": "task_123456789012",
  "app_code": "your_app_code",
  "model": "__aigw_virtual_open_bill_dm",
  "token_type": "_3D_render",
  "token_amount": 2000
}
```

**说明：**
- 用于回滚预扣的积分
- 释放冻结的额度

**响应示例：**
```json
{
  "success": true,
  "released_amount": "1.00"
}
```

---

### 6. 查询计费记录

查询指定 app_code 或 billing_trace_id 的计费记录。

**请求：**
```http
GET /aigw/v1/open-bill/records?app_code=your_app_code&billing_trace_id=task_123456789012
```

**查询参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| app_code | string | 否 | 应用代码 |
| billing_trace_id | string | 否 | 任务追踪 ID |
| start_time | string | 否 | 开始时间（ISO 8601） |
| end_time | string | 否 | 结束时间（ISO 8601） |
| page | int | 否 | 页码，默认 1 |
| limit | int | 否 | 每页数量，默认 20 |

**响应示例：**
```json
{
  "records": [
    {
      "billing_record_id": "bill_001",
      "billing_trace_id": "task_123456789012",
      "app_code": "your_app_code",
      "model": "__aigw_virtual_open_bill_dm",
      "token_type": "_3D_gen_image",
      "token_amount": 1000,
      "billing_stage": 1,
      "amount": "0.50",
      "unit_price": "0.50",
      "created_at": "2026-02-09T12:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 20
}
```

---

## 字段格式规范

### token_type 格式要求

| 规则 | 说明 |
|------|------|
| 前缀 | 必须以下划线 `_` 开头 |
| 字符集 | 只允许英文字母（a-z, A-Z）、数字（0-9）、下划线（_）、连字符（-） |
| 长度 | 6-128 个字符（包含开头的下划线） |
| 正则表达式 | `^_[a-zA-Z0-9_-]{5,127}$` |

**正确示例：**
```
_3D_gen_image      ✅
_text-to-speech    ✅
_order-2024-abc    ✅
```

**错误示例：**
```
3D_gen_image       ❌ 缺少下划线前缀
_abc              ❌ 长度不足 6 个字符
_order@123        ❌ 包含非法字符 @
```

---

### billing_trace_id 格式要求

| 规则 | 说明 |
|------|------|
| 字符集 | 只允许英文字母（a-z, A-Z）、数字（0-9）、下划线（_）、连字符（-） |
| 长度 | 16-64 个字符 |
| 正则表达式 | `^[a-zA-Z0-9_-]{16,64}$` |

**正确示例：**
```
task_1234567890123456    ✅
order-2024-abc-xyz      ✅
```

**错误示例：**
```
task_1234567890         ❌ 长度不足 16 个字符
task@1234567890123456   ❌ 包含非法字符 @
```

---

## 错误码处理

| HTTP 状态码 | 说明 | 处理建议 |
|-------------|------|----------|
| 400 | 请求参数错误 | 检查 token_type 是否启用、价格是否配置 |
| 401 | 认证失败 | 检查 X-Access-Token 是否有效 |
| 402 | 积分不足 | 提示用户充值或联系管理员 |
| 403 | 无权限操作 | 检查是否有目标 App 的操作权限 |
| 404 | 资源不存在 | 检查 report_id、billing_trace_id 是否有效 |

---

## 常见问题

### Q: 用户(app_code)没有积分会限制上报吗？

**A: 不会。** 这个操作应该由用户判断，在每次任务发起时判断用户积分是否足够。因为如果限制的话可能会导致任务跑完上报计费数据失败。

---

### Q: 预扣费超时未处理会怎样？

**A:** 预扣积分会在 24 小时后自动释放，不会产生实际计费。但建议及时调用 commit 或 rollback 接口。

---

### Q: 可以对同一个 report_id 多次 commit 或 rollback 吗？

**A: 不可以。** 第一次操作后记录会被删除，后续操作会返回成功但不产生效果。

---

### Q: billing_trace_id 有什么用？

**A:** 用于关联多次计费记录。例如一个任务分多个阶段计费，可以使用相同的 billing_trace_id，后续可以通过查询接口获取该任务的所有计费明细和总花费。

---

## 完整示例

### Python 示例

```python
import requests


class AIGWOpenBillClient:
    """AIGW 开放计费客户端"""
    
    def __init__(self, base_url, access_token):
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "X-Access-Token": access_token,
            "Content-Type": "application/json"
        }
    
    def query_config(self, model, token_types=None):
        """查询配置"""
        url = f"{self.base_url}/aigw/v1/open-bill"
        params = {"model": model}
        if token_types:
            params["token_types"] = ",".join(token_types)
        
        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def report(self, billing_trace_id, app_code, model, 
               token_type, token_amount, billing_stage):
        """上报计费数据"""
        url = f"{self.base_url}/aigw/v1/open-bill/report"
        data = {
            "billing_trace_id": billing_trace_id,
            "app_code": app_code,
            "model": model,
            "token_type": token_type,
            "token_amount": token_amount,
            "billing_stage": billing_stage
        }
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def commit(self, billing_trace_id, app_code, model,
               token_type, token_amount):
        """预扣费确认"""
        url = f"{self.base_url}/aigw/v1/open-bill/commit"
        data = {
            "billing_trace_id": billing_trace_id,
            "app_code": app_code,
            "model": model,
            "token_type": token_type,
            "token_amount": token_amount
        }
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def rollback(self, billing_trace_id, app_code, model,
                 token_type, token_amount):
        """预扣费回滚"""
        url = f"{self.base_url}/aigw/v1/open-bill/rollback"
        data = {
            "billing_trace_id": billing_trace_id,
            "app_code": app_code,
            "model": model,
            "token_type": token_type,
            "token_amount": token_amount
        }
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def query_records(self, app_code=None, billing_trace_id=None,
                      start_time=None, end_time=None, page=1, limit=20):
        """查询计费记录"""
        url = f"{self.base_url}/aigw/v1/open-bill/records"
        params = {"page": page, "limit": limit}
        if app_code:
            params["app_code"] = app_code
        if billing_trace_id:
            params["billing_trace_id"] = billing_trace_id
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
        
        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()


# 使用示例
if __name__ == "__main__":
    client = AIGWOpenBillClient(
        base_url="https://aigw-int.netease.com",
        access_token="your_auth_token"
    )
    
    # 1. 查询配置
    config = client.query_config("__aigw_virtual_open_bill_dm")
    print("配置:", config)
    
    # 2. 预扣费
    result = client.report(
        billing_trace_id="task_123456789012",
        app_code="your_app_code",
        model="__aigw_virtual_open_bill_dm",
        token_type="_3D_gen_image",
        token_amount=1000,
        billing_stage=0  # 0-预扣
    )
    print("预扣费:", result)
    
    # 3. 任务完成后确认
    result = client.commit(
        billing_trace_id="task_123456789012",
        app_code="your_app_code",
        model="__aigw_virtual_open_bill_dm",
        token_type="_3D_gen_image",
        token_amount=1000
    )
    print("确认:", result)
    
    # 4. 查询记录
    records = client.query_records(billing_trace_id="task_123456789012")
    print("记录:", records)
```

---

### cURL 示例

```bash
# 查询配置
curl -X GET "https://aigw-int.netease.com/aigw/v1/open-bill?model=__aigw_virtual_open_bill_dm" \
  -H "X-Access-Token: your_auth_token"

# 上报计费
curl -X POST "https://aigw-int.netease.com/aigw/v1/open-bill/report" \
  -H "X-Access-Token: your_auth_token" \
  -H "Content-Type: application/json" \
  -d '{
    "billing_trace_id": "task_123456789012",
    "app_code": "your_app_code",
    "model": "__aigw_virtual_open_bill_dm",
    "token_type": "_3D_gen_image",
    "token_amount": 1000,
    "billing_stage": 1
  }'

# 预扣费确认
curl -X POST "https://aigw-int.netease.com/aigw/v1/open-bill/commit" \
  -H "X-Access-Token: your_auth_token" \
  -H "Content-Type: application/json" \
  -d '{
    "billing_trace_id": "task_123456789012",
    "app_code": "your_app_code",
    "model": "__aigw_virtual_open_bill_dm",
    "token_type": "_3D_render",
    "token_amount": 2000
  }'

# 预扣费回滚
curl -X POST "https://aigw-int.netease.com/aigw/v1/open-bill/rollback" \
  -H "X-Access-Token: your_auth_token" \
  -H "Content-Type: application/json" \
  -d '{
    "billing_trace_id": "task_123456789012",
    "app_code": "your_app_code",
    "model": "__aigw_virtual_open_bill_dm",
    "token_type": "_3D_render",
    "token_amount": 2000
  }'

# 查询记录
curl -X GET "https://aigw-int.netease.com/aigw/v1/open-bill/records?app_code=your_app_code" \
  -H "X-Access-Token: your_auth_token"
```

---

## 相关资源

- **ModelSpace**: https://modelspace.netease.com/
- **Auth 控制台**: https://console-auth.nie.netease.com/mymessage/mymessage
- **AIGW 文档**: https://aigw.doc.nie.netease.com/

---

*最后更新时间: 2026-02-12*
