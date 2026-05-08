import json
import os
import markdown

def generate_html(article):
    # MarkdownをHTMLに変換
    content_html = markdown.markdown(article['content'])
    
    # テンプレートの作成
    template = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article['title']}</title>
    <meta name="description" content="{article['description']}">
    <meta name="keywords" content="{article['keywords']}">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;700&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary-color: #8B4513; /* Saddle Brown */
            --secondary-color: #D2B48C; /* Tan */
            --accent-color: #DC143C; /* Crimson */
            --light-bg: #FFF8DC; /* Cornsilk */
            --text-dark: #333333;
            --text-light: #666666;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Noto Sans JP', sans-serif;
            line-height: 1.6;
            color: var(--text-dark);
            background-color: #FAFAFA;
        }}

        header {{
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            color: white;
            padding: 60px 20px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}

        header h1 {{
            font-family: 'Playfair Display', serif;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }}

        header p {{
            font-size: 1.1em;
            opacity: 0.95;
        }}

        nav {{
            background-color: var(--primary-color);
            padding: 15px 0;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}

        nav ul {{
            list-style: none;
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 0;
        }}

        nav a {{
            color: white;
            text-decoration: none;
            padding: 12px 20px;
            display: block;
            transition: background-color 0.3s;
        }}

        nav a:hover {{
            background-color: var(--accent-color);
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            background-color: white;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            margin-top: 30px;
            margin-bottom: 30px;
        }}

        h2 {{
            font-family: 'Playfair Display', serif;
            font-size: 2em;
            color: var(--primary-color);
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 3px solid var(--secondary-color);
            margin-top: 40px;
        }}

        h3 {{
            font-size: 1.5em;
            color: var(--primary-color);
            margin-top: 25px;
            margin-bottom: 15px;
        }}

        p {{
            margin-bottom: 1em;
        }}

        ul, ol {{
            margin-left: 20px;
            margin-bottom: 1em;
        }}

        li {{
            margin-bottom: 0.5em;
        }}

        .ad-button-container {{
            text-align: center;
            margin: 40px 0;
        }}

        .ad-button {{
            display: inline-block;
            background-color: var(--accent-color);
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            transition: background-color 0.3s;
        }}

        .ad-button:hover {{
            background-color: #b30000;
        }}

        footer {{
            background-color: var(--primary-color);
            color: white;
            text-align: center;
            padding: 30px 20px;
            margin-top: 60px;
        }}

        footer p {{
            margin-bottom: 10px;
        }}

        footer a {{
            color: var(--secondary-color);
            text-decoration: none;
            margin: 0 15px;
        }}

        footer a:hover {{
            text-decoration: underline;
        }}

        @media (max-width: 768px) {{
            header h1 {{
                font-size: 1.8em;
            }}

            nav ul {{
                flex-direction: column;
                gap: 0;
            }}

            .container {{
                padding: 20px 15px;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>{article['title'].split('|')[0].strip()}</h1>
        <p>イギリスの伝統的なティータイムを深く知る</p>
    </header>

    <nav>
        <ul>
            <li><a href="index.html#history">歴史</a></li>
            <li><a href="index.html#pastries">代表菓子</a></li>
            <li><a href="index.html#classification">分類</a></li>
            <li><a href="index.html#recipes">レシピ</a></li>
            <li><a href="index.html#columns">コラム</a></li>
        </ul>
    </nav>

    <div class="container">
        {content_html}
        
        <div class="ad-button-container">
            <a href="#" class="ad-button">おすすめの紅茶セットを見る</a>
        </div>
    </div>

    <footer>
        <p>&copy; 2026 イギリス郷土菓子探訪 | All Rights Reserved</p>
        <div>
            <a href="privacy.html">プライバシーポリシー</a>
            <a href="contact.html">お問い合わせ</a>
        </div>
    </footer>
</body>
</html>"""
    return template

def update_index_html(articles):
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # コラムセクションの開始と終了を探す
    start_marker = '<div class="columns-section">'
    end_marker = '</div>\n        </section>'
    
    start_idx = content.find(start_marker) + len(start_marker)
    end_idx = content.find(end_marker, start_idx)
    
    if start_idx == -1 or end_idx == -1:
        print("Could not find columns-section in index.html")
        return

    # 既存のリンクを保持しつつ、新しいリンクを追加
    new_links = ""
    # 既存のリンクをパースするのは複雑なので、JSONから全リンクを再生成する形にする
    # ただし、既存の column1.html なども考慮する必要がある
    
    # 今回はシンプルに、JSONにある記事を先頭に追加する形にする
    for article in articles:
        link_html = f"""
                <a href="{article['slug']}.html" class="column-link">
                    <h4>{article['title'].split('|')[0].strip()}</h4>
                    <p>{article['description']}</p>
                </a>"""
        new_links += link_html
    
    # 既存のコンテンツを維持しつつ、新しいリンクを挿入
    # 既存のリンクが重複しないようにチェックが必要だが、今回は簡易的に追加のみ
    updated_content = content[:start_idx] + new_links + content[start_idx:]
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print("Updated index.html with new article links")

def main():
    with open('articles.json', 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    for article in articles:
        filename = f"{article['slug']}.html"
        html_content = generate_html(article)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Generated: {filename}")
    
    update_index_html(articles)

if __name__ == "__main__":
    main()
