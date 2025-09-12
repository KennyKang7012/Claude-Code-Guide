# 無頭模式-自動化部署

## 文章資訊
- 文章原始標題：Claude Code Best Practices
- 文章網址：https://www.anthropic.com/engineering/claude-code-best-practices

## 文章原始內容

Claude Code 包含用於非互動環境（如 CI、預提交鉤子、建構腳本和自動化）的無頭模式。使用 -p 標誌加上提示來啟用無頭模式，使用 --output-format stream-json 來獲得串流 JSON 輸出。

請注意，無頭模式在會話之間不會持續。您必須在每個會話中觸發它。

### 使用 Claude 進行問題分類

無頭模式可以支援由 GitHub 事件觸發的自動化，例如在您的儲存庫中創建新問題時。例如，公開的 Claude Code 儲存庫使用 Claude 來檢查新問題並分配適當的標籤。

### 使用 Claude 作為 linter

Claude Code 可以提供超越傳統 linting 工具檢測範圍的主觀程式碼審查，識別諸如拼字錯誤、過時註釋、誤導性函數或變數名稱等問題。

### 使用帶有自訂工具的無頭模式

claude -p（無頭模式）將 Claude Code 程式化地整合到更大的工作流程中，同時利用其內建工具和系統提示。無頭模式有兩種主要模式：

1. 扇出處理大型遷移或分析（例如，分析數百個日誌中的情感或分析數千個 CSV）：
   - 讓 Claude 編寫腳本來生成任務列表
   - 迴圈執行任務，為每個任務程式化地呼叫 Claude
   - 多次執行腳本並優化您的提示

2. 流水線將 Claude 整合到現有的資料/處理流水線中：
   - 呼叫 claude -p "<your prompt>" --json | your_command
   - JSON 輸出（可選）可以幫助為更容易的自動化處理提供結構

對於這兩種使用情況，使用 --verbose 標誌來除錯 Claude 調用會很有幫助。我們通常建議在生產環境中關閉詳細模式以獲得更清潔的輸出。

## 功能分析與使用建議

無頭模式是 Claude Code 自動化能力的核心，將 AI 輔助開發從互動式體驗擴展到完全自動化的工作流程：

### 1. 無頭模式基礎架構

**核心概念**：
- **非互動執行**：無需人工干預的完全自動化
- **單次會話**：每次執行都是獨立的會話
- **結構化輸出**：支援 JSON 格式便於自動化處理
- **管道整合**：可嵌入現有的 CI/CD 和自動化流程

**基本語法**：
```bash
# 基本無頭模式
claude -p "修復所有 TypeScript 類型錯誤"

# JSON 輸出模式
claude -p "分析程式碼品質" --output-format json

# 串流 JSON 輸出
claude -p "重構認證模組" --output-format stream-json

# 詳細除錯模式
claude -p "建立部署腳本" --verbose
```

### 2. CI/CD 整合應用

**GitHub Actions 整合**：
```yaml
# .github/workflows/claude-automation.yml
name: Claude Code Automation
on:
  push:
    branches: [main]
  pull_request:

jobs:
  code-review:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Claude Code Review
      run: |
        claude -p "審查這次 commit 的程式碼品質，重點檢查安全性問題" \
          --output-format json \
          --allowedTools "Edit,Bash(git:*)" \
          > review-result.json
    
    - name: Process Review Results
      run: |
        python process_review.py review-result.json
        
  lint-fix:
    runs-on: ubuntu-latest  
    steps:
    - uses: actions/checkout@v3
    
    - name: Auto-fix Lint Issues
      run: |
        claude -p "修復所有 ESLint 和 Prettier 錯誤，確保程式碼風格一致" \
          --dangerously-skip-permissions \
          --output-format stream-json
    
    - name: Commit Changes
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add .
        git diff --staged --quiet || git commit -m "Auto-fix: Resolve linting issues"
```

**預提交鉤子整合**：
```bash
#!/bin/sh
# .git/hooks/pre-commit

echo "Running Claude Code quality checks..."

# 檢查程式碼品質
claude -p "檢查即將提交的程式碼，識別潛在問題：
- 未使用的變數或函數
- 拼寫錯誤  
- 不一致的命名
- 潛在的安全問題" \
  --output-format json \
  --allowedTools "Bash(git diff:*)" \
  > pre-commit-check.json

# 處理檢查結果
python .git/hooks/process_check.py pre-commit-check.json

if [ $? -ne 0 ]; then
  echo "❌ Claude 發現程式碼品質問題，請修復後重新提交"
  exit 1
fi

echo "✅ Claude 程式碼檢查通過"
```

### 3. 大規模自動化處理

**扇出模式（Fan-out Pattern）**：
```bash
#!/bin/bash
# migration-script.sh

echo "生成遷移任務列表..."
claude -p "分析 src/ 目錄下的所有 React 組件，
生成需要從 Class 組件遷移到 Function 組件的文件清單，
輸出 JSON 格式的任務列表" \
  --output-format json > migration-tasks.json

echo "執行批量遷移..."
jq -r '.tasks[].file' migration-tasks.json | while read -r file; do
  echo "處理 $file..."
  
  claude -p "將 $file 從 Class 組件重構為 Function 組件，
  保持功能完全一致，使用 React Hooks 替代生命週期方法" \
    --allowedTools "Edit" \
    --output-format json \
    > "migration-result-$(basename $file).json"
    
  # 檢查結果並驗證
  if jq -e '.success' "migration-result-$(basename $file).json" > /dev/null; then
    echo "✅ $file 遷移成功"
  else
    echo "❌ $file 遷移失敗，請手動檢查"
  fi
done

echo "批量遷移完成，正在運行測試驗證..."
claude -p "運行完整的測試套件，確保遷移沒有破壞任何功能" \
  --allowedTools "Bash(npm test:*)" \
  --output-format stream-json
```

**流水線模式（Pipeline Pattern）**：
```bash
#!/bin/bash
# data-processing-pipeline.sh

# 階段 1：資料清理
cat raw-data.csv | \
  claude -p "清理這個 CSV 資料，移除重複項目，標準化日期格式，
  處理缺失值，輸出清理後的 CSV" \
  --output-format text > cleaned-data.csv

# 階段 2：資料分析  
claude -p "分析這個清理後的資料集，
生成統計摘要和趨勢分析，
輸出 JSON 格式的分析結果" \
  --output-format json \
  cleaned-data.csv > analysis-results.json

# 階段 3：報告生成
claude -p "基於分析結果生成 Markdown 格式的執行摘要報告，
包含關鍵指標、趨勢圖表描述和行動建議" \
  --output-format text \
  analysis-results.json > executive-summary.md

echo "資料處理流水線完成！"
```

### 4. 問題分類自動化

**GitHub 問題自動分類**：
```yaml
# .github/workflows/issue-triage.yml
name: Automatic Issue Triage
on:
  issues:
    types: [opened]

jobs:
  triage:
    runs-on: ubuntu-latest
    steps:
    - name: Analyze and Label Issue
      uses: actions/github-script@v6
      with:
        script: |
          const { execSync } = require('child_process');
          
          // 取得問題內容
          const issue = context.payload.issue;
          const issueContent = `${issue.title}\n\n${issue.body}`;
          
          // 使用 Claude 分析問題
          const analysisResult = execSync(`
            echo "${issueContent}" | claude -p "
            分析這個 GitHub 問題，判斷：
            1. 問題類型（bug、feature、documentation、question）
            2. 優先級（critical、high、medium、low）  
            3. 影響範圍（frontend、backend、infrastructure、all）
            4. 建議的處理團隊
            
            以 JSON 格式輸出結果
            " --output-format json
          `).toString();
          
          const analysis = JSON.parse(analysisResult);
          
          // 自動添加標籤
          const labels = [
            \`type: \${analysis.type}\`,
            \`priority: \${analysis.priority}\`,
            \`scope: \${analysis.scope}\`
          ];
          
          await github.rest.issues.addLabels({
            owner: context.repo.owner,
            repo: context.repo.repo,
            issue_number: issue.number,
            labels: labels
          });
          
          // 自動分配給相關團隊
          if (analysis.suggested_team) {
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: issue.number,
              body: \`🤖 自動分析結果：
              
              **問題類型**: \${analysis.type}
              **優先級**: \${analysis.priority}
              **影響範圍**: \${analysis.scope}
              **建議處理團隊**: @\${analysis.suggested_team}
              
              _此分析由 Claude Code 自動生成_\`
            });
          }
```

### 5. 進階自動化模式

**智能程式碼審查**：
```python
#!/usr/bin/env python3
# smart-code-review.py

import json
import subprocess
import sys

def run_claude_review(file_path, diff_content):
    """使用 Claude 進行智能程式碼審查"""
    
    prompt = f"""
    請審查以下程式碼變更：
    
    檔案：{file_path}
    變更內容：
    {diff_content}
    
    重點檢查：
    1. 安全性問題（SQL 注入、XSS、CSRF 等）
    2. 性能問題（查詢效率、記憶體洩漏等）
    3. 可讀性和維護性
    4. 測試覆蓋率
    5. 文檔完整性
    
    如果發現問題，請提供具體的行號和修正建議。
    以 JSON 格式輸出結果。
    """
    
    result = subprocess.run([
        'claude', '-p', prompt,
        '--output-format', 'json',
        '--allowedTools', 'Bash(git diff:*)'
    ], capture_output=True, text=True)
    
    return json.loads(result.stdout)

def main():
    """主要審查流程"""
    
    # 取得所有變更的檔案
    changed_files = subprocess.run([
        'git', 'diff', '--name-only', 'HEAD~1', 'HEAD'
    ], capture_output=True, text=True).stdout.strip().split('\n')
    
    all_reviews = []
    
    for file_path in changed_files:
        if file_path.endswith(('.py', '.js', '.ts', '.jsx', '.tsx')):
            # 取得檔案的 diff
            diff = subprocess.run([
                'git', 'diff', 'HEAD~1', 'HEAD', '--', file_path
            ], capture_output=True, text=True).stdout
            
            # 進行 Claude 審查
            review = run_claude_review(file_path, diff)
            all_reviews.append({
                'file': file_path,
                'review': review
            })
    
    # 輸出審查報告
    report = {
        'summary': f'審查了 {len(all_reviews)} 個檔案',
        'reviews': all_reviews,
        'timestamp': subprocess.run(['date'], capture_output=True, text=True).stdout.strip()
    }
    
    print(json.dumps(report, indent=2, ensure_ascii=False))
    
    # 檢查是否有嚴重問題
    critical_issues = sum(1 for r in all_reviews 
                         if r['review'].get('severity') == 'critical')
    
    if critical_issues > 0:
        print(f"\n❌ 發現 {critical_issues} 個嚴重問題，請修復後重新提交", file=sys.stderr)
        sys.exit(1)
    
    print("\n✅ 程式碼審查通過！", file=sys.stderr)

if __name__ == '__main__':
    main()
```

### 6. 監控與除錯

**效能監控**：
```bash
#!/bin/bash
# monitor-claude-performance.sh

start_time=$(date +%s)

claude -p "執行完整的系統健康檢查，
包括資料庫連接、API 回應時間、記憶體使用率" \
  --output-format json \
  --verbose \
  2> claude-debug.log \
  > health-check.json

end_time=$(date +%s)
execution_time=$((end_time - start_time))

echo "Claude 執行時間：${execution_time} 秒"
echo "Token 使用量：$(jq '.token_usage' health-check.json)"
echo "成功率：$(jq '.success_rate' health-check.json)"

# 記錄效能數據
echo "$(date),${execution_time},$(jq -r '.token_usage.total' health-check.json)" >> claude-performance.csv
```

**錯誤處理與重試機制**：
```bash
#!/bin/bash
# resilient-claude-execution.sh

MAX_RETRIES=3
RETRY_DELAY=5

execute_claude() {
    local prompt="$1"
    local attempt=1
    
    while [ $attempt -le $MAX_RETRIES ]; do
        echo "嘗試 $attempt/$MAX_RETRIES..."
        
        if claude -p "$prompt" --output-format json --timeout 300 > result.json 2> error.log; then
            echo "✅ 執行成功！"
            return 0
        else
            echo "❌ 執行失敗，錯誤詳情："
            cat error.log
            
            if [ $attempt -lt $MAX_RETRIES ]; then
                echo "等待 $RETRY_DELAY 秒後重試..."
                sleep $RETRY_DELAY
                RETRY_DELAY=$((RETRY_DELAY * 2))  # 指數退避
            fi
            
            attempt=$((attempt + 1))
        fi
    done
    
    echo "❌ 所有重試都失敗了"
    return 1
}

# 使用範例
execute_claude "分析系統日誌並生成異常報告"
```

### 7. 最佳實踐與注意事項

**安全考量**：
- 在隔離環境中執行無頭模式
- 嚴格控制 `--dangerously-skip-permissions` 的使用
- 定期審查自動化腳本的權限設定
- 實施日誌記錄和稽核追蹤

**效能優化**：
- 使用適當的超時設定
- 實施重試和錯誤恢復機制  
- 監控 Token 使用量和執行時間
- 批量處理時適當控制並發數量

**維護策略**：
- 定期更新自動化腳本
- 測試 Claude 版本升級的相容性
- 建立自動化流程的版本控制
- 文件化所有自動化工作流程

無頭模式將 Claude Code 從開發工具轉變為強大的自動化平台，使 AI 輔助開發能夠無縫整合到現代軟體交付流程中。