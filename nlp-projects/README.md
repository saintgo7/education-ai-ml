# NLP 프로젝트 (Natural Language Processing)

자연어 처리 실전 프로젝트와 최신 트랜스포머 모델 활용

## 📚 프로젝트 목록

### 1. 감성 분석 (Sentiment Analysis)
- IMDB 영화 리뷰 분석
- BERT 파인튜닝
- Multi-class Sentiment (긍정/부정/중립)
- 📓 [01_sentiment_analysis.ipynb](./notebooks/01_sentiment_analysis.ipynb)
- 🔗 [Colab](https://colab.research.google.com/github/yourusername/education-ai-ml/blob/main/nlp-projects/notebooks/01_sentiment_analysis.ipynb)

### 2. 개체명 인식 (Named Entity Recognition)
- NER with spaCy
- BERT for Token Classification
- Custom Entity Recognition
- 📓 [02_ner.ipynb](./notebooks/02_ner.ipynb)
- 🔗 [Colab](https://colab.research.google.com/github/yourusername/education-ai-ml/blob/main/nlp-projects/notebooks/02_ner.ipynb)

### 3. 텍스트 생성 (Text Generation)
- GPT-2/GPT-3 파인튜닝
- 한국어 텍스트 생성 (KoGPT)
- Creative Writing Assistant
- 📓 [03_text_generation.ipynb](./notebooks/03_text_generation.ipynb)
- 🔗 [Colab](https://colab.research.google.com/github/yourusername/education-ai-ml/blob/main/nlp-projects/notebooks/03_text_generation.ipynb)

### 4. 질의응답 시스템 (Question Answering)
- SQuAD 데이터셋
- BERT/RoBERTa for QA
- Extractive QA
- 📓 [04_question_answering.ipynb](./notebooks/04_question_answering.ipynb)

### 5. 텍스트 요약 (Text Summarization)
- Abstractive Summarization (T5, BART)
- Extractive Summarization
- 뉴스 기사 요약
- 📓 [05_summarization.ipynb](./notebooks/05_summarization.ipynb)

## 🚀 빠른 시작

```bash
pip install -r requirements.txt
python -m spacy download ko_core_news_sm
jupyter notebook
```

## 💻 주요 예제

### BERT 감성 분석

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import Trainer, TrainingArguments

# 모델 로드
model_name = "bert-base-multilingual-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

# 학습
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    warmup_steps=500,
    weight_decay=0.01,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)

trainer.train()
```

### 텍스트 생성

```python
from transformers import pipeline

generator = pipeline('text-generation', model='gpt2')
text = generator("Once upon a time", max_length=50, num_return_sequences=3)
```

## 🎯 주요 기술

- ✅ Hugging Face Transformers
- ✅ BERT, GPT, T5, BART
- ✅ 한국어 NLP (KoBERT, KoGPT)
- ✅ 토크나이저 (WordPiece, SentencePiece)
- ✅ Fine-tuning 전략
- ✅ Few-shot Learning

## 🎨 데모 애플리케이션

### Streamlit 감성 분석 데모

```bash
cd demos
streamlit run sentiment_analysis_demo.py
```

### Gradio 텍스트 생성 데모

```bash
cd demos
python text_generation_demo.py
```

## 📊 데이터셋

- **한국어**: NSMC, KorQuAD, Korean Hate Speech
- **영어**: IMDB, SQuAD, CNN/Daily Mail
- **다국어**: XNLI, MLQA

---

**다음**: [Computer Vision](../computer-vision)
