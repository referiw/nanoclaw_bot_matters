# Stage1st 战报生成器

自动爬取Stage1st论坛帖子并生成HTML格式战报。

## 功能

- 自动登录Stage1st论坛
- 爬取指定帖子的最新回复
- 生成美观的HTML战报
- 关键词分析和词云生成
- 投资建议生成
- 图片嵌入（base64）

## 文件结构

```
stage1st_report/
├── crawler/           # 爬虫相关
│   ├── stage1st_crawler.py
│   └── crawl_pages.py
├── generator/         # 战报生成
│   ├── report_generator.js
│   ├── generate_battle_report.py
│   └── report_template.py
├── data/              # 数据文件
│   └── posts_*.json
└── output/            # 输出文件
```

## 使用方法

1. 安装依赖: `npm install` 或 `pip install -r requirements.txt`
2. 配置账号密码
3. 运行爬虫获取数据
4. 生成战报

## 定时任务

支持通过cron或任务调度器定时执行。
