import os
import json
import datetime
from flask import current_app
from slugify import slugify

class Project:
    """ランディングページプロジェクトモデル"""
    
    def __init__(self, project_id, name, template_id, sections, metadata=None):
        """
        プロジェクトモデルの初期化
        
        Args:
            project_id: プロジェクトID
            name: プロジェクト名
            template_id: 使用しているテンプレートID
            sections: セクションのリスト（辞書形式）
            metadata: プロジェクトのメタデータ（作成日時など）
        """
        self.id = project_id
        self.name = name
        self.template_id = template_id
        self.sections = sections
        self.metadata = metadata or {}
        
        # メタデータが存在しない場合は初期化
        if 'created_at' not in self.metadata:
            self.metadata['created_at'] = datetime.datetime.now().isoformat()
        
        self.metadata['updated_at'] = datetime.datetime.now().isoformat()
    
    @classmethod
    def create_new(cls, name, template_id, sections):
        """
        新しいプロジェクトを作成
        
        Args:
            name: プロジェクト名
            template_id: 使用するテンプレートID
            sections: セクションのリスト
            
        Returns:
            Project オブジェクト
        """
        # プロジェクトIDの生成（名前からスラッグ化し、タイムスタンプを付加）
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        project_id = f"{slugify(name)}-{timestamp}"
        
        return cls(
            project_id=project_id,
            name=name,
            template_id=template_id,
            sections=sections
        )
    
    @classmethod
    def get_by_id(cls, project_id):
        """
        IDによるプロジェクトの取得
        
        Args:
            project_id: プロジェクトID
            
        Returns:
            Project オブジェクト、見つからない場合は None
        """
        project_path = os.path.join(current_app.config['PROJECTS_DIR'], f"{project_id}.json")
        
        if not os.path.exists(project_path):
            return None
        
        try:
            with open(project_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(
                    project_id=project_id,
                    name=data.get('name', 'Unnamed Project'),
                    template_id=data.get('template_id', ''),
                    sections=data.get('sections', []),
                    metadata=data.get('metadata', {})
                )
        except (json.JSONDecodeError, IOError):
            return None
    
    def save(self):
        """
        プロジェクトをファイルに保存
        
        Returns:
            成功した場合は True、失敗した場合は False
        """
        # 保存前に更新日時を更新
        self.metadata['updated_at'] = datetime.datetime.now().isoformat()
        
        project_data = self.to_dict()
        project_path = os.path.join(current_app.config['PROJECTS_DIR'], f"{self.id}.json")
        
        try:
            # ディレクトリが存在することを確認
            os.makedirs(os.path.dirname(project_path), exist_ok=True)
            
            with open(project_path, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, ensure_ascii=False, indent=2)
            return True
        except (IOError, OSError):
            return False
    
    def to_dict(self):
        """
        プロジェクトデータを辞書形式に変換
        
        Returns:
            プロジェクトデータの辞書
        """
        return {
            'id': self.id,
            'name': self.name,
            'template_id': self.template_id,
            'sections': self.sections,
            'metadata': self.metadata
        }