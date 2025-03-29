import os
import json
import shutil
import zipfile
import tempfile
from flask import current_app, render_template
from jinja2 import Template as Jinja2Template
from bs4 import BeautifulSoup
import re

class ExportService:
    """HTMLとアセットのエクスポートを処理するサービス"""
    
    def export_html(self, project, output_dir, include_bootstrap=True, include_jquery=True, minify=False):
        """
        プロジェクトをHTMLとしてエクスポート
        
        Args:
            project: Project オブジェクト
            output_dir: 出力ディレクトリのパス
            include_bootstrap: Bootstrapを含めるか
            include_jquery: jQueryを含めるか
            minify: HTMLを最小化するか
            
        Returns:
            生成されたHTMLファイルのパス
        """
        # HTMLテンプレートを読み込み
        template_path = os.path.join(
            current_app.root_path, 
            '../static/templates', 
            f"{project.template_id}/index.html"
        )
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Jinja2テンプレートとしてレンダリング
        template = Jinja2Template(template_content)
        html_content = template.render(
            project=project,
            sections=project.sections,
            include_bootstrap=include_bootstrap,
            include_jquery=include_jquery
        )
        
        # HTMLの最小化（オプション）
        if minify:
            html_content = self._minify_html(html_content)
        
        # HTMLファイルの保存
        output_path = os.path.join(output_dir, 'index.html')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path
    
    def export_zip(self, project, include_bootstrap=True, include_jquery=True, include_assets=True, minify=False):
        """
        プロジェクトとアセットをZIPアーカイブとしてエクスポート
        
        Args:
            project: Project オブジェクト
            include_bootstrap: Bootstrapを含めるか
            include_jquery: jQueryを含めるか
            include_assets: 画像などのアセットを含めるか
            minify: HTMLとCSSを最小化するか
            
        Returns:
            生成されたZIPファイルのパス
        """
        # 一時ディレクトリを作成
        temp_dir = tempfile.mkdtemp()
        try:
            # HTMLファイルを生成
            self.export_html(
                project=project,
                output_dir=temp_dir,
                include_bootstrap=include_bootstrap,
                include_jquery=include_jquery,
                minify=minify
            )
            
            # CSSファイルをコピー
            css_dir = os.path.join(temp_dir, 'css')
            os.makedirs(css_dir, exist_ok=True)
            
            template_css_path = os.path.join(
                current_app.root_path, 
                '../static/css/templates', 
                f"{project.template_id}.css"
            )
            
            output_css_path = os.path.join(css_dir, 'style.css')
            shutil.copy2(template_css_path, output_css_path)
            
            # CSSの最小化（オプション）
            if minify:
                with open(output_css_path, 'r', encoding='utf-8') as f:
                    css_content = f.read()
                
                css_content = self._minify_css(css_content)
                
                with open(output_css_path, 'w', encoding='utf-8') as f:
                    f.write(css_content)
            
            # アセットをコピー（オプション）
            if include_assets:
                # プロジェクト内で使用されている画像を特定してコピー
                assets_dir = os.path.join(temp_dir, 'img')
                os.makedirs(assets_dir, exist_ok=True)
                
                # アセットディレクトリからのコピー（実際には画像の特定ロジックが必要）
                source_assets_dir = os.path.join(
                    current_app.root_path, 
                    '../static/img/templates', 
                    project.template_id
                )
                
                if os.path.exists(source_assets_dir):
                    # 単純に全てのアセットをコピー（実際には使用中の画像のみをコピーする最適化が必要）
                    for asset in os.listdir(source_assets_dir):
                        asset_path = os.path.join(source_assets_dir, asset)
                        if os.path.isfile(asset_path):
                            shutil.copy2(asset_path, os.path.join(assets_dir, asset))
            
            # ZIPファイルの作成
            zip_path = os.path.join(tempfile.gettempdir(), f"{project.id}.zip")
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # ディレクトリの全内容をZIPに追加
                for root, _, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # ZIPファイル内のパスを計算（temp_dirからの相対パス）
                        arc_name = os.path.relpath(file_path, temp_dir)
                        zipf.write(file_path, arc_name)
            
            return zip_path
        
        finally:
            # 一時ディレクトリの削除
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def _minify_html(self, html_content):
        """
        HTMLコンテンツを最小化
        
        Args:
            html_content: 最小化するHTMLコンテンツ
            
        Returns:
            最小化されたHTMLコンテンツ
        """
        # BeautifulSoupを使用して整形
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # コメントを削除
        for comment in soup.find_all(text=lambda text: isinstance(text, str) and text.strip().startswith('<!--')):
            comment.extract()
        
        # 余分な空白を削除
        html_content = str(soup)
        html_content = re.sub(r'\s{2,}', ' ', html_content)
        html_content = re.sub(r'>\s+<', '><', html_content)
        
        return html_content
    
    def _minify_css(self, css_content):
        """
        CSSコンテンツを最小化
        
        Args:
            css_content: 最小化するCSSコンテンツ
            
        Returns:
            最小化されたCSSコンテンツ
        """
        # コメントを削除
        css_content = re.sub(r'/\*[\s\S]*?\*/', '', css_content)
        
        # 余分な空白を削除
        css_content = re.sub(r'\s{2,}', ' ', css_content)
        css_content = re.sub(r'\s*([:;,{}])\s*', r'\1', css_content)
        css_content = re.sub(r'\s*{\s*', '{', css_content)
        css_content = re.sub(r'\s*}\s*', '}', css_content)
        
        return css_content