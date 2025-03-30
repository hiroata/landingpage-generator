from PIL import Image, ImageDraw, ImageFont
import os

# ディレクトリが存在するか確認し、なければ作成
def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# プレースホルダー画像を作成
def create_placeholder(path, size, text, bg_color=(200, 200, 200), text_color=(50, 50, 50)):
    # ディレクトリを確認
    ensure_dir(os.path.dirname(path))
    
    # 画像を作成
    img = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # テキストを中央に配置（フォントがなければ自動調整）
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        font = ImageFont.load_default()
    
    text_width, text_height = draw.textsize(text, font=font)
    position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
    draw.text(position, text, font=font, fill=text_color)
    
    # 保存
    img.save(path)
    print(f"画像を作成しました: {path}")

# 必要な画像を作成
create_placeholder('static/img/hero-image.png', (800, 450), 'ランディングページ生成イメージ')
create_placeholder('static/img/templates/thumbnails/product.jpg', (400, 300), '製品テンプレート')
create_placeholder('static/img/templates/thumbnails/service.jpg', (400, 300), 'サービステンプレート')
create_placeholder('static/img/templates/thumbnails/portfolio.jpg', (400, 300), 'ポートフォリオテンプレート')