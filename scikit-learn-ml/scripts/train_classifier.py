"""
Scikit-learn 분류기 학습 스크립트

Usage:
    python train_classifier.py --model random_forest --dataset iris
"""

import argparse
import joblib
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris, load_wine, load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_dataset(dataset_name):
    """데이터셋 로드"""
    if dataset_name == 'iris':
        data = load_iris()
    elif dataset_name == 'wine':
        data = load_wine()
    elif dataset_name == 'breast_cancer':
        data = load_breast_cancer()
    else:
        raise ValueError(f"Unknown dataset: {dataset_name}")

    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = data.target
    return X, y, data.target_names


def get_model(model_name, random_state=42):
    """모델 생성"""
    models = {
        'logistic': LogisticRegression(random_state=random_state, max_iter=1000),
        'svm': SVC(random_state=random_state, probability=True),
        'random_forest': RandomForestClassifier(n_estimators=100, random_state=random_state),
        'gradient_boosting': GradientBoostingClassifier(n_estimators=100, random_state=random_state),
        'xgboost': XGBClassifier(n_estimators=100, random_state=random_state),
        'lightgbm': LGBMClassifier(n_estimators=100, random_state=random_state, verbose=-1)
    }
    return models.get(model_name)


def get_param_grid(model_name):
    """하이퍼파라미터 그리드"""
    grids = {
        'random_forest': {
            'n_estimators': [50, 100, 200],
            'max_depth': [10, 20, None],
            'min_samples_split': [2, 5, 10]
        },
        'xgboost': {
            'n_estimators': [50, 100, 200],
            'max_depth': [3, 5, 7],
            'learning_rate': [0.01, 0.1, 0.3]
        },
        'svm': {
            'C': [0.1, 1, 10],
            'kernel': ['rbf', 'linear'],
            'gamma': ['scale', 'auto']
        }
    }
    return grids.get(model_name, {})


def main(args):
    logger.info(f"Loading dataset: {args.dataset}")
    X, y, target_names = load_dataset(args.dataset)
    logger.info(f"Dataset shape: {X.shape}")
    logger.info(f"Classes: {target_names}")

    # 데이터 분할
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    logger.info(f"Train size: {X_train.shape[0]}, Test size: {X_test.shape[0]}")

    # 모델 생성
    logger.info(f"Training model: {args.model}")
    model = get_model(args.model)

    if args.tune:
        # 하이퍼파라미터 튜닝
        logger.info("Performing hyperparameter tuning...")
        param_grid = get_param_grid(args.model)
        if param_grid:
            grid_search = GridSearchCV(
                model, param_grid, cv=5, scoring='accuracy',
                n_jobs=-1, verbose=1
            )
            grid_search.fit(X_train, y_train)
            model = grid_search.best_estimator_
            logger.info(f"Best parameters: {grid_search.best_params_}")
            logger.info(f"Best CV score: {grid_search.best_score_:.4f}")
        else:
            model.fit(X_train, y_train)
    else:
        # 기본 학습
        model.fit(X_train, y_train)

    # Cross-validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=5)
    logger.info(f"CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

    # 테스트 평가
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test) if hasattr(model, 'predict_proba') else None

    logger.info("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=target_names))

    logger.info("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    # ROC-AUC (이진 분류인 경우)
    if len(target_names) == 2 and y_proba is not None:
        roc_auc = roc_auc_score(y_test, y_proba[:, 1])
        logger.info(f"\nROC-AUC Score: {roc_auc:.4f}")

    # Feature Importance
    if hasattr(model, 'feature_importances_'):
        importances = pd.DataFrame({
            'feature': X.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        logger.info("\nTop 10 Important Features:")
        print(importances.head(10))

    # 모델 저장
    output_path = f'../configs/{args.model}_{args.dataset}.joblib'
    joblib.dump(model, output_path)
    logger.info(f"\nModel saved to: {output_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train ML classifier')
    parser.add_argument('--model', type=str, default='random_forest',
                       choices=['logistic', 'svm', 'random_forest',
                               'gradient_boosting', 'xgboost', 'lightgbm'])
    parser.add_argument('--dataset', type=str, default='iris',
                       choices=['iris', 'wine', 'breast_cancer'])
    parser.add_argument('--tune', action='store_true',
                       help='Perform hyperparameter tuning')
    args = parser.parse_args()
    main(args)
