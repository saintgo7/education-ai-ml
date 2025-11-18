# LLM 애플리케이션 (Large Language Model Applications)

LangChain, RAG, 프롬프트 엔지니어링을 활용한 LLM 애플리케이션 개발

## 📚 프로젝트 목록

### 1. LangChain 기초 (LangChain Fundamentals)
- Chains, Agents, Tools
- Memory Management
- Prompt Templates
- 📓 [01_langchain_basics.ipynb](./notebooks/01_langchain_basics.ipynb)
- 🔗 [Colab](https://colab.research.google.com/github/yourusername/education-ai-ml/blob/main/llm-applications/notebooks/01_langchain_basics.ipynb)

### 2. RAG (Retrieval Augmented Generation)
- Vector Databases (ChromaDB, Pinecone, Weaviate)
- Document Loading & Splitting
- Embedding Models
- Retrieval Strategies
- 📓 [02_rag_implementation.ipynb](./notebooks/02_rag_implementation.ipynb)
- 🔗 [Colab](https://colab.research.google.com/github/yourusername/education-ai-ml/blob/main/llm-applications/notebooks/02_rag_implementation.ipynb)

### 3. 프롬프트 엔지니어링 (Prompt Engineering)
- Zero-shot, Few-shot Learning
- Chain-of-Thought Prompting
- ReAct Pattern
- Prompt Optimization
- 📓 [03_prompt_engineering.ipynb](./notebooks/03_prompt_engineering.ipynb)
- 🔗 [Colab](https://colab.research.google.com/github/yourusername/education-ai-ml/blob/main/llm-applications/notebooks/03_prompt_engineering.ipynb)

### 4. 챗봇 구축 (Chatbot Development)
- Conversational AI
- Context Management
- Multi-turn Dialogue
- 📓 [04_chatbot_development.ipynb](./notebooks/04_chatbot_development.ipynb)

### 5. LLM 파인튜닝 (LLM Fine-tuning)
- LoRA, QLoRA
- PEFT (Parameter Efficient Fine-Tuning)
- Instruction Tuning
- 📓 [05_llm_finetuning.ipynb](./notebooks/05_llm_finetuning.ipynb)

## 🚀 빠른 시작

```bash
# 의존성 설치
pip install -r requirements.txt

# API 키 설정 (선택사항)
export OPENAI_API_KEY="your-api-key"
export ANTHROPIC_API_KEY="your-api-key"

# 노트북 실행
jupyter notebook
```

## 💻 주요 예제

### LangChain 기본 체인

```python
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# LLM 초기화
llm = OpenAI(temperature=0.7)

# 프롬프트 템플릿
template = "다음 주제에 대해 설명해주세요: {topic}"
prompt = PromptTemplate(template=template, input_variables=["topic"])

# 체인 생성
chain = LLMChain(llm=llm, prompt=prompt)

# 실행
result = chain.run("인공지능의 미래")
print(result)
```

### RAG 구현

```python
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# 문서 로드
loader = TextLoader("document.txt")
documents = loader.load()

# 텍스트 분할
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = text_splitter.split_documents(documents)

# 벡터 저장소 생성
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings)

# RAG 체인
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    retriever=vectorstore.as_retriever(),
    return_source_documents=True
)

# 질의
result = qa_chain({"query": "문서의 주요 내용은?"})
print(result["result"])
```

### LangChain Agent

```python
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.llms import OpenAI

# Tools 정의
tools = [
    Tool(
        name="Calculator",
        func=lambda x: eval(x),
        description="수학 계산에 유용합니다"
    ),
    Tool(
        name="Search",
        func=search_function,
        description="최신 정보 검색에 유용합니다"
    )
]

# Agent 초기화
agent = initialize_agent(
    tools,
    OpenAI(temperature=0),
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 실행
result = agent.run("2024년 AI 트렌드는 무엇이고, 관련 기업들의 시가총액 합은?")
```

### LoRA 파인튜닝

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

# 모델 로드
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    load_in_8bit=True,
    device_map="auto"
)

# LoRA 설정
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# LoRA 적용
model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, lora_config)

# 학습
trainer.train()
```

## 🎯 주요 기술

- ✅ LangChain Framework
- ✅ Vector Databases (ChromaDB, Pinecone, Weaviate)
- ✅ Embedding Models (OpenAI, Sentence Transformers)
- ✅ RAG (Retrieval Augmented Generation)
- ✅ LLM APIs (OpenAI, Anthropic, Cohere)
- ✅ LoRA/QLoRA Fine-tuning
- ✅ Prompt Engineering

## 🎨 데모 애플리케이션

### RAG 챗봇 데모

```bash
cd demos
streamlit run rag_chatbot_demo.py
```

### 문서 Q&A 데모

```bash
cd demos
python document_qa_demo.py
```

## 📊 벡터 데이터베이스

### ChromaDB (로컬)
```python
from langchain.vectorstores import Chroma

vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)
```

### Pinecone (클라우드)
```python
from langchain.vectorstores import Pinecone
import pinecone

pinecone.init(api_key="your-api-key")
vectorstore = Pinecone.from_documents(documents, embeddings, index_name="my-index")
```

## 🚀 실전 응용

1. **고객 지원 챗봇**: FAQ 자동 응답
2. **문서 검색 시스템**: 기업 내부 문서 검색
3. **코드 어시스턴트**: 프로그래밍 도우미
4. **교육 플랫폼**: 개인화된 학습 도우미
5. **컨텐츠 생성**: 블로그, 마케팅 자동화

## 🔒 보안 및 비용 관리

- API 키 안전한 관리
- Rate Limiting 설정
- 토큰 사용량 모니터링
- 캐싱 전략

---

**다음**: [Reinforcement Learning](../reinforcement-learning)
