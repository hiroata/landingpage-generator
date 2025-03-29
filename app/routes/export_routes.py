from flask import Blueprint, render_template, request, jsonify, send_file, current_app
from app.models.project import Project
from app.services.export_service import ExportService
import os
import tempfile
import shutil

bp = Blueprint('export', __name__, url_prefix='/export')

@bp.route('/options/<project_id>')
def export_options(project_id):
    """エクスポートオプション画面を表示"""
    project = Project.get_by_id(project_id)
    if not project:
        return jsonify({'success': False, 'message': 'Project not found'})
    
    return render_template('export/export_options.html', project=project)

@bp.route('/html/<project_id>', methods=['POST'])
def export_html(project_id):
    """プロジェクトをHTMLとしてエクスポート"""
    project = Project.get_by_id(project_id)
    if not project:
        return jsonify({'success': False, 'message': 'Project not found'})
    
    # エクスポートオプションの取得
    include_bootstrap = request.form.get('include_bootstrap', 'true') == 'true'
    include_jquery = request.form.get('include_jquery', 'true') == 'true'
    minify = request.form.get('minify', 'false') == 'true'
    
    # エクスポートサービスの初期化
    export_service = ExportService()
    
    try:
        # 一時ディレクトリを作成
        with tempfile.TemporaryDirectory() as temp_dir:
            # HTMLファイルの生成
            html_path = export_service.export_html(
                project=project,
                output_dir=temp_dir,
                include_bootstrap=include_bootstrap,
                include_jquery=include_jquery,
                minify=minify
            )
            
            # ファイルをクライアントに送信
            return send_file(
                html_path,
                as_attachment=True,
                download_name=f"{project.name.replace(' ', '_')}.html",
                mimetype='text/html'
            )
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@bp.route('/zip/<project_id>', methods=['POST'])
def export_zip(project_id):
    """プロジェクトをZIPとしてエクスポート（HTMLとアセット）"""
    project = Project.get_by_id(project_id)
    if not project:
        return jsonify({'success': False, 'message': 'Project not found'})
    
    # エクスポートオプションの取得
    include_bootstrap = request.form.get('include_bootstrap', 'true') == 'true'
    include_jquery = request.form.get('include_jquery', 'true') == 'true'
    include_assets = request.form.get('include_assets', 'true') == 'true'
    minify = request.form.get('minify', 'false') == 'true'
    
    # エクスポートサービスの初期化
    export_service = ExportService()
    
    try:
        # ZIPファイルの生成
        zip_path = export_service.export_zip(
            project=project,
            include_bootstrap=include_bootstrap,
            include_jquery=include_jquery,
            include_assets=include_assets,
            minify=minify
        )
        
        # ファイルをクライアントに送信
        return send_file(
            zip_path,
            as_attachment=True,
            download_name=f"{project.name.replace(' ', '_')}.zip",
            mimetype='application/zip'
        )
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})