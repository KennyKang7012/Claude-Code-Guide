# 多Claude工作流-並行處理

## 文章資訊
- 文章原始標題：Claude Code Best Practices
- 文章網址：https://www.anthropic.com/engineering/claude-code-best-practices

## 文章原始內容

除了獨立使用之外，一些最強大的應用涉及並行運行多個 Claude 實例：

### 讓一個 Claude 編寫程式碼；使用另一個 Claude 進行驗證

一個簡單但有效的方法是讓一個 Claude 編寫程式碼，而另一個審查或測試它。類似於與多個工程師合作，有時擁有單獨的上下文是有益的：

- 使用 Claude 編寫程式碼
- 運行 /clear 或在另一個終端中啟動第二個 Claude
- 讓第二個 Claude 審查第一個 Claude 的工作
- 啟動另一個 Claude（或再次 /clear）來讀取程式碼和審查反饋
- 讓這個 Claude 根據反饋編輯程式碼

您可以對測試做類似的事情：讓一個 Claude 編寫測試，然後讓另一個 Claude 編寫程式碼來使測試通過。您甚至可以讓您的 Claude 實例彼此溝通，給它們單獨的工作便箋本，並告訴它們寫入哪一個和讀取哪一個。

這種分離通常比讓單個 Claude 處理所有事情產生更好的結果。

### 擁有您代碼庫的多個檢出

許多 Anthropic 的工程師所做的，而不是等待 Claude 完成每一步：

- 在單獨的資料夾中創建 3-4 個 git 檢出
- 在單獨的終端標籤中打開每個資料夾
- 在每個資料夾中啟動 Claude 處理不同的任務
- 循環檢查進度並批准/拒絕權限請求

### 使用 git worktrees

這種方法對於多個獨立任務表現出色，提供了比多個檢出更輕量級的替代方案。Git worktrees 允許您從同一個代碼庫將多個分支檢出到單獨的目錄中。每個 worktree 都有自己的工作目錄與隔離的文件，同時共享相同的 Git 歷史和 reflog。

使用 git worktrees 可以讓您在專案的不同部分同時運行多個 Claude 會話，每個會話專注於自己的獨立任務。例如，您可能有一個 Claude 重構您的身份驗證系統，而另一個構建完全不相關的資料可視化組件。由於任務不重疊，每個 Claude 都可以全速工作，不需要等待其他人的變更或處理合併衝突：

- 創建 worktrees：`git worktree add ../project-feature-a feature-a`
- 在每個 worktree 中啟動 Claude：`cd ../project-feature-a && claude`
- 根據需要創建額外的 worktrees（在新的終端標籤中重複步驟 1-2）

一些提示：
- 使用一致的命名約定
- 每個 worktree 維護一個終端標籤
- 如果您在 Mac 上使用 iTerm2，設置通知當 Claude 需要注意時
- 對不同的 worktrees 使用單獨的 IDE 視窗
- 完成後清理：`git worktree remove ../project-feature-a`

## 功能分析與使用建議

多 Claude 工作流程代表了 AI 輔助開發的進階應用模式，通過並行處理和專業化分工大幅提升開發效率：

### 1. 程式碼寫作與驗證分離模式

**核心概念**：將創作和審查職責分離，模擬真實團隊協作

**實施流程**：
```bash
# Terminal 1 - 程式碼編寫 Claude
claude
> 請實施用戶認證模組，包含登入、登出和會話管理功能

# Terminal 2 - 程式碼審查 Claude  
claude
> 請審查剛才實施的認證模組，重點檢查安全性漏洞和程式碼品質

# Terminal 3 - 整合優化 Claude
claude
> 根據審查意見優化認證模組，並確保所有測試通過
```

**優勢分析**：
- **客觀性提升**：獨立上下文避免確認偏誤
- **專業化分工**：每個實例專注特定職責
- **品質保證**：多重驗證機制確保程式碼品質
- **學習效應**：觀察不同 Claude 實例的方法差異

### 2. 並行多任務處理

**場景適用**：
- **獨立功能開發**：前端 UI 與後端 API 並行開發
- **多模組重構**：同時優化不同系統組件
- **測試與實作分離**：一邊寫測試，一邊實作功能
- **文檔與程式碼同步**：程式碼開發的同時更新文檔

**最佳實踐**：
- **任務隔離性**：確保任務之間沒有直接依賴關係
- **定期同步**：通過共享文檔或檔案系統進行協調
- **進度追蹤**：使用檢查清單追蹤各實例的進展

### 3. Git Worktrees 進階應用

**技術優勢**：
- **輕量級**：比完整 clone 佔用更少磁碟空間
- **共享歷史**：所有 worktrees 共享 Git 物件和歷史
- **獨立工作區**：每個 worktree 有完全獨立的工作目錄
- **分支專用**：每個 worktree 可以工作在不同分支

**管理策略**：
```bash
# 創建專用功能分支的 worktree
git worktree add ../feature-auth auth-refactor
git worktree add ../feature-ui ui-improvements  
git worktree add ../feature-api api-optimization

# 設定 IDE 工作區
code ../feature-auth    # VS Code 視窗 1
code ../feature-ui      # VS Code 視窗 2  
code ../feature-api     # VS Code 視窗 3

# 清理完成的工作
git worktree remove ../feature-auth
git branch -d auth-refactor
```

### 4. 通訊協調機制

**文件型通訊**：
```bash
# 共享狀態文件
echo "auth-module: 進行中" > shared-status.md
echo "ui-components: 已完成" >> shared-status.md
echo "api-endpoints: 待開始" >> shared-status.md
```

**任務分配策略**：
- **Claude A**：專責後端邏輯和資料庫操作
- **Claude B**：專責前端介面和使用者體驗
- **Claude C**：專責測試撰寫和品質保證
- **Claude D**：專責文檔撰寫和部署配置

### 5. 實際應用建議

#### 團隊規模決策
- **小型任務**：2-3 個 Claude 實例
- **中型專案**：3-5 個實例，按模組分工
- **大型系統**：5+ 實例，按架構層次分工

#### 監控與管理
- **iTerm2 通知設定**：及時響應 Claude 請求
- **進度可視化**：使用 GitHub Projects 或類似工具追蹤
- **資源管理**：監控 API 使用量和成本

#### 風險管控
- **衝突預防**：確保工作範圍不重疊
- **定期同步**：避免長時間的分歧發展
- **回滾機制**：為每個 worktree 準備回滾策略

多 Claude 工作流程將 AI 輔助開發提升到全新水平，通過並行處理和專業分工實現了接近真實開發團隊的效率和品質。