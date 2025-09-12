# 環境設定-CLAUDE文件配置

## 文章資訊
- 文章原始標題：Claude Code Best Practices
- 文章網址：https://www.anthropic.com/engineering/claude-code-best-practices

## 文章原始內容

CLAUDE.md 是一個特殊檔案，Claude 在開始對話時會自動將其納入上下文。這使其成為記錄以下內容的理想場所：

- 常用的 bash 指令
- 核心檔案和實用功能
- 程式碼風格指南
- 測試指令
- 代碼庫禮儀（例如分支命名、合併 vs 變基等）
- 開發者環境設定（例如 pyenv use、哪些編譯器可用）
- 專案特有的任何異常行為或警告
- 您希望 Claude 記住的其他資訊

CLAUDE.md 檔案沒有必需的格式。我們建議保持簡潔且人類可讀。例如：

```markdown
# Bash commands
- npm run build: Build the project
- npm run typecheck: Run the typechecker

# Code style
- Use ES modules (import/export) syntax, not CommonJS (require)
- Destructure imports when possible (eg. import { foo } from 'bar')

# Workflow
- Be sure to typecheck when you're done making a series of code changes
- Prefer running single tests, and not the whole test suite, for performance
```

您可以將 CLAUDE.md 檔案放在幾個位置：

- 在您的代碼庫根目錄，或您運行 claude 的任何地方（最常見的用法）
- 運行 claude 目錄的任何父目錄
- 運行 claude 目錄的任何子目錄
- 您的家目錄（~/.claude/CLAUDE.md），適用於所有 claude 會話

## 功能分析與使用建議

CLAUDE.md 檔案是 Claude Code 工作流程的核心配置工具，具有以下關鍵優勢：

### 1. 自動上下文載入
- **自動化**：Claude 啟動時自動載入，無需手動指定
- **持久性**：內容在整個會話期間保持可用
- **層級化**：支援多層級配置，從全域到專案特定

### 2. 團隊協作優化
- **版本控制整合**：檢入 git 以與團隊共享
- **本地化選項**：使用 `.local.md` 後綴進行個人化配置
- **一致性保證**：確保團隊成員使用相同的開發標準

### 3. 提示優化策略
- **迭代改進**：像其他經常使用的提示一樣進行優化
- **強調關鍵字**：使用「IMPORTANT」或「YOU MUST」增強遵循度
- **提示改進工具**：可透過 Anthropic 的提示改進器進一步優化

### 4. 實用建議
- **保持簡潔**：避免過度冗長的內容
- **定期更新**：使用 `#` 鍵即時新增內容到 CLAUDE.md
- **結構化組織**：按功能分類（指令、風格、工作流程等）
- **團隊共享**：將 CLAUDE.md 更改包含在提交中，讓團隊成員受益