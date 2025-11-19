"""
PDF 문서 RAG 예제
-----------------
PDF 파일을 읽어서 RAG 시스템을 구축하는 예제입니다.
텍스트 분할(chunking)과 메타데이터 활용을 보여줍니다.
"""

import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# 환경 변수 로드
load_dotenv()


def load_sample_documents():
    """
    실제 PDF 대신 샘플 텍스트 문서를 로드합니다.
    실제 사용시에는 PyPDFLoader를 사용하세요.
    """
    # 샘플 긴 텍스트 (실제로는 PDF에서 추출된 내용)
    sample_text = """
    파이썬 프로그래밍 가이드

    제1장: 파이썬 소개
    파이썬은 1991년 귀도 반 로섬이 개발한 고급 프로그래밍 언어입니다.
    파이썬이라는 이름은 영국의 코미디 그룹 몬티 파이썬에서 따온 것입니다.
    파이썬은 간결하고 읽기 쉬운 문법을 특징으로 하며, "Life is short, use Python"이라는
    모토로 잘 알려져 있습니다.

    제2장: 파이썬의 특징
    파이썬의 주요 특징은 다음과 같습니다:
    1. 간결한 문법: 들여쓰기로 코드 블록을 구분하여 가독성이 높습니다.
    2. 동적 타이핑: 변수의 타입을 명시할 필요가 없습니다.
    3. 인터프리터 언어: 컴파일 없이 바로 실행 가능합니다.
    4. 다양한 라이브러리: 풍부한 표준 라이브러리와 서드파티 패키지를 제공합니다.
    5. 객체 지향: 클래스와 상속을 지원합니다.

    제3장: 파이썬 설치
    파이썬은 python.org에서 다운로드할 수 있습니다.
    Windows, macOS, Linux 등 대부분의 운영체제를 지원합니다.
    최신 버전은 Python 3.12이며, Python 2는 2020년에 지원이 종료되었습니다.

    설치 후 터미널에서 'python --version' 명령어로 설치를 확인할 수 있습니다.
    pip는 파이썬 패키지 관리자로, 'pip install 패키지명' 형식으로 사용합니다.

    제4장: 데이터 타입
    파이썬의 기본 데이터 타입은 다음과 같습니다:
    - 숫자형: int(정수), float(실수), complex(복소수)
    - 문자열: str, 작은따옴표나 큰따옴표로 표현
    - 불린: bool, True 또는 False
    - 리스트: list, 순서가 있는 가변 컬렉션
    - 튜플: tuple, 순서가 있는 불변 컬렉션
    - 딕셔너리: dict, 키-값 쌍의 컬렉션
    - 집합: set, 중복을 허용하지 않는 컬렉션

    제5장: 제어문
    파이썬의 제어문에는 조건문과 반복문이 있습니다.

    if문은 조건에 따라 코드를 실행합니다:
    if condition:
        # 실행할 코드
    elif another_condition:
        # 다른 조건의 코드
    else:
        # 모든 조건이 거짓일 때

    for문은 시퀀스를 순회합니다:
    for item in sequence:
        # 각 항목에 대해 실행

    while문은 조건이 참인 동안 반복합니다:
    while condition:
        # 조건이 참인 동안 실행
    """

    return [Document(
        page_content=sample_text,
        metadata={"source": "python_guide.pdf", "total_pages": 5}
    )]


def main():
    print("=" * 60)
    print("PDF 문서 RAG 시스템 예제")
    print("=" * 60)

    # 1. 문서 로드
    print("\n[1단계] 문서 로드 중...")
    documents = load_sample_documents()
    print(f"   ✓ 총 {len(documents)}개의 문서 로드 완료")

    # 2. 텍스트 분할 (Chunking)
    print("\n[2단계] 텍스트 분할 중...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,      # 각 청크의 크기
        chunk_overlap=50,    # 청크 간 겹치는 부분 (문맥 유지)
        length_function=len,
        separators=["\n\n", "\n", " ", ""]  # 분할 우선순위
    )

    split_documents = text_splitter.split_documents(documents)
    print(f"   ✓ 문서가 {len(split_documents)}개의 청크로 분할되었습니다")

    # 각 청크 미리보기
    print("\n   [청크 미리보기]")
    for i, doc in enumerate(split_documents[:3], 1):
        preview = doc.page_content[:100].replace('\n', ' ')
        print(f"   청크 {i}: {preview}...")

    # 3. 벡터 스토어 생성
    print("\n[3단계] 벡터 스토어 생성 중...")
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(split_documents, embeddings)
    print("   ✓ 벡터 스토어 생성 완료")

    # 벡터 스토어를 로컬에 저장 (선택사항)
    vector_store.save_local("./faiss_index")
    print("   ✓ 벡터 스토어가 './faiss_index'에 저장되었습니다")

    # 4. RAG 체인 구성
    print("\n[4단계] RAG 체인 구성 중...")
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}  # 상위 3개 청크 검색
        ),
        return_source_documents=True
    )
    print("   ✓ RAG 체인 구성 완료")

    # 5. 질문하기
    print("\n" + "=" * 60)
    print("RAG 시스템 테스트")
    print("=" * 60)

    questions = [
        "파이썬은 누가 개발했나요?",
        "파이썬의 주요 특징을 설명해주세요",
        "파이썬의 기본 데이터 타입에는 어떤 것들이 있나요?",
        "파이썬을 어떻게 설치하나요?"
    ]

    for i, question in enumerate(questions, 1):
        print(f"\n[질문 {i}] {question}")
        print("-" * 60)

        result = qa_chain.invoke({"query": question})

        print(f"[답변]")
        print(f"{result['result']}")

        print(f"\n[참고 청크]")
        for j, doc in enumerate(result['source_documents'], 1):
            content_preview = doc.page_content[:150].replace('\n', ' ')
            print(f"{j}. {content_preview}...")

    # 6. 대화형 모드
    print("\n" + "=" * 60)
    print("대화형 모드 (종료하려면 'quit' 입력)")
    print("=" * 60)

    while True:
        user_question = input("\n질문을 입력하세요: ").strip()

        if user_question.lower() in ['quit', 'exit', '종료', 'q']:
            print("프로그램을 종료합니다.")
            break

        if not user_question:
            continue

        result = qa_chain.invoke({"query": user_question})
        print(f"\n[답변] {result['result']}")


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("오류: OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
        exit(1)

    main()
