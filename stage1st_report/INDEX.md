# Stage1st 论坛爬取与分析项目

## 目录结构

```
stage1st_project/
├── tools/                          # 工具脚本
│   ├── stage1st_crawler.py         # 爬虫脚本
│   ├── generate_report_pdf.py      # PDF报告生成器
│   └── report_template.py          # 报告模板（可复用）
│
├── docs/                           # 文档
│   ├── README.md                   # 使用说明
│   └── DIALOG_LOG.md               # 对话记录
│
└── archive/                        # 归档数据
    └── thread_2271232/             # 2026-03-02 伊朗冲突帖
        ├── posts_thread_2271232.json   # 原始数据(JSON)
        ├── posts_thread_2271232.txt    # 原始数据(文本)
        ├── iran_conflict_report.pdf    # PDF报告
        ├── iran_conflict_report.html   # HTML报告
        ├── wordcloud_2271232.png       # 词云图
        └── page_sample.html            # 页面样例
```

## 快速开始

### 1. 爬取新帖子

编辑 `tools/stage1st_crawler.py`：
```python
THREAD_ID = "你的帖子ID"
START_PAGE = 起始页码
COOKIES = {"B7Y9_2f85_sid": "你的sid", ...}
```

运行：
```bash
python tools/stage1st_crawler.py
```

### 2. 生成报告

编辑 `tools/report_template.py`：
```python
CONFIG = {
    "data_file": "posts_thread_新ID.json",
    "title": "报告标题",
    # ...
}
```

运行：
```bash
python tools/report_template.py
```

### 3. 归档数据

每次任务完成后，将生成的文件移动到 `archive/thread_新ID/` 目录。

## 依赖安装

```bash
pip install requests beautifulsoup4 jieba wordcloud matplotlib reportlab
```

## 项目历史

| 日期 | 帖子ID | 主题 | 页码范围 | 回复数 |
|------|--------|------|----------|--------|
| 2026-03-02 | 2271232 | 伊朗-以色列冲突 | 1-129 | 约5000+ |
| 2026-03-02 | 2271232 | 伊朗-以色列冲突（更新） | 130-150 | 838 |

## 注意事项

- Cookie有时效性，需定期更新
- 爬取间隔已内置随机延迟(1.5-3.5秒)
- PDF生成需要中文字体支持
