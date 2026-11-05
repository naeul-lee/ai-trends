#!/usr/bin/env python3
"""docs/_posts/*.md 를 읽어 docs/archive.md (월별) 와 docs/tags.md (주제별) 를 재생성한다."""
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "docs" / "_posts"
URL_PREFIX = "{{ site.baseurl }}"

TAG_LABELS = {
    "best-practice": "🎯 활용 Best Practice",
    "model": "🤖 새로운 모델",
    "serving": "⚙️ LLM 서빙/인프라",
    "monetization": "💰 수익화",
    "industry": "🏢 업계 동향",
    "weekly": "📚 주간 정리",
}


def parse(path: Path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    fm = m.group(1) if m else ""

    def field(name):
        r = re.search(rf"^{name}:\s*(.+)$", fm, re.M)
        return r.group(1).strip().strip('"') if r else ""

    tags_raw = field("tags")
    tags = [t.strip() for t in re.sub(r"[\[\]]", "", tags_raw.split("#")[0]).split(",") if t.strip()]
    date = path.name[:10]
    url = f"{URL_PREFIX}/{date[:4]}/{date[5:7]}/{date[8:10]}/{path.stem[11:]}.html"
    return {"date": date, "title": field("title") or path.stem, "summary": field("summary"), "tags": tags, "url": url}


def main():
    posts = sorted((parse(p) for p in POSTS.glob("*.md")), key=lambda p: p["date"], reverse=True)

    by_month = defaultdict(list)
    for p in posts:
        by_month[p["date"][:7]].append(p)

    out = ["---", "layout: page", "title: 아카이브", "permalink: /archive/", "---", "",
           f"총 {len(posts)}개의 리포트", ""]
    for month in sorted(by_month, reverse=True):
        out += [f"## {month}", ""]
        for p in by_month[month]:
            out.append(f"- **{p['date'][5:]}** [{p['title']}]({p['url']})" + (f" — {p['summary']}" if p["summary"] else ""))
        out.append("")
    (ROOT / "docs" / "archive.md").write_text("\n".join(out), encoding="utf-8")

    by_tag = defaultdict(list)
    for p in posts:
        for t in p["tags"]:
            by_tag[t].append(p)
    out = ["---", "layout: page", "title: 주제별 보기", "permalink: /tags/", "---", ""]
    for t in list(TAG_LABELS) + sorted(set(by_tag) - set(TAG_LABELS)):
        if t not in by_tag:
            continue
        out += [f"## {TAG_LABELS.get(t, t)}", ""]
        out += [f"- {p['date']} [{p['title']}]({p['url']})" for p in by_tag[t]]
        out.append("")
    (ROOT / "docs" / "tags.md").write_text("\n".join(out), encoding="utf-8")
    print(f"archive/tags rebuilt: {len(posts)} posts")


if __name__ == "__main__":
    main()
