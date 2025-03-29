from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, current_app
from app.models.template import Template
from app.models.section import Section
from app.models.project import Project
from app.services.ai_service import AIService
import json
import os

bp = Blueprint('editor', __name__, url_prefix='/editor')

@bp.route('/templates')
def template_select():
    """テンプレート選択画面を表示"""
    templates = Template.get_all()
    return render_template('editor/template_select.html', templates=templates)

@bp.route('/create', methods=['POST'])
def create_project():
    """新しいプロジェクトを作成"""
    template_id = request.form.get('template_id')
    project_name = request.form.get('project_name', 'New Project')
    
    if not template_id:
        # テンプレートIDが指定されていない場合はエラー
        return redirect(url_for('editor.template_select'))
    
    # テンプレートを取得
    template = Template.get_by_id(template_id)
    if not template:
        return redirect(url_for('editor.template_select'))
    
    # テンプレートからセクションを作成
    sections = []
    for section_def in template.sections:
        section = Section.create_default(
            section_type=section_def.get('type'),
            section_id=section_def.get('id')
        )
        sections.append(section.to_dict())
    
    # プロジェクトを作成
    project = Project.create_new(
        name=project_name,
        template_id=template_id,
        sections=sections
    )
    
    # プロジェクトを保存
    if project.save():
        # 成功した場合はエディタ画面にリダイレクト
        return redirect(url_for('editor.edit_project', project_id=project.id))
    else:
        # 保存に失敗した場合
        return redirect(url_for('editor.template_select'))

@bp.route('/edit/<project_id>')
def edit_project(project_id):
    """プロジェクト編集画面を表示"""
    project = Project.get_by_id(project_id)
    if not project:
        return redirect(url_for('main.dashboard'))
    
    # テンプレート情報を取得
    template = Template.get_by_id(project.template_id)
    
    return render_template('editor/section_edit.html', 
                          project=project,
                          template=template)

@bp.route('/preview/<project_id>')
def preview_project(project_id):
    """プロジェクトのプレビュー画面を表示"""
    project = Project.get_by_id(project_id)
    if not project:
        return redirect(url_for('main.dashboard'))
    
    # テンプレート情報を取得
    template = Template.get_by_id(project.template_id)
    
    return render_template('editor/preview.html', 
                          project=project,
                          template=template)

@bp.route('/save-section/<project_id>', methods=['POST'])
def save_section(project_id):
    """セクションの内容を保存"""
    project = Project.get_by_id(project_id)
    if not project:
        return jsonify({'success': False, 'message': 'Project not found'})
    
    try:
        data = request.get_json()
        section_id = data.get('section_id')
        content = data.get('content', {})
        settings = data.get('settings', {})
        
        # プロジェクト内のセクションを更新
        for i, section in enumerate(project.sections):
            if section['id'] == section_id:
                project.sections[i]['content'] = content
                project.sections[i]['settings'] = settings
                break
        
        # プロジェクトを保存
        if project.save():
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Failed to save project'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@bp.route('/generate-content', methods=['POST'])
def generate_content():
    """AIを使用してコンテンツを生成"""
    try:
        data = request.get_json()
        section_type = data.get('section_type')
        context = data.get('context', {})
        
        # AIサービスの初期化（環境変数に応じて適切なAPIを選択）
        api_type = os.getenv('DEFAULT_AI_API', 'openai')
        ai_service = AIService(api_type=api_type)
        
        # コンテンツ生成
        generated_content = ai_service.generate_content(
            prompt_type=section_type,
            context=context
        )
        
        return jsonify({
            'success': True,
            'content': generated_content
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })