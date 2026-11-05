# ai-trends

매일 AI 최신 동향(특히 **활용 Best Practice**)을 조사해 GitHub Pages로 발행하는 프로젝트.

- 📖 사이트: https://naeul-lee.github.io/ai-trends/
- 📝 지침: [`GUIDELINES.md`](GUIDELINES.md) — 스케줄 작업이 매번 이 파일을 읽고 실행합니다. 수정 후 push 하면 다음 실행부터 반영됩니다.
- 🗂 결과물: `docs/_posts/YYYY-MM-DD-ai-trends.md` (아카이브 `/archive/`, 주제별 `/tags/`)
- ⏰ 스케줄: Claude 클라우드 루틴, 매일 09:00 KST (https://claude.ai/code/routines)

## 구조
```
GUIDELINES.md          # 조사 지침 (사람이 관리)
scripts/build_archive.py  # archive/tags 페이지 재생성
docs/                  # GitHub Pages 루트 (Jekyll + minima)
  _posts/              # 일일 리포트
  archive.md, tags.md  # 자동 생성
```
