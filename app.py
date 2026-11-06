#!/usr/bin/env python3
"""
code-review-assistant Web UI (Flask)
"""

from flask import Flask, render_template_string, request, jsonify
from reviewer import review_code, review_security, review_style

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Code Review Assistant</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1100px; margin: 0 auto; }
        h1 { color: white; text-align: center; margin-bottom: 30px; font-size: 2.5rem; }
        .card {
            background: white;
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            margin-bottom: 20px;
        }
        .tabs { display: flex; gap: 10px; margin-bottom: 20px; }
        .tab {
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            background: #f0f0f0;
            border: none;
            font-size: 1rem;
            transition: all 0.3s;
        }
        .tab.active { background: #2c5364; color: white; }
        textarea {
            width: 100%;
            min-height: 250px;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            font-family: 'Courier New', monospace;
            resize: vertical;
            margin-bottom: 15px;
        }
        textarea:focus { outline: none; border-color: #2c5364; }
        button.generate {
            background: linear-gradient(135deg, #2c5364 0%, #0f2027 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            font-size: 1rem;
            cursor: pointer;
            transition: transform 0.2s;
        }
        button.generate:hover { transform: translateY(-2px); }
        button.generate:disabled { opacity: 0.6; cursor: not-allowed; }
        .result {
            margin-top: 20px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            white-space: pre-wrap;
            display: none;
            line-height: 1.6;
        }
        .result.show { display: block; }
        .loading { text-align: center; color: #2c5364; display: none; }
        .loading.show { display: block; }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #2c5364;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .lang-select, .mode-select { 
            padding: 10px; 
            border-radius: 8px; 
            border: 2px solid #e0e0e0; 
            margin-bottom: 15px;
            margin-right: 10px;
        }
        .stats { display: flex; gap: 20px; margin-bottom: 20px; flex-wrap: wrap; }
        .stat-item { 
            background: #f8f9fa; 
            padding: 15px 20px; 
            border-radius: 8px; 
            text-align: center;
            flex: 1;
            min-width: 120px;
        }
        .stat-value { font-size: 1.5rem; font-weight: bold; color: #2c5364; }
        .stat-label { font-size: 0.9rem; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Code Review Assistant</h1>
        
        <div class="card">
            <div class="tabs">
                <button class="tab active" onclick="switchTab('full')">全面审查</button>
                <button class="tab" onclick="switchTab('security')">安全审查</button>
                <button class="tab" onclick="switchTab('style')">风格审查</button>
            </div>

            <div>
                <label>编程语言:</label>
                <select class="lang-select" id="language">
                    <option value="python">Python</option>
                    <option value="javascript">JavaScript</option>
                    <option value="java">Java</option>
                    <option value="go">Go</option>
                    <option value="sql">SQL</option>
                </select>
            </div>

            <textarea id="code-input" placeholder="粘贴你的代码片段...

def login(username, password):
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    return db.execute(query)"></textarea>
            
            <button class="generate" onclick="review()">开始审查</button>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>AI 正在分析代码，请稍候...</p>
            </div>

            <div class="result" id="result"></div>
        </div>
    </div>

    <script>
        let currentMode = 'full';
        
        function switchTab(mode) {
            currentMode = mode;
            document.querySelectorAll('.tab').forEach((t) => {
                t.classList.remove('active');
            });
            event.target.classList.add('active');
        }
        
        async function review() {
            const code = document.getElementById('code-input').value;
            if (!code.trim()) {
                alert('请粘贴代码');
                return;
            }
            
            document.getElementById('loading').classList.add('show');
            document.getElementById('result').classList.remove('show');
            
            const response = await fetch('/api/review', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    code: code,
                    language: document.getElementById('language').value,
                    mode: currentMode
                })
            });
            
            const data = await response.json();
            
            document.getElementById('loading').classList.remove('show');
            document.getElementById('result').textContent = data.result;
            document.getElementById('result').classList.add('show');
        }
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/review', methods=['POST'])
def api_review():
    data = request.json
    code = data.get('code', '')
    language = data.get('language', 'python')
    mode = data.get('mode', 'full')
    
    if mode == 'full':
        result = review_code(code, language)
    elif mode == 'security':
        result = review_security(code, language)
    elif mode == 'style':
        result = review_style(code, language)
    else:
        result = '未知的审查模式'
    
    return jsonify({'result': result})


if __name__ == '__main__':
    print("🔍 Code Review Assistant 启动中...")
    print("📖 访问 http://localhost:5001")
    app.run(debug=True, port=5001)
