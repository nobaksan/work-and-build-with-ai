# 11_프로젝트A_개인_비서_시스템

본문에 실린 순서대로 코드 블록 47개를 그대로 옮겼다.

| 파일 | 절 | 언어 | 첫 줄 |
|---|---|---|---|
| [01.txt](01.txt) | 프로젝트 개요 | - | `브리핑 미리보기` |
| [02.txt](02.txt) | 프로젝트 설정 | - | `폴더 구조 요청` |
| [03.txt](03.txt) | 프로젝트 설정 | - | `프로젝트 구조를 생성했습니다.` |
| [04.txt](04.txt) | 프로젝트 설정 | - | `다음 내용으로 PLAN.md를 작성해줘:` |
| [05.txt](05.txt) | 프로젝트 설정 | - | `config/settings.json에 기본 설정 파일을 만들어줘:` |
| [06.txt](06.txt) | 왜 할 일 관리부터 시작하는가? | - | `간단한 할 일 관리 스크립트를 만들어줘.` |
| [07.txt](07.txt) | 왜 할 일 관리부터 시작하는가? | - | `# scripts/todo.py - Claude가 생성한 코드 (핵심 부분)` |
| [08.txt](08.txt) | 왜 할 일 관리부터 시작하는가? | - | `# 기본 추가` |
| [09.txt](09.txt) | 왜 할 일 관리부터 시작하는가? | - | `# 오늘 할 일 보기` |
| [10.txt](10.txt) | 왜 할 일 관리부터 시작하는가? | - | `# 할 일 완료` |
| [11.txt](11.txt) | 왜 할 일 관리부터 시작하는가? | - | `python scripts/todo.py list --all` |
| [12.txt](12.txt) | 왜 할 일 관리부터 시작하는가? | - | `python scripts/todo.py add "운동하기" --tag 건강 --repeat daily` |
| [13.txt](13.txt) | 왜 할 일 관리부터 시작하는가? | - | `python scripts/todo.py add "운동하기" --tag 건강 --repeat daily` |
| [14.txt](14.txt) | Google Calendar API 설정 (상세 가이드) | - | `Google Calendar API 설정 가이드` |
| [15.txt](15.txt) | Google Calendar API 설정 (상세 가이드) | - | `# 필요한 패키지 설치` |
| [16.txt](16.txt) | Google Calendar API 설정 (상세 가이드) | - | `calendar_sync.py 스크립트를 만들어줘:` |
| [17.txt](17.txt) | Google Calendar API 설정 (상세 가이드) | - | `python scripts/calendar_sync.py today` |
| [18.txt](18.txt) | Google Calendar API 설정 (상세 가이드) | - | `python scripts/calendar_sync.py week` |
| [19.txt](19.txt) | Google Calendar API 설정 (상세 가이드) | - | `python scripts/calendar_sync.py next` |
| [20.txt](20.txt) | Google Calendar API 설정 (상세 가이드) | - | `calendar_sync.py를 수정해서 다음 기능을 추가해줘:` |
| [21.txt](21.txt) | 11.4 이메일 요약 하기 | - | `Gmail API도 연동해줘.` |
| [22.txt](22.txt) | 11.4 이메일 요약 하기 | - | `Gmail API를 연동해서 이메일을 요약하는 스크립트를 만들어줘.` |
| [23.txt](23.txt) | 11.4 이메일 요약 하기 | - | `# 터미널에서 한 번 설정 (Mac·Linux)` |
| [24.txt](24.txt) | 11.4 이메일 요약 하기 | - | `python scripts/email_summary.py` |
| [25.txt](25.txt) | 11.4 이메일 요약 하기 | - | `python scripts/email_summary.py --from "김부장"` |
| [26.txt](26.txt) | 11.4 이메일 요약 하기 | - | `email_summary.py를 수정해서 다음 기능을 추가해줘:` |
| [27.txt](27.txt) | 11.5 데일리 브리핑 통합 하기 | - | `daily_briefing.py를 만들어줘.` |
| [28.txt](28.txt) | 11.5 데일리 브리핑 통합 하기 | - | `python scripts/daily_briefing.py` |
| [29.txt](29.txt) | 11.5 데일리 브리핑 통합 하기 | - | `# 아직 연동하지 않은 상태에서 실행하면` |
| [30.txt](30.txt) | 11.5 데일리 브리핑 통합 하기 | - | `# 데일리 브리핑 - 2026년 2월 23일 (월)` |
| [31.txt](31.txt) | 커스터마이징 옵션: 데일리 브리핑 | - | `# 간단 모드 (핵심만)` |
| [32.txt](32.txt) | 커스터마이징 옵션: 데일리 브리핑 | - | `# TTS로 읽어주기` |
| [33.txt](33.txt) | 매일 아침 자동 실행 설정 | - | `Mac 자동 실행 설정 (launchd)` |
| [34.txt](34.txt) | 매일 아침 자동 실행 설정 | - | `Windows 자동 실행 설정 (Task Scheduler)` |
| [35.txt](35.txt) | 매일 아침 자동 실행 설정 | - | `Linux 자동 실행 설정 (cron)` |
| [36.txt](36.txt) | 매일 아침 자동 실행 설정 | - | `자동화를 더 발전시켜줘:` |
| [37.txt](37.txt) | 일상적인 사용법 | - | `#  아침: 데일리 브리핑 확인` |
| [38.txt](38.txt) | 단축 명령어 설정 (선택) | - | `# ~/.bashrc 또는 ~/.zshrc에 추가` |
| [39.txt](39.txt) | 즉시 추가 가능 (1-2시간) | - | `1. 음성 브리핑 (TTS)` |
| [40.txt](40.txt) | 알림 연동 (2-3시간) | - | `1. Slack 알림` |
| [41.txt](41.txt) | 분석 기능 (3-4시간) | - | `1. 주간/월간 리뷰 자동 생성` |
| [42.txt](42.txt) | AI 강화 (4-5시간) | - | `1. 스마트 우선순위` |
| [43.txt](43.txt) | 통합 확장 (5시간+) | - | `1. Notion 연동` |
| [44.txt](44.txt) | 확장 예시: 주간 리뷰 자동화 | - | `주간 리뷰를 자동 생성하는 weekly_review.py를 만들어줘.` |
| [45.txt](45.txt) | 실습 1: 브리핑에 한 칸 더 넣기 | - | `daily_briefing.py에 항목을 하나 더 추가해줘.` |
| [46.txt](46.txt) | 실습 2: 할 일에 내 규칙 넣기 | - | `todo.py에 다음 기능을 추가해줘.` |
| [47.txt](47.txt) | 실습 3: 자동 실행 걸어 보기 | - | `매일 [시각]에 daily_briefing.py가 자동으로 돌게 설정해줘.` |
