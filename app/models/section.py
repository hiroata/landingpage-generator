class Section:
    """ランディングページのセクションモデル"""
    
    def __init__(self, section_id, section_type, title, content=None, settings=None):
        """
        セクションモデルの初期化
        
        Args:
            section_id: セクションID（HTML要素のIDに使用）
            section_type: セクションタイプ（header, features, about, pricing, ctaなど）
            title: セクションタイトル
            content: セクションコンテンツ（辞書）
            settings: セクション設定（辞書）
        """
        self.id = section_id
        self.type = section_type
        self.title = title
        self.content = content or {}
        self.settings = settings or {}
    
    @classmethod
    def create_default(cls, section_type, section_id=None):
        """
        デフォルト設定でセクションを作成
        
        Args:
            section_type: セクションタイプ
            section_id: セクションID（省略時は自動生成）
            
        Returns:
            Section オブジェクト
        """
        if section_id is None:
            # タイプ名を基にIDを生成
            section_id = f"{section_type}-section"
        
        # セクションタイプに応じたデフォルト設定
        default_settings = {
            "background_color": "#ffffff",
            "text_color": "#333333",
            "padding": "60px 0",
            "text_align": "left",
        }
        
        default_content = {}
        
        # セクションタイプに応じたデフォルトコンテンツ
        if section_type == "header":
            default_title = "ヘッダーセクション"
            default_content = {
                "headline": "魅力的な見出しをここに",
                "subheadline": "あなたの価値提案を伝えるサブ見出し",
                "cta_text": "今すぐ始める",
                "cta_url": "#contact",
                "background_image": ""
            }
        elif section_type == "features":
            default_title = "特徴セクション"
            default_content = {
                "intro_text": "私たちの主な特徴",
                "features": [
                    {
                        "title": "特徴1",
                        "description": "この特徴の説明文をここに記載します。",
                        "icon": "fa-star"
                    },
                    {
                        "title": "特徴2",
                        "description": "この特徴の説明文をここに記載します。",
                        "icon": "fa-heart"
                    },
                    {
                        "title": "特徴3",
                        "description": "この特徴の説明文をここに記載します。",
                        "icon": "fa-bolt"
                    }
                ]
            }
        elif section_type == "about":
            default_title = "会社紹介セクション"
            default_content = {
                "heading": "私たちについて",
                "description": "会社やサービスについての説明文をここに記載します。お客様に伝えたい価値や強みを簡潔に説明しましょう。",
                "image": ""
            }
        elif section_type == "pricing":
            default_title = "料金プランセクション"
            default_content = {
                "heading": "料金プラン",
                "description": "お客様のニーズに合わせた料金プラン",
                "plans": [
                    {
                        "name": "ベーシック",
                        "price": "¥5,000",
                        "period": "月額",
                        "description": "スタンダード機能",
                        "features": ["機能1", "機能2", "機能3"],
                        "cta_text": "選択する",
                        "recommended": False
                    },
                    {
                        "name": "プロ",
                        "price": "¥10,000",
                        "period": "月額",
                        "description": "高度な機能",
                        "features": ["ベーシックの全機能", "追加機能1", "追加機能2", "追加機能3"],
                        "cta_text": "選択する",
                        "recommended": True
                    }
                ]
            }
        elif section_type == "cta":
            default_title = "行動喚起セクション"
            default_content = {
                "heading": "今すぐ始めましょう",
                "description": "簡単な登録で、すぐにサービスをご利用いただけます。",
                "button_text": "無料で試す",
                "button_url": "#signup"
            }
        elif section_type == "contact":
            default_title = "お問い合わせセクション"
            default_content = {
                "heading": "お問い合わせ",
                "description": "ご質問やご相談がございましたら、お気軽にお問い合わせください。",
                "contact_info": {
                    "email": "info@example.com",
                    "phone": "03-1234-5678",
                    "address": "東京都千代田区○○ XX-XX"
                },
                "form_fields": ["名前", "メールアドレス", "件名", "メッセージ"]
            }
        else:
            # 未知のセクションタイプの場合
            default_title = f"{section_type}セクション"
        
        return cls(
            section_id=section_id,
            section_type=section_type,
            title=default_title,
            content=default_content,
            settings=default_settings
        )
    
    def to_dict(self):
        """
        セクションデータを辞書形式に変換
        
        Returns:
            セクションデータの辞書
        """
        return {
            'id': self.id,
            'type': self.type,
            'title': self.title,
            'content': self.content,
            'settings': self.settings
        }