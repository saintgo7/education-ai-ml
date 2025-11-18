"""
감성 분석 모델 학습 스크립트 (Transformers)

Usage:
    python train_sentiment_classifier.py --model bert-base-multilingual-cased --epochs 3
"""

import argparse
import logging
from pathlib import Path
import torch
from torch.utils.data import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
    EarlyStoppingCallback
)
from datasets import load_dataset
from sklearn.metrics import accuracy_score, f1_score, precision_recall_fscore_support
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SentimentDataset(Dataset):
    """감성 분석 데이터셋"""
    def __init__(self, texts, labels, tokenizer, max_length=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = self.labels[idx]

        encoding = self.tokenizer(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }


def compute_metrics(pred):
    """평가 지표 계산"""
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)

    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, preds, average='binary'
    )
    acc = accuracy_score(labels, preds)

    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }


def load_imdb_dataset():
    """IMDB 데이터셋 로드"""
    logger.info("Loading IMDB dataset...")
    dataset = load_dataset('imdb')
    return dataset


def load_nsmc_dataset():
    """네이버 영화 리뷰 데이터셋 로드 (한국어)"""
    logger.info("Loading NSMC dataset...")
    try:
        dataset = load_dataset('nsmc')
        return dataset
    except:
        logger.warning("NSMC dataset not available, using IMDB instead")
        return load_imdb_dataset()


def main(args):
    logger.info(f"Model: {args.model}")
    logger.info(f"Device: {'GPU' if torch.cuda.is_available() else 'CPU'}")

    # 토크나이저 및 모델 로드
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForSequenceClassification.from_pretrained(
        args.model,
        num_labels=2  # 이진 분류 (긍정/부정)
    )

    # 데이터셋 로드
    if args.dataset == 'imdb':
        dataset = load_imdb_dataset()
        text_column = 'text'
        label_column = 'label'
    elif args.dataset == 'nsmc':
        dataset = load_nsmc_dataset()
        text_column = 'document'
        label_column = 'label'
    else:
        raise ValueError(f"Unknown dataset: {args.dataset}")

    # 토큰화
    def tokenize_function(examples):
        return tokenizer(
            examples[text_column],
            padding='max_length',
            truncation=True,
            max_length=args.max_length
        )

    logger.info("Tokenizing dataset...")
    tokenized_datasets = dataset.map(tokenize_function, batched=True)
    tokenized_datasets = tokenized_datasets.rename_column(label_column, "labels")
    tokenized_datasets.set_format("torch", columns=["input_ids", "attention_mask", "labels"])

    # 학습 설정
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir=f'{args.output_dir}/logs',
        logging_steps=100,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        push_to_hub=False,
    )

    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["test"],
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
    )

    # 학습
    logger.info("Starting training...")
    trainer.train()

    # 평가
    logger.info("Evaluating model...")
    eval_results = trainer.evaluate()
    logger.info(f"Evaluation results: {eval_results}")

    # 모델 저장
    output_path = Path(args.output_dir) / "final_model"
    trainer.save_model(output_path)
    tokenizer.save_pretrained(output_path)
    logger.info(f"Model saved to {output_path}")

    # 테스트 예제
    logger.info("\nTesting with sample texts...")
    test_texts = [
        "This movie was absolutely fantastic! I loved every minute of it.",
        "Terrible waste of time. I want my money back.",
        "It was okay, nothing special but not bad either."
    ]

    for text in test_texts:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=args.max_length)
        with torch.no_grad():
            outputs = model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            sentiment = "긍정" if predictions[0][1] > 0.5 else "부정"
            confidence = predictions[0][1].item() if sentiment == "긍정" else predictions[0][0].item()

        logger.info(f"\nText: {text}")
        logger.info(f"Sentiment: {sentiment} (Confidence: {confidence:.2%})")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train sentiment classifier')
    parser.add_argument('--model', type=str, default='bert-base-multilingual-cased',
                       help='Pretrained model name')
    parser.add_argument('--dataset', type=str, default='imdb',
                       choices=['imdb', 'nsmc'],
                       help='Dataset to use')
    parser.add_argument('--output_dir', type=str, default='../models/sentiment',
                       help='Output directory')
    parser.add_argument('--epochs', type=int, default=3,
                       help='Number of training epochs')
    parser.add_argument('--batch_size', type=int, default=16,
                       help='Batch size')
    parser.add_argument('--max_length', type=int, default=128,
                       help='Maximum sequence length')

    args = parser.parse_args()
    main(args)
