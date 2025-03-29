from flask import Blueprint, render_template, redirect, url_for, current_app, session
import os
import json

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """トップページを表示"""
    return render_template('index.html')

@bp.route('/dashboard')
def dashboard():
    """ダッシュボードを表示（保存プロジェクトがある場合）"""
    # プロジェクトリストを取得（初期フェーズでは省略可能）
    projects = []
    # プロジェクトディレクトリ内のJSONファイルをプロジェクトとして読み込む
    if os.path.exists(current_app.config['PROJECTS_DIR']):
        for filename in os.listdir(current_app.config['PROJECTS_DIR']):
            if filename.endswith('.json'):
                project_path = os.path.join(current_app.config['PROJECTS_DIR'], filename)
                try:
                    with open(project_path, 'r', encoding='utf-8') as f:
                        project_data = json.load(f)
                        projects.append({
                            'id': filename.replace('.json', ''),
                            'name': project_data.get('name', 'Unnamed Project'),
                            'template': project_data.get('template', 'Unknown'),
                            'created_at': project_data.get('created_at', 'Unknown'),
                            'updated_at': project_data.get('updated_at', 'Unknown')
                        })
                except (json.JSONDecodeError, IOError):
                    # 破損ファイルはスキップ
                    continue
    
    return render_template('dashboard.html', projects=projects)

@bp.route('/about')
def about():
    """アプリケーション説明ページを表示"""
    return render_template('about.html')