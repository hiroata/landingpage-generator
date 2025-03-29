import os

# デバッグ設定
DEBUG = True

# セキュリティ設定
SECRET_KEY = 'dev-secret-key-change-in-production'  # 本番環境では必ず変更する
SESSION_COOKIE_SECURE = False  # 本番環境ではTrueに設定
SESSION_COOKIE_HTTPONLY = True
PERMANENT_SESSION_LIFETIME = 3600  # セッション有効期限（秒）

# API設定
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')  # 環境変数から読み込み
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')  # 環境変数から読み込み
DEFAULT_AI_API = 'openai'  # デフォルトで使用するAI API

# アップロード設定
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 最大アップロードサイズ: 5MB

# テンプレート設定
TEMPLATES_AUTO_RELOAD = True