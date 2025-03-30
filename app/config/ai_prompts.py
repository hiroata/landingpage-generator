"""
AIプロンプトテンプレート定義

各プロンプトは以下のコンテキスト変数を使用できます:
- business_type: ビジネスの種類（製品、サービス、ポートフォリオなど）
- business_name: ビジネス/製品/サービス名
- industry: 業種（テクノロジー、健康、教育など）
- target_audience: ターゲットオーディエンス（年齢層、職業など）
- key_features: 主な特徴やメリット（カンマ区切りリスト）
- tone: 文体トーン（フォーマル、カジュアル、専門的など）
- keywords: SEOキーワード（カンマ区切りリスト）
"""

# プロンプトテンプレート辞書
PROMPT_TEMPLATES = {
    # ヘッドラインセクション用プロンプト
    "headline": """
あなたは{business_name}の魅力的なヘッドラインを作成してください。
業種: {industry}
ターゲットオーディエンス: {target_audience}
主な特徴: {key_features}
トーン: {tone}

以下の要件を満たすヘッドラインを1つだけ提案してください:
- 簡潔で魅力的な表現（30文字以内が理想）
- ビジネスの価値提案を明確に伝える
- ターゲットオーディエンスの関心を引く
- SEOキーワード「{keywords}」のいずれかを自然に含める

ヘッドラインと、その下に表示する1-2文の簡潔なサブヘッドラインも提案してください。
""",

    # 特徴紹介セクション用プロンプト
    "features": """
あなたは{business_name}の主要な特徴を紹介するセクションのコンテンツを作成してください。
業種: {industry}
ターゲットオーディエンス: {target_audience}
主な特徴: {key_features}
トーン: {tone}

以下の要件を満たす特徴紹介コンテンツを作成してください:
- {key_features}から3-4つの主要な特徴を選び、各特徴について:
  - 簡潔で魅力的な見出し（15文字以内）
  - 特徴を説明する2-3文の簡潔な説明
  - メリットを強調し、顧客視点で書く
- 全体で約200-300文字のテキスト
- SEOキーワード「{keywords}」を自然に組み込む

特徴ごとに「見出し: 説明文」の形式で提案してください。
""",

    # 会社/製品紹介セクション用プロンプト
    "about": """
あなたは{business_name}の概要を紹介するセクション（About Us/製品紹介）のコンテンツを作成してください。
業種: {industry}
ターゲットオーディエンス: {target_audience}
主な特徴: {key_features}
トーン: {tone}

以下の要件を満たす紹介コンテンツを作成してください:
- {business_type}の価値提案を明確に伝える（何を提供し、どのような問題を解決するか）
- 信頼性を構築する要素を含める
- 読者に共感を示し、顧客の課題を理解していることを伝える
- 全体で約150-200文字のテキスト
- SEOキーワード「{keywords}」を自然に組み込む

約200文字の簡潔な紹介文を作成してください。
""",

    # CTAセクション用プロンプト
    "cta": """
あなたは{business_name}の行動喚起（CTA）セクションのコンテンツを作成してください。
業種: {industry}
ターゲットオーディエンス: {target_audience}
主な特徴: {key_features}
トーン: {tone}

以下の要件を満たすCTAコンテンツを作成してください:
- 簡潔で魅力的な見出し（20文字以内）
- 行動を促す1-2文の説明文（約40-60文字）
- ボタンテキスト（「今すぐ申し込む」「無料で試す」など - 10文字以内）
- 緊急性や価値を伝える表現を含める
- SEOキーワード「{keywords}」を自然に組み込む

「見出し: 説明文: ボタンテキスト」の形式で提案してください。
""",

    # 価格/プラン紹介セクション用プロンプト
    "pricing": """
あなたは{business_name}の価格プランの紹介文を作成してください。
業種: {industry}
ターゲットオーディエンス: {target_audience}
主な特徴: {key_features}
トーン: {tone}

以下の要件を満たす価格プラン紹介コンテンツを作成してください:
- 価格プランセクションの簡潔な見出し（20文字以内）
- 価格体系の概要を説明する1-2文（約50-70文字）
- 3つのプラン例（Basic, Standard, Premiumなど）について、各プランの:
  - プラン名（10文字以内）
  - 簡潔な説明（30文字以内）
  - 含まれる機能（3-4項目、箇条書き）
- SEOキーワード「{keywords}」を自然に組み込む

「見出し: 説明文: プラン1(名前/説明/機能リスト): プラン2: プラン3:」の形式で提案してください。
""",
    
    # headerセクション用プロンプト（追加）
    "header": """
あなたは{business_name}の魅力的なヘッドラインを作成してください。
業種: {industry}
ターゲットオーディエンス: {target_audience}
主な特徴: {key_features}
トーン: {tone}

以下の要件を満たすヘッドラインを1つだけ提案してください:
- 簡潔で魅力的な表現（30文字以内が理想）
- ビジネスの価値提案を明確に伝える
- ターゲットオーディエンスの関心を引く
- SEOキーワード「{keywords}」のいずれかを自然に含める

ヘッドラインと、その下に表示する1-2文の簡潔なサブヘッドラインも提案してください。
"""
}

def get_prompt_template(prompt_type):
    """
    指定されたタイプのプロンプトテンプレートを取得
    
    Args:
        prompt_type: プロンプトタイプ（headline, features, about, ctaなど）
        
    Returns:
        プロンプトテンプレート文字列
    """
    if prompt_type not in PROMPT_TEMPLATES:
        raise ValueError(f"Unknown prompt type: {prompt_type}")
    
    return PROMPT_TEMPLATES[prompt_type]