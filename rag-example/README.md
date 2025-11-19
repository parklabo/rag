# RAG 예제 실습 가이드

이 디렉토리에는 RAG(Retrieval-Augmented Generation)를 실습할 수 있는 다양한 예제가 포함되어 있습니다.

## 📋 예제 목록

### 1. basic_rag.py - 기본 RAG 시스템
가장 간단한 형태의 RAG 시스템입니다.
메모리 내 샘플 문서를 사용하여 RAG의 기본 개념을 학습합니다.

**특징:**
- 샘플 문서 직접 생성
- FAISS 벡터 스토어 사용
- 질문-답변 체인 구현
- 출처 문서 표시

**실행 방법:**
```bash
cd rag-example
python basic_rag.py
```

**학습 내용:**
- Document 객체 생성
- 벡터 스토어 구축
- RetrievalQA 체인 사용
- 검색된 문서 확인

---

### 2. pdf_rag.py - PDF 문서 RAG
긴 텍스트를 청크(chunk)로 분할하여 처리하는 방법을 보여줍니다.

**특징:**
- 텍스트 분할(chunking) 기법
- 청크 오버랩 설정
- 벡터 스토어 로컬 저장
- 메타데이터 활용

**실행 방법:**
```bash
cd rag-example
python pdf_rag.py
```

**학습 내용:**
- RecursiveCharacterTextSplitter 사용
- chunk_size와 chunk_overlap 설정
- 벡터 스토어 저장 및 로드
- 청크 단위 검색

---

### 3. chat_with_docs.py - 대화형 문서 챗봇
로컬 문서 파일들을 읽어서 대화형 RAG 챗봇을 만듭니다.

**특징:**
- 여러 텍스트 파일 동시 로드
- 대화 히스토리 유지
- ConversationalRetrievalChain 사용
- 출처 문서 추적

**실행 방법:**
```bash
cd rag-example
python chat_with_docs.py
```

**사용할 문서:**
`../sample-docs/` 디렉토리의 텍스트 파일들:
- company_policy.txt (회사 정책)
- product_manual.txt (제품 매뉴얼)
- faq.txt (자주 묻는 질문)

**학습 내용:**
- 디렉토리에서 문서 일괄 로드
- 대화 메모리 관리
- 이전 대화 내용 기반 답변

---

## 🚀 시작하기

### 1. 환경 설정

```bash
# 가상환경 생성 (프로젝트 루트에서)
cd ..
python -m venv venv

# 가상환경 활성화
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. API 키 설정

`.env` 파일을 생성하고 OpenAI API 키를 설정하세요:

```bash
# 루트 디렉토리에 .env 파일 생성
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

또는 `.env.example` 파일을 복사하여 수정:

```bash
cp .env.example .env
# 그 후 .env 파일을 편집하여 실제 API 키 입력
```

### 3. 예제 실행

원하는 예제를 선택하여 실행:

```bash
cd rag-example

# 기본 예제
python basic_rag.py

# PDF 예제
python pdf_rag.py

# 대화형 챗봇
python chat_with_docs.py
```

---

## 💡 예제별 추천 순서

RAG를 처음 접하는 경우 다음 순서로 학습하는 것을 권장합니다:

1. **basic_rag.py** → RAG의 기본 개념 이해
2. **pdf_rag.py** → 텍스트 분할과 청크 개념 학습
3. **chat_with_docs.py** → 실제 활용 사례 경험

---

## 🔧 커스터마이징 가이드

### 자신만의 문서 추가하기

`../sample-docs/` 디렉토리에 `.txt` 파일을 추가하면 `chat_with_docs.py`에서 자동으로 로드됩니다.

```bash
# 새 문서 추가 예시
echo "나만의 문서 내용" > ../sample-docs/my_document.txt
```

### 다른 LLM 모델 사용하기

코드에서 모델명을 변경:

```python
llm = ChatOpenAI(
    model="gpt-4",  # gpt-3.5-turbo, gpt-4, gpt-4-turbo 등
    temperature=0
)
```

### 검색 개수 조정하기

검색할 문서 개수 변경:

```python
retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}  # 기본값 3에서 5로 증가
)
```

### 청크 크기 조정하기

문서 특성에 맞게 청크 크기 변경:

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,    # 문서가 짧으면 작게
    chunk_overlap=50   # 10-20% 정도 권장
)
```

---

## 📊 성능 비교

각 예제의 특성 비교:

| 예제 | 문서 수 | 메모리 사용 | 응답 속도 | 정확도 |
|------|---------|-------------|-----------|--------|
| basic_rag | 소량 | 낮음 | 빠름 | 높음 |
| pdf_rag | 중간 | 중간 | 중간 | 높음 |
| chat_with_docs | 많음 | 높음 | 느림 | 매우 높음 |

---

## 🐛 문제 해결

### ImportError 발생 시

```bash
# 의존성 재설치
pip install -r ../requirements.txt --upgrade
```

### API 키 오류 시

```bash
# .env 파일 확인
cat ../.env

# API 키가 올바른지 확인
# https://platform.openai.com/api-keys
```

### 벡터 스토어 오류 시

```bash
# FAISS 인덱스 삭제 후 재생성
rm -rf faiss_index/
python pdf_rag.py
```

### 문서를 찾을 수 없다는 오류 시

```bash
# sample-docs 디렉토리 확인
ls -la ../sample-docs/

# 없으면 README의 지침대로 생성
```

---

## 📚 다음 단계

예제를 완료했다면 다음을 시도해보세요:

1. **고급 검색 기법**
   - 하이브리드 검색 (키워드 + 시맨틱)
   - MMR (Maximal Marginal Relevance) 검색
   - 메타데이터 필터링

2. **다양한 문서 형식**
   - PDF 파일 로드 (PyPDFLoader)
   - Word 문서 (Docx2txtLoader)
   - 웹 페이지 (WebBaseLoader)

3. **벡터 스토어 비교**
   - Chroma
   - Pinecone
   - Weaviate

4. **프로덕션 배포**
   - FastAPI로 API 서버 구축
   - Streamlit으로 웹 인터페이스 제작
   - Docker 컨테이너화

---

## 💬 피드백 및 기여

개선 사항이나 버그를 발견하셨나요?
이슈를 생성하거나 PR을 보내주세요!

## 📖 참고 자료

- [LangChain 공식 문서](https://python.langchain.com/)
- [OpenAI API 문서](https://platform.openai.com/docs)
- [FAISS 문서](https://github.com/facebookresearch/faiss)
- [상위 디렉토리 README](../README.md)

---

Happy Learning! 🎓
