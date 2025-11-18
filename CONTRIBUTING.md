# 기여 가이드 (Contributing Guide)

AI/ML 교육 저장소에 기여해주셔서 감사합니다! 🎉

## 🤝 기여 방법

### 1. 이슈 생성
- 버그 리포트, 기능 제안, 문서 개선 등 이슈를 자유롭게 생성해주세요
- 명확한 제목과 상세한 설명을 포함해주세요

### 2. Fork & Clone

```bash
# Fork 후 클론
git clone https://github.com/YOUR-USERNAME/education-ai-ml.git
cd education-ai-ml

# Upstream 추가
git remote add upstream https://github.com/ORIGINAL-OWNER/education-ai-ml.git
```

### 3. 브랜치 생성

```bash
# Feature 브랜치 생성
git checkout -b feature/your-feature-name

# Bugfix 브랜치 생성
git checkout -b bugfix/your-bugfix-name
```

### 4. 변경 사항 작성

#### 코드 스타일
- **Python**: PEP 8 준수
- **Docstrings**: Google 스타일 사용
- **타입 힌트**: 가능한 경우 타입 힌트 추가

```python
def train_model(data: pd.DataFrame, epochs: int = 10) -> tf.keras.Model:
    """
    모델을 학습합니다.

    Args:
        data: 학습 데이터프레임
        epochs: 학습 에폭 수

    Returns:
        학습된 Keras 모델

    Example:
        >>> model = train_model(df, epochs=20)
    """
    pass
```

#### 노트북 작성 가이드
- 명확한 섹션 제목과 설명 추가
- 코드 셀마다 주석 작성
- 결과 시각화 포함
- 한국어와 영어 병행 설명

### 5. 테스트

```bash
# 의존성 설치
pip install -r requirements.txt
pip install pytest pytest-cov

# 테스트 실행
pytest tests/

# 코드 스타일 체크
flake8 .
black --check .
```

### 6. 커밋

```bash
# 변경 사항 추가
git add .

# 커밋 (명확한 메시지 작성)
git commit -m "Add: CNN 이미지 분류 예제 추가"
```

#### 커밋 메시지 규칙
- `Add`: 새로운 기능/파일 추가
- `Update`: 기존 기능 개선
- `Fix`: 버그 수정
- `Docs`: 문서 수정
- `Style`: 코드 스타일 변경
- `Refactor`: 코드 리팩토링
- `Test`: 테스트 추가/수정

### 7. Push & Pull Request

```bash
# 브랜치 푸시
git push origin feature/your-feature-name
```

GitHub에서 Pull Request 생성:
- 명확한 제목과 설명 작성
- 관련 이슈 번호 참조 (`Closes #123`)
- 스크린샷 또는 데모 추가 (해당하는 경우)

## 📝 기여 아이디어

### 새로운 예제 추가
- 실전 프로젝트 예제
- 최신 모델 구현 (GPT-4, Stable Diffusion 등)
- 한국어 데이터셋 활용 예제

### 문서 개선
- 튜토리얼 번역 (영어 ↔ 한국어)
- 설명 보강
- 코드 주석 추가

### 버그 수정
- 오타 수정
- 코드 에러 수정
- 링크 수정

### 데모 애플리케이션
- Streamlit/Gradio 데모 추가
- 대화형 시각화
- 웹 애플리케이션

## ✅ Pull Request 체크리스트

PR을 생성하기 전에 확인해주세요:

- [ ] 코드가 PEP 8 스타일을 따릅니다
- [ ] 모든 테스트가 통과합니다
- [ ] 새로운 기능에 대한 테스트를 추가했습니다
- [ ] 문서를 업데이트했습니다 (README, docstrings 등)
- [ ] 커밋 메시지가 명확합니다
- [ ] 브랜치가 최신 main과 동기화되어 있습니다

## 🎯 우선순위

특히 환영하는 기여:

1. **한국어 컨텐츠**: 한국어 설명, 한국어 데이터셋 활용
2. **실전 프로젝트**: 산업에서 사용하는 실전 예제
3. **최신 기술**: 최신 논문 구현, State-of-the-art 모델
4. **성능 최적화**: 코드 최적화, 효율성 개선
5. **접근성**: 초보자를 위한 쉬운 설명

## 📧 질문이 있으신가요?

- GitHub Issues에 질문 남기기
- Discussions 탭 활용
- 이메일: your.email@example.com

## 🙏 감사합니다!

여러분의 기여가 많은 사람들의 AI/ML 학습에 도움이 됩니다.
함께 성장하는 커뮤니티를 만들어갑시다! 🚀
