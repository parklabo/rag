# Pull Request 정보

## 📋 변경 사항 요약

이 PR은 RAG(Retrieval-Augmented Generation) 프로젝트의 문서와 실습 예제를 대폭 개선합니다.

## 🎯 주요 개선 사항

### 📚 문서 개선
- **README.md 전면 개편**
  - RAG 개념을 쉬운 비유로 설명 (학생의 시험 비유)
  - 상세한 작동 원리 설명과 Mermaid 다이어그램
  - RAG vs 일반 LLM 비교표 추가
  - 실제 사용 사례 및 FAQ 섹션 추가
  - 성능 최적화 팁 및 고급 기법 안내

### 💻 실습 예제 추가
새로운 `rag-example/` 디렉토리에 3개의 실행 가능한 예제 추가:

1. **basic_rag.py** - 기본 RAG 시스템
   - 메모리 내 샘플 문서 사용
   - FAISS 벡터 스토어 구축
   - 질문-답변 체인 구현
   - 대화형 모드 지원

2. **pdf_rag.py** - PDF 문서 RAG
   - 텍스트 청킹(chunking) 기법 시연
   - 벡터 스토어 로컬 저장
   - 메타데이터 활용

3. **chat_with_docs.py** - 대화형 문서 챗봇
   - 여러 문서 파일 동시 로드
   - 대화 히스토리 유지
   - 출처 문서 추적

### 📄 샘플 문서 (sample-docs/)
실습에 바로 사용할 수 있는 한글 샘플 문서 3개:
- `company_policy.txt` - 회사 정책 문서
- `product_manual.txt` - 제품 사용 설명서
- `faq.txt` - 자주 묻는 질문

### 🛠️ 설정 파일
- **requirements.txt** - 모든 필요한 의존성 명시
- **.env.example** - 환경 변수 템플릿
- **rag-example/README.md** - 예제 실행 가이드

## 📊 파일 변경 통계

```
 10 files changed, 1518 insertions(+), 30 deletions(-)

 새 파일:
 - .env.example
 - requirements.txt
 - rag-example/README.md
 - rag-example/basic_rag.py
 - rag-example/chat_with_docs.py
 - rag-example/pdf_rag.py
 - sample-docs/company_policy.txt
 - sample-docs/faq.txt
 - sample-docs/product_manual.txt

 수정된 파일:
 - README.md (대폭 확장)
```

## 🚀 시작하기

이 PR 머지 후 사용자는 다음과 같이 바로 시작할 수 있습니다:

```bash
# 1. 저장소 클론
git clone <repo-url>
cd rag

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 환경 변수 설정
cp .env.example .env
# .env 파일에 OPENAI_API_KEY 입력

# 4. 예제 실행
cd rag-example
python basic_rag.py
```

## ✨ 주요 특징

1. **초보자 친화적**: 단계별 설명과 쉬운 비유
2. **즉시 실행 가능**: 모든 예제가 바로 작동
3. **한글 지원**: 모든 문서와 예제가 한글
4. **실용적**: 실제 프로젝트에 바로 적용 가능한 패턴
5. **점진적 학습**: 기초부터 고급까지 체계적 구성

## 🎓 학습 경로

1. README.md로 RAG 개념 이해
2. basic_rag.py로 기본 구현 학습
3. pdf_rag.py로 청킹 기법 습득
4. chat_with_docs.py로 실전 적용

## 📝 테스트 완료

- ✅ 모든 Python 스크립트 문법 검증
- ✅ 파일 경로 및 임포트 확인
- ✅ 샘플 문서 인코딩 확인 (UTF-8)
- ✅ README 마크다운 렌더링 확인

## 🔍 리뷰 포인트

1. 문서 설명이 명확하고 이해하기 쉬운가?
2. 예제 코드가 best practice를 따르는가?
3. 샘플 문서가 학습 목적에 적합한가?
4. 의존성 버전이 적절한가?

## 📌 Pull Request 생성 방법

다음 URL을 방문하여 Pull Request를 생성하세요:

**PR 생성 URL:**
```
https://github.com/parklabo/rag/pull/new/claude/improve-rag-docs-01N5Fth5UKz3aJbrLADZz8U5
```

**PR 제목:**
```
📚 RAG 문서 및 예제 대폭 개선
```

**PR 본문:**
위의 내용을 복사하여 PR 본문에 붙여넣으세요.

---

**이 PR을 머지하면 사용자들이 RAG 기술을 쉽게 이해하고 실습할 수 있게 됩니다! 🎉**
