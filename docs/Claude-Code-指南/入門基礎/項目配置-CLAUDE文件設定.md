# 項目配置-CLAUDE文件設定

## 文章資訊
- 文章原始標題：Anthropic 推出 Claude Code 智能编程最佳实践指南（中文版）
- 文章網址：https://ai-bot.cn/ai-tutorials-claude-code-best-practices-for-agentic-coding/

## 文章原始內容

1. 自定義設置
- 創建 CLAUDE.md 文件，記錄:
  - 常用 bash 命令
  - 核心文件和功能
  - 代碼風格指南
  - 測試說明
  - 項目規範

Initial Setup
- Create a `CLAUDE.md` file to provide project-specific instructions
- Customize permissions and tool integrations
- Place the file in project root, parent directory, or home directory

## 功能分析與使用建議

### CLAUDE.md 文件的重要性
CLAUDE.md 文件是 Claude Code 項目配置的核心，它允許你為每個專案提供客製化的指導和設定。

### 文件放置位置
Claude Code 會按照以下優先順序尋找 CLAUDE.md 文件：
1. **專案根目錄** - 最高優先級，專案特定設定
2. **父級目錄** - 用於多專案的共通設定
3. **家目錄** - 全域預設設定

### 建議包含的內容

**1. 常用 Bash 命令**
```markdown
## 常用命令
- 啟動開發伺服器：`npm run dev`
- 執行測試：`npm test`
- 建置專案：`npm run build`
- 程式碼檢查：`npm run lint`
```

**2. 核心文件和功能說明**
```markdown
## 專案結構
- `/src` - 主要原始碼
- `/components` - React 組件
- `/utils` - 工具函數
- `/tests` - 測試文件
```

**3. 代碼風格指南**
```markdown
## 編碼規範
- 使用 2 空格縮排
- 使用 camelCase 命名變數
- 使用 PascalCase 命名組件
- 每個文件末尾保留一行空行
```

**4. 測試說明**
```markdown
## 測試指導
- 所有新功能都需要編寫單元測試
- 使用 Jest 作為測試框架
- 測試覆蓋率需達到 80% 以上
```

**5. 專案規範**
```markdown
## 開發規範
- 所有 commit 必須遵循 conventional commits 格式
- PR 需要通過 CI/CD 檢查
- 不允許直接推送到 main 分支
```

### 實用建議
1. **持續更新**：隨著專案發展，定期更新 CLAUDE.md 內容
2. **團隊協作**：確保團隊成員都了解並遵循 CLAUDE.md 中的設定
3. **模板化**：為不同類型的專案建立 CLAUDE.md 模板
4. **版本控制**：將 CLAUDE.md 納入版本控制，確保團隊同步