# 10_Skills로_반복_작업_자동화

본문에 실린 순서대로 코드 블록 67개를 그대로 옮겼다.

| 파일 | 절 | 언어 | 첫 줄 |
|---|---|---|---|
| [01.txt](01.txt) | Skills의 구조 | - | `my-skill/` |
| [02.txt](02.txt) | SKILL.md가 중요한 이유 | - | `---` |
| [03.txt](03.txt) | Step 1: 폴더 생성 | - | `mkdir -p .claude/skills/image-optimizer` |
| [04.txt](04.txt) | Step 2: SKILL.md 작성 | - | `이미지 최적화 스킬을 만들어줘.` |
| [05.txt](05.txt) | Step 2: SKILL.md 작성 | - | `---` |
| [06.txt](06.txt) | Step 2: SKILL.md 작성 | - | `## 의존성` |
| [07.txt](07.txt) | Step 3: 테스트 | - | `image-optimizer 스킬을 사용해서` |
| [08.txt](08.txt) | Step 3: 테스트 | - | `/image-optimizer test-images 폴더를 너비 800px, 품질 70으로` |
| [09.txt](09.txt) | 1단계: 폴더 만들기 | - | `.claude/skills 폴더 안에 meeting-summary라는 폴더를 만들어줘.` |
| [10.txt](10.txt) | 2단계: SKILL.md 작성 요청 | - | `회의록 요약 스킬의 SKILL.md를 만들어줘.` |
| [11.txt](11.txt) | 3단계: 템플릿 만들기 | - | `회의록 출력 템플릿도 만들어줘.` |
| [12.txt](12.txt) | 4단계: 테스트하기 | - | `meeting-summary 스킬로 이 회의 내용을 정리해줘:` |
| [13.txt](13.txt) | 1단계: 요구사항 정리 | - | `블로그 포스트 작성 스킬을 만들어줘.` |
| [14.txt](14.txt) | 2단계: 스킬 구조 확인 | - | `blog-writer/` |
| [15.txt](15.txt) | 3단계: 실제 사용 | - | `blog-writer 스킬로 글을 써줘.` |
| [16.txt](16.txt) | 예제 3: 데이터 분석 보고서 Skill | - | `데이터 분석 보고서 스킬을 만들어줘.` |
| [17.txt](17.txt) | 1. 번역 및 교정 Skill | - | `translate-proofread/` |
| [18.txt](18.txt) | 1. 번역 및 교정 Skill | - | `translate-proofread 스킬로 이 영문 이메일을` |
| [19.txt](19.txt) | 1. 번역 및 교정 Skill | - | `# 번역 및 교정 Skill` |
| [20.txt](20.txt) | 2. 문서 템플릿 생성 Skill | - | `doc-templates/` |
| [21.txt](21.txt) | 2. 문서 템플릿 생성 Skill | - | `doc-templates 스킬로 신규 프로젝트 제안서 작성해줘.` |
| [22.txt](22.txt) | 3. 요약 및 정리 Skill | - | `summarize/` |
| [23.txt](23.txt) | 3. 요약 및 정리 Skill | - | `summarize 스킬로 이 긴 보고서를 핵심만 5줄로 요약해줘.` |
| [24.txt](24.txt) | 1. CSV 변환 Skill | - | `csv-tools/` |
| [25.txt](25.txt) | 1. CSV 변환 Skill | - | `csv-tools 스킬로 sales_2024.csv와 sales_2023.csv를 하나로 합쳐줘.` |
| [26.txt](26.txt) | 2. 데이터 시각화 Skill | - | `data-viz/` |
| [27.txt](27.txt) | 2. 데이터 시각화 Skill | - | `data-viz 스킬로 monthly_sales.csv 데이터로` |
| [28.txt](28.txt) | 1. SNS 콘텐츠 생성 Skill | - | `social-content/` |
| [29.txt](29.txt) | 1. SNS 콘텐츠 생성 Skill | - | `social-content 스킬로` |
| [30.txt](30.txt) | 2. 이메일 마케팅 Skill | - | `email-marketing/` |
| [31.txt](31.txt) | 2. 이메일 마케팅 Skill | - | `email-marketing 스킬로 블랙프라이데이 프로모션 이메일 만들어줘.` |
| [32.txt](32.txt) | 1. 파일 정리 Skill | - | `file-organizer/` |
| [33.txt](33.txt) | 1. 파일 정리 Skill | - | `file-organizer 스킬로 Downloads 폴더를 정리해줘.` |
| [34.txt](34.txt) | 2. PDF 도구 Skill | - | `pdf-tools/` |
| [35.txt](35.txt) | 2. PDF 도구 Skill | - | `pdf-tools 스킬로 report1.pdf, report2.pdf, report3.pdf를` |
| [36.txt](36.txt) | 1. 일일 보고서 Skill | - | `daily-report/` |
| [37.txt](37.txt) | 1. 일일 보고서 Skill | - | `daily-report 스킬로 오늘 업무 정리해줘.` |
| [38.txt](38.txt) | Skills 찾기 | - | `[작업 유형]을 자동화하는 스킬이 있을까?` |
| [39.txt](39.txt) | Skills 설치하기 | - | `# 스킬 폴더에 복사` |
| [40.txt](40.txt) | Skills 공유하기 | - | `# GitHub에 올리기` |
| [41.txt](41.txt) | Plugin 설치 | - | `/plugin install 플러그인이름@마켓플레이스이름` |
| [42.txt](42.txt) | Plugin 설치 | - | `claude plugin install 플러그인이름@마켓플레이스이름` |
| [43.txt](43.txt) | Plugin 사용 예시 | - | `방금 설치한 영업팀 플러그인의 제안서 스킬로` |
| [44.txt](44.txt) | GitHub 커넥터 | - | `GitHub에서 my-project 저장소의` |
| [45.txt](45.txt) | GitHub 커넥터 | - | `GitHub의 my-project 저장소에서 지난 릴리스 이후` |
| [46.txt](46.txt) | Notion 커넥터 | - | `Notion의 "프로젝트 관리" 데이터베이스에서` |
| [47.txt](47.txt) | Notion 커넥터 | - | `Notion의 "회의록" 페이지 아래에` |
| [48.txt](48.txt) | Google Drive 커넥터 | - | `Google Drive에서 "2026 예산"이 들어간` |
| [49.txt](49.txt) | Google Drive 커넥터 | - | `Google Drive에 새 문서를 만들고` |
| [50.txt](50.txt) | 조합 예시 1: 데이터 분석 → 보고서 → 공유 | - | `1. sales_2024.csv를 분석해서 결과를 analysis.md로 저장해줘` |
| [51.txt](51.txt) | 조합 예시 2: GitHub 이슈 → 문서화 | - | `1. GitHub 커넥터로 이번 주에 닫힌 이슈들을 가져와줘` |
| [52.txt](52.txt) | 조합 예시 3: 이미지 처리 → SNS 콘텐츠 | - | `1. image-optimizer 스킬로 product-photos 폴더의 사진들을 최적화해줘` |
| [53.txt](53.txt) | 1. 작게 시작하기 | - | `모든 것을 하는 거대한 스킬` |
| [54.txt](54.txt) | 1. 작게 시작하기 | - | `모든 문서 작업을 처리하는 mega-document-skill` |
| [55.txt](55.txt) | 1. 작게 시작하기 | - | `proposal-writer/ # 제안서 전용` |
| [56.txt](56.txt) | 2. 명확한 문서화 | - | `# 좋은 SKILL.md` |
| [57.txt](57.txt) | 3. 에러 처리 | - | `# 좋은 스크립트` |
| [58.txt](58.txt) | 4. 테스트 포함 | - | `test/` |
| [59.txt](59.txt) | 5. 버전 관리 | - | `## 변경 이력` |
| [60.txt](60.txt) | 문제 1: "스킬을 찾을 수 없습니다" | - | `.claude/skills/my-skill 폴더 안에 SKILL.md 파일이 있는지 확인해줘.` |
| [61.txt](61.txt) | 문제 2: "스크립트 실행 오류" | - | `이 스킬에 필요한 Python 라이브러리가 뭔지 확인하고,` |
| [62.txt](62.txt) | 문제 3: "의도한 결과가 나오지 않음" | - | `SKILL.md에 사용 예시를 더 추가해줘.` |
| [63.txt](63.txt) | 문제 4: "파일 경로 문제" | - | `스킬에서 사용하는 모든 경로를 절대 경로로 바꿔줘.` |
| [64.txt](64.txt) | 실습 1: 기본 Skill 만들기 | - | `내가 자주 하는 [작업]을 자동화하는 스킬을 만들어줘.` |
| [65.txt](65.txt) | 실습 2: Plugin 활용하기 | - | `[플러그인 이름] 플러그인으로` |
| [66.txt](66.txt) | 실습 3: Skills + Plugins 조합 | - | `1. [커넥터나 플러그인]으로 [데이터/파일]을 가져와줘` |
| [67.txt](67.txt) | 실습 3: Skills + Plugins 조합 | - | `Skills와 Plugins를 마스터했다면, 이제 여러분은 Claude를 진정한 업무 파트너로 활용할 준비가` |
