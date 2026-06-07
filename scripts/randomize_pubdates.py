"""
randomize_pubdates.py
indexed記事(web/book/nisa)のpubDateを自然な投稿スケジュールに再設定する
- 対象: web-*.md / book-*.md / nisa-*.md (article-*.mdはnoindexのため除外)
- ルール: 同日1記事・1〜2日ランダム間隔・06:00〜22:00のランダム時刻
- 開始日: 2026-03-27 / 終了日: 2026-06-07以内
"""

import re
import random
import os
from datetime import date, timedelta

random.seed(12345)  # 再現性のため固定（変更可）

ARTICLES_DIR = os.path.join(os.path.dirname(__file__), "..", "src", "content", "articles")
START_DATE = date(2026, 3, 27)
END_DATE = date(2026, 6, 7)


def get_sort_key(content, filename):
    """現在のpubDateを取得してソートキーに使う。なければファイル名をキーに"""
    m = re.search(r'^pubDate:\s*"([^"]+)"', content, re.MULTILINE)
    if m:
        return m.group(1)[:10]
    return filename


def collect_articles():
    files = []
    for f in sorted(os.listdir(ARTICLES_DIR)):
        if not f.endswith(".md"):
            continue
        if f.startswith("article-"):
            continue  # noindex記事は除外
        path = os.path.join(ARTICLES_DIR, f)
        with open(path, "r", encoding="utf-8") as fp:
            content = fp.read()
        sort_key = get_sort_key(content, f)
        files.append((sort_key, f, path, content))

    files.sort(key=lambda x: x[0])
    return files


def generate_dates(n):
    """n本分の日付を生成。1〜2日ランダム間隔、END_DATEを超えたら1日間隔に切り替え"""
    dates = [START_DATE]
    for _ in range(n - 1):
        remaining_slots = (END_DATE - dates[-1]).days
        remaining_articles = n - len(dates)
        # 残りスロット数が記事数ギリギリなら1日間隔を強制
        if remaining_slots <= remaining_articles:
            gap = 1
        else:
            gap = random.choice([1, 2])
        next_date = dates[-1] + timedelta(days=gap)
        dates.append(next_date)
    return dates


def random_time():
    """06:00〜21:59のランダム時刻"""
    h = random.randint(6, 21)
    m = random.randint(0, 59)
    s = random.randint(0, 59)
    return f"{h:02d}:{m:02d}:{s:02d}"


def update_pubdate(content, new_datetime_str):
    return re.sub(
        r'^pubDate:\s*"[^"]+"',
        f'pubDate: "{new_datetime_str}"',
        content,
        flags=re.MULTILINE,
    )


def main():
    articles = collect_articles()
    n = len(articles)
    dates = generate_dates(n)

    print(f"対象記事数: {n}本")
    print(f"日付範囲: {dates[0]} 〜 {dates[-1]}")
    print()

    for i, (sort_key, filename, path, content) in enumerate(articles):
        d = dates[i]
        t = random_time()
        new_dt = f"{d.isoformat()}T{t}"

        new_content = update_pubdate(content, new_dt)

        with open(path, "w", encoding="utf-8", newline="\n") as fp:
            fp.write(new_content)

        print(f"  [{i+1:02d}] {filename:<35} {sort_key} → {new_dt}")

    print()
    print("完了")


if __name__ == "__main__":
    main()
