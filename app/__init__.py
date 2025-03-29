from flask import Flask
import os

def create_app(test_config=None):
    """Flaskアプリケーションファクトリー関数"""
    # アプリケーションの作成と設定
    app = Flask(__name__, 
                instance_relative_config=True,
                template_folder='../templates',
                static_folder='../static')
    
    # デフォルト設定
    app.config.from_mapping(
        SECRET_KEY='dev',  # 開発用キー（本番では変更が必要）
        TEMPLATES_DIR=os.path.join(app.root_path, '../data/templates'),
        PROJECTS_DIR=os.path.join(app.root_path, '../data/projects'),
        MAX_CONTENT_LENGTH=5 * 1024 * 1024,  # アップロード上限: 5MB
    )

    if test_config is None:
        # テストでない場合は、configファイルから設定を読み込む
        app.config.from_pyfile('../config.py', silent=True)
    else:
        # テスト用設定を適用
        app.config.from_mapping(test_config)

    # 必要なディレクトリが存在することを確認
    for directory in [app.config['TEMPLATES_DIR'], app.config['PROJECTS_DIR']]:
        try:
            os.makedirs(directory, exist_ok=True)
        except OSError:
            pass

    # ルートの登録
    from app.routes import main_routes, editor_routes, export_routes
    app.register_blueprint(main_routes.bp)
    app.register_blueprint(editor_routes.bp)
    app.register_blueprint(export_routes.bp)

    return app