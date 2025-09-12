# MCP整合-外部工具連接

## 文章資訊
- 文章原始標題：Claude Code Best Practices
- 文章網址：https://www.anthropic.com/engineering/claude-code-best-practices

## 文章原始內容

Claude Code 同時充當 MCP 伺服器和客戶端。作為客戶端，它可以通過三種方式連接到任意數量的 MCP 伺服器以存取其工具：

- 在專案配置中（在該目錄中運行 Claude Code 時可用）
- 在全域配置中（在所有專案中可用）
- 在檢入的 .mcp.json 檔案中（對在您的程式碼庫中工作的任何人都可用）。例如，您可以將 Puppeteer 和 Sentry 伺服器新增到您的 .mcp.json，這樣在您的代碼庫中工作的每個工程師都可以開箱即用地使用這些功能。

在使用 MCP 時，使用 --mcp-debug 標誌啟動 Claude 也會很有幫助，以幫助識別配置問題。

## 功能分析與使用建議

MCP（Model Context Protocol）是 Claude Code 與外部工具和系統整合的強大機制，提供了豐富的擴展性：

### 1. 多層級配置策略
- **專案層級**：透過專案配置文件，只在特定專案中啟用相關工具
- **全域層級**：在所有專案中共享常用工具配置
- **團隊共享**：使用 `.mcp.json` 確保團隊成員擁有一致的工具環境

### 2. 實際應用場景
- **網頁操作**：整合 Puppeteer 進行自動化瀏覽器操作
- **錯誤監控**：連接 Sentry 進行即時錯誤追蹤和分析
- **資料庫存取**：透過自訂 MCP 伺服器連接各種資料庫
- **API 整合**：連接第三方服務和內部 API

### 3. 配置最佳實踐

#### 專案特定配置
```json
{
  "mcpServers": {
    "puppeteer": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-puppeteer"]
    },
    "sentry": {
      "command": "npx", 
      "args": ["@modelcontextprotocol/server-sentry", "--token", "YOUR_TOKEN"]
    }
  }
}
```

#### 除錯與問題排解
- **除錯模式**：使用 `--mcp-debug` 標誌識別配置問題
- **連接驗證**：確認 MCP 伺服器正確啟動和連接
- **權限管理**：適當配置工具權限以確保安全性

### 4. 開發建議
- **逐步導入**：從簡單的 MCP 工具開始，逐步增加複雜度
- **文件化配置**：在 CLAUDE.md 中記錄專案特定的 MCP 配置
- **測試環境**：在開發環境中充分測試 MCP 整合後再部署
- **安全考量**：謹慎管理包含敏感資訊的 MCP 配置，避免意外提交機密資料