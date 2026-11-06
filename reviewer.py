#!/usr/bin/env python3
"""
code-review-assistant: Local AI code review using Ollama.

Usage:
    python reviewer.py --file app.py
    python reviewer.py --code "def add(a, b): return a + b"
"""

import argparse
import ollama

MODEL = "qwen2.5:7b"


def review_code(code: str, language: str = "python") -> str:
    """Review code and return detailed feedback."""
    prompt = f"""你是一个资深的高级软件工程师和代码审查专家。请对以下{language}代码进行全面审查。

代码：
```{language}
{code}
```

请从以下维度进行审查，用Markdown格式输出：

## 1. 总体评分
- 可读性评分：X/10
- 安全性评分：X/10
- 性能评分：X/10
- 可维护性评分：X/10
- 综合评分：X/10

## 2. 安全问题
- 列出所有潜在安全漏洞（如SQL注入、XSS、硬编码密钥等）
- 每个问题给出严重程度（高/中/低）

## 3. 代码规范
- 命名规范问题
- 代码风格问题
- 注释和文档缺失

## 4. 性能问题
- 冗余计算
- 不必要的循环
- 资源泄漏风险

## 5. 改进建议
- 给出具体的优化建议
- 提供改进后的代码示例

请用中文回答，保持专业和建设性的语气。
"""
    
    resp = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
    return resp["message"]["content"]


def review_security(code: str, language: str = "python") -> str:
    """Focused security review only."""
    prompt = f"""你是一个应用安全专家。请对以下{language}代码进行安全审查。

代码：
```{language}
{code}
```

请重点检查：
1. 注入攻击风险（SQL注入、命令注入、XSS）
2. 硬编码的敏感信息（密钥、密码、令牌）
3. 不安全的随机数使用
4. 路径遍历风险
5. 不安全的反序列化
6. 敏感数据泄露

输出格式：
- 每个安全问题列出：严重程度、位置描述、风险说明、修复建议
- 用表格形式展示
"""
    
    resp = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
    return resp["message"]["content"]


def review_style(code: str, language: str = "python") -> str:
    """Focused code style review."""
    prompt = f"""你是一个代码风格专家。请对以下{language}代码进行风格审查。

代码：
```{language}
{code}
```

请检查：
1. 命名规范（变量、函数、类名）
2. 函数长度和复杂度
3. 代码重复
4. 注释和文档字符串
5.  import 组织
6. 错误处理是否完善

给出具体的改进建议和示例。
"""
    
    resp = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
    return resp["message"]["content"]


def main():
    parser = argparse.ArgumentParser(description="Code Review Assistant")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", type=str, help="要审查的文件路径")
    group.add_argument("--code", type=str, help="要审查的代码片段")
    
    parser.add_argument("--language", type=str, default="python", help="编程语言")
    parser.add_argument("--mode", type=str, choices=["full", "security", "style"], default="full", help="审查模式")
    
    args = parser.parse_args()
    
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            code = f.read()
    else:
        code = args.code
    
    print(f"审查中...\n" + "=" * 50)
    
    if args.mode == "full":
        result = review_code(code, args.language)
    elif args.mode == "security":
        result = review_security(code, args.language)
    else:
        result = review_style(code, args.language)
    
    print(result)


if __name__ == "__main__":
    main()
