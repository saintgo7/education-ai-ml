# Scikit-learn 머신러닝 (Classical ML)

전통적인 머신러닝 알고리즘과 실전 예제

## 📚 학습 내용

### 1. 지도 학습 (Supervised Learning)
- **회귀**: Linear, Ridge, Lasso, ElasticNet, SVR
- **분류**: Logistic, SVM, Decision Tree, Random Forest, XGBoost
- 📓 [01_supervised_learning.ipynb](./notebooks/01_supervised_learning.ipynb)

### 2. 비지도 학습 (Unsupervised Learning)
- **클러스터링**: K-Means, DBSCAN, Hierarchical
- **차원 축소**: PCA, t-SNE, UMAP
- **이상 탐지**: Isolation Forest, One-Class SVM
- 📓 [02_unsupervised_learning.ipynb](./notebooks/02_unsupervised_learning.ipynb)

### 3. 앙상블 기법 (Ensemble Methods)
- Bagging, Boosting (AdaBoost, Gradient Boosting)
- Random Forest, XGBoost, LightGBM, CatBoost
- Stacking, Voting
- 📓 [03_ensemble_methods.ipynb](./notebooks/03_ensemble_methods.ipynb)

### 4. 모델 평가 및 선택
- Cross-Validation
- GridSearchCV, RandomizedSearchCV
- 평가 지표 (Accuracy, Precision, Recall, F1, ROC-AUC)
- 📓 [04_model_evaluation.ipynb](./notebooks/04_model_evaluation.ipynb)

## 🚀 빠른 시작

```bash
pip install -r requirements.txt
jupyter notebook
```

## 💻 주요 예제

### Random Forest 분류기

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 모델 학습
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# 예측 및 평가
y_pred = rf.predict(X_test)
print(classification_report(y_test, y_pred))
```

### 하이퍼파라미터 튜닝

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [100, 200, 500],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(rf, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)
print(f"Best params: {grid_search.best_params_}")
```

## 🎯 실전 프로젝트

1. **타이타닉 생존 예측** - 이진 분류
2. **주택 가격 예측** - 회귀
3. **붓꽃 품종 분류** - 다중 클래스 분류
4. **고객 세분화** - 클러스터링
5. **신용카드 사기 탐지** - 이상 탐지

---

**다음**: [NLP Projects](../nlp-projects)
