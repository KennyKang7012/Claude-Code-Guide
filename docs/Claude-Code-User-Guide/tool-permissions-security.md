# 工具權限-安全管理

## 文章資訊
- 文章原始標題：Claude Code Best Practices
- 文章網址：https://www.anthropic.com/engineering/claude-code-best-practices

## 文章原始內容

預設情況下，Claude Code 會為任何可能修改您系統的操作請求權限：檔案寫入、許多 bash 指令、MCP 工具等。我們設計 Claude Code 採用這種故意保守的方法來優先考慮安全性。您可以自訂許可清單以允許您知道是安全的額外工具，或允許容易撤銷的潛在不安全工具（例如檔案編輯、git commit）。

有四種方式管理允許的工具：

- 在會話期間出現提示時選擇「始終允許」
- 啟動 Claude Code 後使用 /permissions 指令來新增或移除許可清單中的工具。例如，您可以新增 Edit 以始終允許檔案編輯，Bash(git commit:*) 以允許 git 提交，或 mcp__puppeteer__puppeteer_navigate 以允許使用 Puppeteer MCP 伺服器進行導航
- 手動編輯您的 .claude/settings.json 或 ~/.claude.json（我們建議將前者檢入原始碼控制以與您的團隊共享）
- 使用 --allowedTools CLI 標誌進行會話特定權限

### 安全 YOLO 模式

您可以使用 claude --dangerously-skip-permissions 來繞過所有權限檢查，讓 Claude 不受干擾地工作直到完成，而不是監督 Claude。這對於修復 lint 錯誤或生成樣板程式碼等工作流程效果很好。

讓 Claude 運行任意指令是有風險的，可能導致資料遺失、系統損壞，甚至資料外洩（例如透過提示注入攻擊）。為了最小化這些風險，在沒有網路存取的容器中使用 --dangerously-skip-permissions。您可以遵循這個參考實作，使用 Docker Dev Containers。

## 功能分析與使用建議

Claude Code 的權限管理系統是安全性與效率之間的精妙平衡，提供了靈活而強大的控制機制：

### 1. 權限系統架構

**安全優先原則**：
- **預設拒絕**：所有潛在危險操作需明確授權
- **最小權限**：僅授予完成任務所需的最小權限
- **可撤銷性**：權限可隨時修改或撤銷
- **透明度**：所有權限請求都會明確提示用戶

**權限分類體系**：
```
安全級別 1: 檔案讀取、基本查詢 - 自動允許
安全級別 2: 檔案編輯、Git 操作 - 需要授權但風險可控
安全級別 3: 系統指令、網路存取 - 需要明確授權
安全級別 4: 管理員操作、系統修改 - 高風險操作
```

### 2. 四種權限管理方式

**方式一：即時授權**
```bash
# Claude 請求權限時的響應
Claude: 我需要編輯 src/auth.py 檔案，是否允許？
用戶: [選擇 "Always allow" 或 "Allow once"]
```

**方式二：/permissions 指令管理**
```bash
# 檢視當前權限
> /permissions list

# 新增檔案編輯權限
> /permissions add Edit

# 新增特定 Git 操作權限  
> /permissions add "Bash(git commit:*)"

# 新增 MCP 工具權限
> /permissions add "mcp__puppeteer__puppeteer_navigate"

# 移除權限
> /permissions remove Edit
```

**方式三：配置檔案管理**
```json
// .claude/settings.json (專案層級，建議納入版本控制)
{
  "allowedTools": [
    "Edit",
    "Bash(git commit:*)",
    "Bash(git push:*)",
    "mcp__github__create_issue"
  ]
}

// ~/.claude.json (全域層級，個人設定)  
{
  "allowedTools": [
    "Edit",
    "Bash(npm run:*)",
    "Bash(docker compose:*)"
  ]
}
```

**方式四：CLI 標誌**
```bash
# 會話特定權限
claude --allowedTools="Edit,Bash(git commit:*)"

# 完全跳過權限檢查（危險模式）
claude --dangerously-skip-permissions
```

### 3. 安全 YOLO 模式深度解析

**適用場景**：
- **重複性任務**：修復 lint 錯誤、格式化程式碼
- **樣板程式碼生成**：創建標準結構和檔案
- **自動化工作流**：批量處理、資料轉換
- **信任環境**：隔離的開發容器

**風險評估**：
```
高風險：
- 資料外洩（git push 到錯誤儲存庫）
- 系統破壞（刪除重要檔案）
- 惡意代碼執行（提示注入攻擊）

中風險：
- 不當修改（覆蓋重要設定）
- 網路操作（未授權的 API 呼叫）
- 權限提升（修改系統設定）

低風險：
- 檔案編輯（可透過 Git 撤銷）
- 本地指令（影響範圍有限）
- 測試執行（隔離環境）
```

**安全容器化實踐**：
```dockerfile
# Dockerfile for secure Claude Code environment
FROM ubuntu:22.04

# 安裝必要工具但限制網路存取
RUN apt-get update && apt-get install -y \
    git nodejs npm python3 \
    --no-install-recommends

# 創建非 root 用戶
RUN useradd -m -s /bin/bash claude-user
USER claude-user

# 設定工作目錄
WORKDIR /workspace

# 限制網路存取（僅允許本地連接）
# 透過 docker run --network none 進一步限制
```

### 4. 進階權限策略

**專案特定配置**：
```json
// .claude/settings.json 範例
{
  "allowedTools": [
    "Edit",                          // 檔案編輯
    "Bash(npm run test:*)",         // 測試指令
    "Bash(git add:*)",              // Git 新增  
    "Bash(git commit:*)",           // Git 提交
    "mcp__github__create_pr",       // GitHub PR
    "mcp__slack__send_message"      // Slack 通知
  ],
  "blockedTools": [
    "Bash(rm:*)",                   // 禁止刪除操作
    "Bash(sudo:*)",                 // 禁止管理員權限
    "mcp__aws__*"                   // 禁止 AWS 操作
  ]
}
```

**團隊協作權限模板**：
```json
// 前端團隊配置
{
  "allowedTools": [
    "Edit",
    "Bash(npm:*)",
    "Bash(yarn:*)", 
    "Bash(git commit:*)",
    "mcp__figma__*"
  ]
}

// 後端團隊配置  
{
  "allowedTools": [
    "Edit",
    "Bash(docker:*)",
    "Bash(kubectl:*)",
    "Bash(git commit:*)",
    "mcp__database__query"
  ]
}

// DevOps 團隊配置
{
  "allowedTools": [
    "Edit",
    "Bash(*)",  // 更寬泛的權限
    "mcp__aws__*",
    "mcp__kubernetes__*"
  ]
}
```

### 5. 權限監控與稽核

**活動記錄**：
```bash
# 檢視權限使用歷史
> /permissions history

# 檢視當前會話的工具使用
> /permissions audit

# 匯出權限使用報告
> /permissions export --format json
```

**安全檢查清單**：
```
□ 定期審查 allowedTools 列表
□ 監控異常的權限請求
□ 檢查 YOLO 模式使用頻率
□ 驗證容器隔離設定
□ 更新權限配置文件
□ 培訓團隊成員安全意識
```

### 6. 常見安全場景處理

**場景一：新團隊成員加入**
```bash
# 提供基礎權限模板
cp .claude/settings.template.json .claude/settings.json

# 漸進式權限開放
# 第一週：僅檔案編輯和基本 Git
# 第二週：新增測試和建構權限  
# 第三週：新增部署相關權限
```

**場景二：生產環境操作**
```bash
# 嚴格模式：無自動權限
claude --no-auto-permissions

# 每個操作都需明確確認
# 建議使用配對程式設計模式
```

**場景三：CI/CD 整合**
```bash
# 無頭模式的安全配置
claude -p "修復 lint 錯誤" \
  --allowedTools="Edit,Bash(npm run lint:*)" \
  --no-network-access
```

### 7. 最佳實踐總結

**權限設計原則**：
1. **最小權限原則**：僅給予必要權限
2. **職責分離**：不同角色不同權限
3. **定期審查**：權限配置需定期檢視
4. **分層防護**：多重安全控制措施
5. **透明度**：所有權限操作可追蹤

**安全建議**：
- 在隔離環境中使用 YOLO 模式
- 定期更新和審查權限配置
- 監控和記錄所有權限使用
- 建立權限撤銷的應急程序
- 培訓團隊成員權限管理最佳實踐

Claude Code 的權限系統在保障安全的同時提供了高度的靈活性，通過合理配置可以實現安全與效率的最佳平衡。