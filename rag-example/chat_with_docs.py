"""
문서 기반 채팅 인터페이스
-----------------------
로컬 텍스트 파일들을 읽어서 RAG 기반 챗봇을 만드는 예제입니다.
여러 문서를 한번에 로드하고, 대화형으로 질문할 수 있습니다.
"""

import os
import glob
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()


def load_documents_from_directory(directory_path):
    """디렉토리에서 모든 텍스트 파일을 로드합니다."""
    documents = []

    # .txt 파일 찾기
    txt_files = glob.glob(os.path.join(directory_path, "*.txt"))

    if not txt_files:
        print(f"경고: {directory_path}에서 .txt 파일을 찾을 수 없습니다.")
        return documents

    for file_path in txt_files:
        try:
            loader = TextLoader(file_path, encoding='utf-8')
            docs = loader.load()
            documents.extend(docs)
            print(f"   ✓ 로드됨: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"   ✗ 오류: {os.path.basename(file_path)} - {str(e)}")

    return documents


def main():
    print("=" * 60)
    print("문서 기반 대화형 RAG 챗봇")
    print("=" * 60)

    # 1. 문서 디렉토리 설정
    docs_directory = "../sample-docs"

    if not os.path.exists(docs_directory):
        print(f"\n오류: '{docs_directory}' 디렉토리가 존재하지 않습니다.")
        print("sample-docs 디렉토리를 먼저 생성하고 텍스트 파일을 추가해주세요.")
        return

    # 2. 문서 로드
    print(f"\n[1단계] '{docs_directory}'에서 문서 로드 중...")
    documents = load_documents_from_directory(docs_directory)

    if not documents:
        print("\n문서를 찾을 수 없습니다. 프로그램을 종료합니다.")
        return

    print(f"\n   총 {len(documents)}개의 문서 로드 완료")

    # 3. 텍스트 분할
    print("\n[2단계] 텍스트 분할 중...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len
    )

    split_documents = text_splitter.split_documents(documents)
    print(f"   ✓ {len(split_documents)}개의 청크로 분할 완료")

    # 4. 벡터 스토어 생성
    print("\n[3단계] 벡터 스토어 생성 중...")
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(split_documents, embeddings)
    print("   ✓ 벡터 스토어 생성 완료")

    # 5. 대화 메모리 설정
    print("\n[4단계] 대화 체인 구성 중...")
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7  # 좀 더 자연스러운 대화를 위해
    )

    # ConversationalRetrievalChain은 이전 대화를 기억합니다
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
        memory=memory,
        return_source_documents=True,
        verbose=False
    )
    print("   ✓ 대화형 RAG 체인 구성 완료")

    # 6. 대화 시작
    print("\n" + "=" * 60)
    print("채팅 시작! (명령어: 'quit'=종료, 'clear'=대화기록 초기화)")
    print("=" * 60)

    conversation_count = 0

    while True:
        user_input = input("\n당신: ").strip()

        if user_input.lower() in ['quit', 'exit', '종료', 'q']:
            print("\n챗봇을 종료합니다. 안녕히 가세요!")
            break

        if user_input.lower() in ['clear', '초기화']:
            memory.clear()
            conversation_count = 0
            print("\n대화 기록이 초기화되었습니다.")
            continue

        if not user_input:
            continue

        try:
            # 질문 처리
            result = qa_chain.invoke({"question": user_input})
            conversation_count += 1

            print(f"\n봇: {result['answer']}")

            # 출처 표시 (옵션)
            if result.get('source_documents'):
                print(f"\n📚 참고 문서: ", end="")
                sources = set()
                for doc in result['source_documents']:
                    if 'source' in doc.metadata:
                        sources.add(os.path.basename(doc.metadata['source']))
                print(", ".join(sources))

        except Exception as e:
            print(f"\n오류가 발생했습니다: {str(e)}")

    print(f"\n총 {conversation_count}번의 대화를 나눴습니다.")


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("오류: OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
        print(".env 파일에 API 키를 설정해주세요.")
        exit(1)

    main()
