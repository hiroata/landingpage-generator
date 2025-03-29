import os
import json
from flask import current_app
import openai
import anthropic
import requests  # xAI APIのリクエスト用
from app.config.ai_prompts import get_prompt_template

class AIService:
    """AIサービスクラス - 複数のAI APIを統合"""
    
    def __init__(self, api_type="openai"):
        """
        AIサービスの初期化
        
        Args:
            api_type: 使用するAPIのタイプ（"openai", "anthropic", "xai"など）
        """
        self.api_type = api_type
        
        # APIクライアントの初期化
        if api_type == "openai":
            openai.api_key = os.getenv("OPENAI_API_KEY") or current_app.config.get("OPENAI_API_KEY")
            self.client = openai.OpenAI(api_key=openai.api_key)
        elif api_type == "anthropic":
            anthropic_api_key = os.getenv("ANTHROPIC_API_KEY") or current_app.config.get("ANTHROPIC_API_KEY")
            self.client = anthropic.Anthropic(api_key=anthropic_api_key)
        elif api_type == "xai":
            # xAI API キーの取得
            self.xai_api_key = os.getenv("XAI_API_KEY") or current_app.config.get("XAI_API_KEY")
            self.xai_api_url = os.getenv("XAI_API_URL") or current_app.config.get("XAI_API_URL")
    
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
        elif self.api_type == "xai":
            return self._generate_with_xai(prompt, max_tokens)
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
    
    def _generate_with_xai(self, prompt, max_tokens):
        """xAI (Grok 2) APIを使用してテキストを生成"""
        # システムメッセージを含む
        system_message = "あなたはプロフェッショナルなウェブコピーライターです。魅力的で効果的なウェブサイトコンテンツを作成します。"
        
        # APIリクエストを送信
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.xai_api_key}"
        }
        
        payload = {
            "model": "grok-2-1212",  # Grok 2モデル
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(
                self.xai_api_url,
                headers=headers,
                json=payload
            )
            
            # レスポンスをJSONとして解析
            if response.status_code == 200:
                result = response.json()
                return result.get("choices", [{}])[0].get("message", {}).get("content", "")
            else:
                # エラーレスポンスの処理
                error_msg = f"xAI API error: {response.status_code} - {response.text}"
                print(error_msg)
                raise Exception(error_msg)
                
        except Exception as e:
            print(f"xAI API request failed: {str(e)}")
            # エラー時はフォールバックとしてOpenAIを使用するか、エラーメッセージを返す
            return f"コンテンツの生成に失敗しました。エラー: {str(e)}"