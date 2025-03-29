import os
import json
from flask import current_app

import os
import json
from flask import current_app

class Template:
    """ランディングページテンプレートモデル"""
    
    def __init__(self, template_id, name, description, thumbnail, sections, css_file):
        """
        テンプレートモデルの初期化
        
        Args:
            template_id: テンプレートID（ファイル名に使用）
            name: テンプレート名
            description: テンプレートの説明
            thumbnail: サムネイル画像パス
            sections: セクション定義のリスト
            css_file: 関連するCSSファイルのパス
        """
        self.id = template_id
        self.name = name
        self.description = description
        self.thumbnail = thumbnail
        self.sections = sections
        self.css_file = css_file
    
    @classmethod
    def get_all(cls):
        """
        利用可能なすべてのテンプレートを取得
        
        Returns:
            Template オブジェクトのリスト
        """
        templates = []
        templates_dir = current_app.config['TEMPLATES_DIR']
        
        # テンプレートインデックスファイルの読み込み
        index_path = os.path.join(templates_dir, 'template_index.json')
        if not os.path.exists(index_path):
            # インデックスがなければ空のリストを返す
            return templates
        
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                template_index = json.load(f)
            
            # 各テンプレートを読み込む
            for template_info in template_index:
                template_id = template_info['id']
                template_path = os.path.join(templates_dir, f"{template_id}.json")
                
                if os.path.exists(template_path):
                    with open(template_path, 'r', encoding='utf-8') as f:
                        template_data = json.load(f)
                        template = cls(
                            template_id=template_id,
                            name=template_data.get('name', 'Unnamed Template'),
                            description=template_data.get('description', ''),
                            thumbnail=template_data.get('thumbnail', ''),
                            sections=template_data.get('sections', []),
                            css_file=template_data.get('css_file', '')
                        )
                        templates.append(template)
        except (json.JSONDecodeError, IOError) as e:
            # エラーログを出力するなどの対応
            print(f"Error loading templates: {e}")
        
        return templates
    
    @classmethod
    def get_by_id(cls, template_id):
        """
        IDによるテンプレートの取得
        
        Args:
            template_id: テンプレートID
            
        Returns:
            Template オブジェクト、見つからない場合は None
        """
        template_path = os.path.join(current_app.config['TEMPLATES_DIR'], f"{template_id}.json")
        
        if not os.path.exists(template_path):
            return None
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_data = json.load(f)
                return cls(
                    template_id=template_id,
                    name=template_data.get('name', 'Unnamed Template'),
                    description=template_data.get('description', ''),
                    thumbnail=template_data.get('thumbnail', ''),
                    sections=template_data.get('sections', []),
                    css_file=template_data.get('css_file', '')
                )
        except (json.JSONDecodeError, IOError):
            return None
    
    def to_dict(self):
        """
        テンプレートデータを辞書形式に変換
        
        Returns:
            テンプレートデータの辞書
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'thumbnail': self.thumbnail,
            'sections': self.sections,
            'css_file': self.css_file
        }