import os

# 創建目錄結構
directories = [
    "docs/Claude-Code-指南/入門基礎",
    "docs/Claude-Code-指南/高級應用", 
    "docs/Claude-Code-指南/專業技巧",
    "docs/Claude-Code-指南/問題解決"
]

# 檢查並創建目錄
for directory in directories:
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"創建目錄: {directory}")
    else:
        print(f"目錄已存在: {directory}")

# 定義檔案分類映射
file_mappings = {
    "入門基礎": [
        "入門基礎-安裝配置.md",
        "入門基礎-帳戶登錄.md", 
        "入門基礎-基本操作.md"
    ],
    "高級應用": [
        "高級應用-版本控制整合.md",
        "高級應用-Subagents多代理協作.md",
        "高級應用-Extended思考模式.md",
        "高級應用-MCP生態整合.md",
        "高級應用-架構設計分析.md"
    ],
    "專業技巧": [
        "專業技巧-提示工程.md",
        "專業技巧-CLAUDE.md記憶管理.md",
        "專業技巧-斜線命令系統.md",
        "專業技巧-管道輸入使用.md"
    ],
    "問題解決": [
        "問題解決-權限安全配置.md"
    ]
}

print(f"\n檔案分類規劃:")
for category, files in file_mappings.items():
    print(f"\n{category}:")
    for file in files:
        print(f"  - {file}")

print(f"\n總共創建了 {len(directories)} 個目錄")
total_files = sum(len(files) for files in file_mappings.values())
print(f"總共規劃了 {total_files} 個檔案")