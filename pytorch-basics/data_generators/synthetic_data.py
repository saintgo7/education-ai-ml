"""
합성 데이터 생성기

다양한 머신러닝 태스크를 위한 합성 데이터를 생성합니다.

Usage:
    python synthetic_data.py --task classification --num_samples 1000
"""

import argparse
import numpy as np
import torch
from torch.utils.data import TensorDataset, DataLoader
from pathlib import Path
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_classification_data(num_samples=1000, num_features=20, num_classes=2,
                                  class_sep=1.0, random_state=42):
    """분류 데이터 생성"""
    np.random.seed(random_state)

    samples_per_class = num_samples // num_classes
    X = []
    y = []

    for class_idx in range(num_classes):
        # 각 클래스의 중심점
        center = np.random.randn(num_features) * class_sep * class_idx

        # 해당 클래스의 샘플 생성
        class_samples = center + np.random.randn(samples_per_class, num_features)
        X.append(class_samples)
        y.extend([class_idx] * samples_per_class)

    X = np.vstack(X).astype(np.float32)
    y = np.array(y, dtype=np.int64)

    # 셔플
    indices = np.random.permutation(len(X))
    X, y = X[indices], y[indices]

    return X, y


def generate_regression_data(num_samples=1000, num_features=10, noise=0.1, random_state=42):
    """회귀 데이터 생성"""
    np.random.seed(random_state)

    X = np.random.randn(num_samples, num_features).astype(np.float32)

    # 가중치 생성
    weights = np.random.randn(num_features).astype(np.float32)
    bias = np.random.randn()

    # 타겟 생성
    y = X @ weights + bias + np.random.randn(num_samples).astype(np.float32) * noise

    return X, y


def generate_sequence_data(num_samples=1000, seq_length=50, vocab_size=100, random_state=42):
    """시퀀스 데이터 생성 (언어 모델링용)"""
    np.random.seed(random_state)

    # 간단한 패턴이 있는 시퀀스 생성
    sequences = []

    for _ in range(num_samples):
        # 기본 시퀀스 생성
        seq = np.random.randint(1, vocab_size, seq_length)

        # 패턴 추가 (반복)
        pattern_length = np.random.randint(3, 8)
        pattern = seq[:pattern_length]
        repeat_start = np.random.randint(seq_length // 2, seq_length - pattern_length)
        seq[repeat_start:repeat_start + pattern_length] = pattern

        sequences.append(seq)

    X = np.array(sequences, dtype=np.int64)
    y = np.roll(X, -1, axis=1)  # 다음 토큰 예측

    return X, y


def generate_image_data(num_samples=1000, image_size=28, num_channels=1,
                        num_classes=10, random_state=42):
    """이미지 분류 데이터 생성 (MNIST 스타일)"""
    np.random.seed(random_state)

    samples_per_class = num_samples // num_classes
    images = []
    labels = []

    for class_idx in range(num_classes):
        for _ in range(samples_per_class):
            # 빈 이미지
            img = np.zeros((num_channels, image_size, image_size), dtype=np.float32)

            # 클래스별 패턴 생성
            center_y = image_size // 2 + np.random.randint(-3, 4)
            center_x = image_size // 2 + np.random.randint(-3, 4)
            radius = 5 + class_idx

            # 원형 패턴
            for i in range(image_size):
                for j in range(image_size):
                    dist = np.sqrt((i - center_y) ** 2 + (j - center_x) ** 2)
                    if dist < radius:
                        img[0, i, j] = 1.0 - dist / radius

            # 노이즈 추가
            img += np.random.randn(*img.shape).astype(np.float32) * 0.1
            img = np.clip(img, 0, 1)

            images.append(img)
            labels.append(class_idx)

    X = np.array(images, dtype=np.float32)
    y = np.array(labels, dtype=np.int64)

    # 셔플
    indices = np.random.permutation(len(X))
    X, y = X[indices], y[indices]

    return X, y


def generate_time_series_data(num_samples=1000, seq_length=100, num_features=1,
                               noise=0.1, random_state=42):
    """시계열 데이터 생성"""
    np.random.seed(random_state)

    X = []
    y = []

    for _ in range(num_samples):
        # 사인파 + 트렌드 + 노이즈
        t = np.linspace(0, 4 * np.pi, seq_length)
        freq = np.random.uniform(0.5, 2.0)
        amplitude = np.random.uniform(0.5, 1.5)
        trend = np.random.uniform(-0.01, 0.01)

        signal = amplitude * np.sin(freq * t) + trend * t
        signal += np.random.randn(seq_length) * noise

        X.append(signal[:-1].reshape(-1, num_features))
        y.append(signal[1:])

    X = np.array(X, dtype=np.float32)
    y = np.array(y, dtype=np.float32)

    return X, y


def create_dataloader(X, y, batch_size=32, shuffle=True, num_workers=0):
    """DataLoader 생성"""
    X_tensor = torch.from_numpy(X)
    y_tensor = torch.from_numpy(y)
    dataset = TensorDataset(X_tensor, y_tensor)
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle, num_workers=num_workers)


def save_data(X, y, output_dir, prefix="data"):
    """데이터 저장"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    np.save(output_path / f"{prefix}_X.npy", X)
    np.save(output_path / f"{prefix}_y.npy", y)

    # 메타데이터 저장
    metadata = {
        "num_samples": len(X),
        "X_shape": list(X.shape),
        "y_shape": list(y.shape),
        "X_dtype": str(X.dtype),
        "y_dtype": str(y.dtype),
    }

    with open(output_path / f"{prefix}_metadata.json", 'w') as f:
        json.dump(metadata, f, indent=2)

    logger.info(f"Data saved to {output_path}")


def main(args):
    logger.info(f"Generating {args.task} data with {args.num_samples} samples")

    if args.task == "classification":
        X, y = generate_classification_data(
            num_samples=args.num_samples,
            num_features=args.num_features,
            num_classes=args.num_classes,
            class_sep=args.class_sep,
            random_state=args.seed
        )
    elif args.task == "regression":
        X, y = generate_regression_data(
            num_samples=args.num_samples,
            num_features=args.num_features,
            noise=args.noise,
            random_state=args.seed
        )
    elif args.task == "sequence":
        X, y = generate_sequence_data(
            num_samples=args.num_samples,
            seq_length=args.seq_length,
            vocab_size=args.vocab_size,
            random_state=args.seed
        )
    elif args.task == "image":
        X, y = generate_image_data(
            num_samples=args.num_samples,
            image_size=args.image_size,
            num_classes=args.num_classes,
            random_state=args.seed
        )
    elif args.task == "timeseries":
        X, y = generate_time_series_data(
            num_samples=args.num_samples,
            seq_length=args.seq_length,
            noise=args.noise,
            random_state=args.seed
        )
    else:
        raise ValueError(f"Unknown task: {args.task}")

    logger.info(f"Generated X shape: {X.shape}, y shape: {y.shape}")

    # 데이터 저장
    if args.output_dir:
        save_data(X, y, args.output_dir, prefix=args.task)

    # 데이터로더 생성 테스트
    dataloader = create_dataloader(X, y, batch_size=args.batch_size)
    sample_X, sample_y = next(iter(dataloader))
    logger.info(f"Batch X shape: {sample_X.shape}, Batch y shape: {sample_y.shape}")

    logger.info("Data generation completed!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate synthetic data')
    parser.add_argument('--task', type=str, default='classification',
                       choices=['classification', 'regression', 'sequence', 'image', 'timeseries'],
                       help='Task type')
    parser.add_argument('--num_samples', type=int, default=1000,
                       help='Number of samples')
    parser.add_argument('--num_features', type=int, default=20,
                       help='Number of features')
    parser.add_argument('--num_classes', type=int, default=2,
                       help='Number of classes')
    parser.add_argument('--seq_length', type=int, default=50,
                       help='Sequence length')
    parser.add_argument('--vocab_size', type=int, default=100,
                       help='Vocabulary size')
    parser.add_argument('--image_size', type=int, default=28,
                       help='Image size')
    parser.add_argument('--class_sep', type=float, default=1.0,
                       help='Class separation')
    parser.add_argument('--noise', type=float, default=0.1,
                       help='Noise level')
    parser.add_argument('--batch_size', type=int, default=32,
                       help='Batch size')
    parser.add_argument('--output_dir', type=str, default='../data/synthetic',
                       help='Output directory')
    parser.add_argument('--seed', type=int, default=42,
                       help='Random seed')

    args = parser.parse_args()
    main(args)
