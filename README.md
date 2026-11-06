# Code Review Assistant

> 本地AI代码审查助手，基于 Ollama 大模型，完全离线运行，无需 API Key。

## ✨ 功能特性

- **代码规范检查**：命名规范、代码风格、注释完整性
- **安全漏洞检测**：SQL注入、XSS、硬编码密钥、不安全的依赖
- **性能优化建议**：冗余计算、不必要的循环、内存泄漏风险
- **代码质量评分**：从可读性、可维护性、安全性多维度评分
- **Web 界面**：简洁的浏览器操作界面
- **完全本地**：代码不上传云端，隐私安全

## 🚀 快速开始

### 前置要求

1. 安装 [Ollama](https://ollama.com/)
2. 拉取模型：
   ```bash
   ollama pull qwen2.5:7b
   ```

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动 Web 界面

```bash
python app.py
```

打开浏览器访问 http://localhost:5001

### 命令行模式

```bash
# 审查单个文件
python reviewer.py --file app.py

# 审查代码片段
python reviewer.py --code "def login(username, password): ..."
```

## 📦 项目结构

```
code-review-assistant/
├── app.py              # Flask Web 界面
├── reviewer.py         # 核心审查逻辑
├── requirements.txt    # Python 依赖
└── README.md
```

## 🛠️ 技术栈

- **后端**：Python + Flask
- **LLM**：Ollama (Qwen2.5)
- **前端**：HTML + 原生 JS

## 📝 License

MIT