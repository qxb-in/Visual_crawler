
# 介绍
本项目是一个基于 Playwright 的网页截图自动化爬取方案，结合视觉识别模型构建全流程内容提取链路，精准完成从网页渲
染捕获到截图内容结构化解析的端到端处理流程。

其中，模型使用的是 SmolDocling-256M-preview ，以及本地部署的Qwen2.5-VL-Instruct 的7B和3B模型

# 启动
后端服务是app.py
主要功能在crawler.py里
infer.py是尝试直接用模型将img给OCR成Markdown的结果。
