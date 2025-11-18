# TensorFlow/Keras

TensorFlow 2.x와 Keras를 활용한 딥러닝 프로젝트

## 📚 학습 내용

### 1. 이미지 분류 (Image Classification)
- Transfer Learning (VGG16, ResNet50, EfficientNet)
- Fine-tuning 기법
- Data Augmentation
- 📓 [01_image_classification.ipynb](./notebooks/01_image_classification.ipynb)
- 🔗 [Colab](https://colab.research.google.com/github/yourusername/education-ai-ml/blob/main/tensorflow-keras/notebooks/01_image_classification.ipynb)

### 2. 자연어 처리 (NLP)
- 텍스트 임베딩 (Word2Vec, GloVe)
- LSTM/GRU 텍스트 분류
- Sentiment Analysis
- 📓 [02_nlp_keras.ipynb](./notebooks/02_nlp_keras.ipynb)
- 🔗 [Colab](https://colab.research.google.com/github/yourusername/education-ai-ml/blob/main/tensorflow-keras/notebooks/02_nlp_keras.ipynb)

### 3. 시계열 예측 (Time Series)
- LSTM/GRU 시계열 모델
- Stock Price Prediction
- Multivariate Time Series
- 📓 [03_time_series.ipynb](./notebooks/03_time_series.ipynb)
- 🔗 [Colab](https://colab.research.google.com/github/yourusername/education-ai-ml/blob/main/tensorflow-keras/notebooks/03_time_series.ipynb)

## 🚀 빠른 시작

```bash
pip install -r requirements.txt
jupyter notebook
```

## 📦 프로젝트 구조

```
tensorflow-keras/
├── notebooks/          # Jupyter 노트북
├── scripts/            # 프로덕션 스크립트
├── demos/              # Streamlit/Gradio 데모
├── configs/            # 모델 설정
└── checkpoints/        # 학습된 모델
```

## 💻 주요 예제

### Transfer Learning

```python
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model

base_model = ResNet50(weights='imagenet', include_top=False)
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(512, activation='relu')(x)
predictions = Dense(num_classes, activation='softmax')(x)
model = Model(inputs=base_model.input, outputs=predictions)
```

### Custom Training Loop

```python
@tf.function
def train_step(x, y):
    with tf.GradientTape() as tape:
        predictions = model(x, training=True)
        loss = loss_fn(y, predictions)
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    return loss
```

## 🎯 주요 기능

- ✅ Keras Functional API 및 Subclassing API
- ✅ Custom Layers, Losses, Metrics
- ✅ TensorBoard 시각화
- ✅ Model Checkpointing & Early Stopping
- ✅ TFLite 변환 (모바일 배포)
- ✅ TensorFlow Serving

---

**다음**: [Scikit-learn ML](../scikit-learn-ml)
