import os
import json
from flask import current_app
import openai
import anthropic
from app.config.ai_prompts import get_prompt_template

class AIService:
    """AIサービスクラス - 複数のAI APIを統合"""
    
    def __init__(self, api_type="openai"):
        """
        AIサービスの初期化
        
        Args:
            api_type: 使用するAPIのタイプ（"openai", "anthropic"など）
        """
        self.api_type = api_type
        
        # APIクライアントの初期化
        if api_type == "openai":
            openai.api_key = os.getenv("OPENAI_API_KEY") or current_app.config.get("OPENAI_API_KEY")
            self.client = openai.OpenAI(api_key=openai.api_key)
        elif api_type == "anthropic":
            anthropic_api_key = os.getenv("ANTHROPIC_API_KEY") or current_app.config.get("ANTHROPIC_API_KEY")
            self.client = anthropic.Anthropic(api_key=anthropic_api_key)
    
    def generate_content(self, prompt_type, context, max_tokens=1000):
        """
        AIを使用してコンテンツを生成
        
        Args:
            prompt_type: プロンプトのタイプ (headline, feature, about, etc.)
            context: コンテキスト情報 (ビジネスタイプ、キーワードなど)
            max_tokens: 生成する最大トークン数
            
        Returns:
            生成されたテキスト
        """
        # プロンプトテンプレートを取得して埋め込み
        prompt_template = get_prompt_template(prompt_type)
        
        # コンテキスト情報をプロンプトに埋め込む
        prompt = prompt_template.format(**context)
        
        # APIタイプに応じた呼び出し
        if self.api_type == "openai":
            return self._generate_with_openai(prompt, max_tokens)
        elif self.api_type == "anthropic":
            return self._generate_with_anthropic(prompt, max_tokens)
        else:
            raise ValueError(f"Unsupported API type: {self.api_type}")
    
    def _generate_with_openai(self, prompt, max_tokens):
        """OpenAI APIを使用してテキストを生成"""
        response = self.client.chat.completions.create(
            model="gpt-4o",  # または他のモデル
            messages=[
                {"role": "system", "content": "あなたはプロフェッショナルなウェブコピーライターです。魅力的で効果的なウェブサイトコンテンツを作成します。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    
    def _generate_with_anthropic(self, prompt, max_tokens):
        """Anthropic Claude APIを使用してテキストを生成"""
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",  # または他のモデル
            max_tokens=max_tokens,
            messages=[
                {"role": "user", "content": prompt}
            ],
            system="あなたはプロフェッショナルなウェブコピーライターです。魅力的で効果的なウェブサイトコンテンツを作成します。"
        )
        return response.content[0].text