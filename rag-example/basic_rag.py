"""
기본 RAG 예제
--------------
이 스크립트는 가장 간단한 형태의 RAG 시스템을 보여줍니다.
샘플 문서를 벡터 스토어에 저장하고, 질문에 대한 답변을 생성합니다.
"""

import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_core.documents import Document

# 환경 변수 로드
load_dotenv()


def main():
    print("=" * 60)
    print("기본 RAG 시스템 예제")
    print("=" * 60)

    # 1. 샘플 문서 준비
    print("\n[1단계] 샘플 문서 준비 중...")
    documents = [
        Document(
            page_content="파이썬은 1991년 귀도 반 로섬(Guido van Rossum)이 개발한 프로그래밍 언어입니다.",
            metadata={"source": "python_history", "topic": "history"}
        ),
        Document(
            page_content="파이썬은 간결하고 읽기 쉬운 문법으로 초보자에게 인기가 많습니다. 들여쓰기로 코드 블록을 구분합니다.",
            metadata={"source": "python_features", "topic": "syntax"}
        ),
        Document(
            page_content="파이썬은 데이터 과학, 웹 개발, 인공지능, 자동화 등 다양한 분야에서 사용됩니다.",
            metadata={"source": "python_usage", "topic": "applications"}
        ),
        Document(
            page_content="파이썬의 주요 라이브러리로는 NumPy, Pandas, Django, Flask, TensorFlow 등이 있습니다.",
            metadata={"source": "python_libraries", "topic": "ecosystem"}
        ),
        Document(
            page_content="파이썬은 동적 타이핑을 지원하며, 인터프리터 방식으로 실행됩니다.",
            metadata={"source": "python_features", "topic": "technical"}
        ),
    ]
    print(f"   ✓ 총 {len(documents)}개의 문서 준비 완료")

    # 2. 임베딩 모델 및 벡터 스토어 생성
    print("\n[2단계] 벡터 스토어 생성 중...")
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(documents, embeddings)
    print("   ✓ 문서가 벡터로 변환되어 저장되었습니다")

    # 3. LLM 및 RAG 체인 구성
    print("\n[3단계] RAG 체인 구성 중...")
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0  # 일관된 답변을 위해 0으로 설정
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # 검색된 문서를 모두 포함하는 방식
        retriever=vector_store.as_retriever(search_kwargs={"k": 2}),  # 상위 2개 문서 검색
        return_source_documents=True,  # 출처 문서도 함께 반환
        verbose=False
    )
    print("   ✓ RAG 체인 구성 완료")

    # 4. 질문하기
    print("\n" + "=" * 60)
    print("RAG 시스템 테스트")
    print("=" * 60)

    questions = [
        "파이썬은 누가 만들었나요?",
        "파이썬은 어떤 분야에서 사용되나요?",
        "파이썬의 주요 특징은 무엇인가요?"
    ]

    for i, question in enumerate(questions, 1):
        print(f"\n[질문 {i}] {question}")
        print("-" * 60)

        result = qa_chain.invoke({"query": question})

        print(f"[답변]")
        print(f"{result['result']}")

        print(f"\n[참고한 문서]")
        for j, doc in enumerate(result['source_documents'], 1):
            print(f"{j}. {doc.page_content}")
            print(f"   (출처: {doc.metadata['source']})")
        print("-" * 60)

    # 5. 대화형 모드
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

        print(f"\n[답변]")
        print(f"{result['result']}")

        print(f"\n[참고 문서]")
        for j, doc in enumerate(result['source_documents'], 1):
            print(f"{j}. {doc.page_content[:100]}...")


if __name__ == "__main__":
    # API 키 확인
    if not os.getenv("OPENAI_API_KEY"):
        print("오류: OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
        print(".env 파일에 API 키를 설정하거나 환경 변수로 설정해주세요.")
        exit(1)

    main()
