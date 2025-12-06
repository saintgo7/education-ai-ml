"""
RNN/LSTM 텍스트 생성 학습 스크립트

Usage:
    python train_rnn.py --config ../configs/rnn_config.yaml --epochs 20
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import argparse
import yaml
from pathlib import Path
import logging
from tqdm import tqdm
import numpy as np
import string

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class CharDataset(Dataset):
    """문자 단위 데이터셋"""
    def __init__(self, text, seq_length):
        self.text = text
        self.seq_length = seq_length
        self.chars = sorted(list(set(text)))
        self.char_to_idx = {ch: i for i, ch in enumerate(self.chars)}
        self.idx_to_char = {i: ch for i, ch in enumerate(self.chars)}
        self.vocab_size = len(self.chars)

    def __len__(self):
        return len(self.text) - self.seq_length

    def __getitem__(self, idx):
        sequence = self.text[idx:idx + self.seq_length]
        target = self.text[idx + 1:idx + self.seq_length + 1]

        x = torch.tensor([self.char_to_idx[ch] for ch in sequence], dtype=torch.long)
        y = torch.tensor([self.char_to_idx[ch] for ch in target], dtype=torch.long)
        return x, y


class CharRNN(nn.Module):
    """문자 단위 RNN 모델"""
    def __init__(self, vocab_size, embed_size, hidden_size, num_layers, dropout=0.5):
        super(CharRNN, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.rnn = nn.LSTM(
            embed_size, hidden_size, num_layers,
            batch_first=True, dropout=dropout if num_layers > 1 else 0
        )
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_size, vocab_size)

    def forward(self, x, hidden=None):
        embed = self.embedding(x)
        output, hidden = self.rnn(embed, hidden)
        output = self.dropout(output)
        output = self.fc(output)
        return output, hidden

    def init_hidden(self, batch_size, device):
        h0 = torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device)
        c0 = torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device)
        return (h0, c0)


class CharGRU(nn.Module):
    """문자 단위 GRU 모델"""
    def __init__(self, vocab_size, embed_size, hidden_size, num_layers, dropout=0.5):
        super(CharGRU, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.gru = nn.GRU(
            embed_size, hidden_size, num_layers,
            batch_first=True, dropout=dropout if num_layers > 1 else 0
        )
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_size, vocab_size)

    def forward(self, x, hidden=None):
        embed = self.embedding(x)
        output, hidden = self.gru(embed, hidden)
        output = self.dropout(output)
        output = self.fc(output)
        return output, hidden

    def init_hidden(self, batch_size, device):
        return torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device)


def generate_text(model, dataset, seed_text, length, device, temperature=1.0):
    """텍스트 생성"""
    model.eval()

    chars = [dataset.char_to_idx.get(ch, 0) for ch in seed_text]
    input_seq = torch.tensor([chars], dtype=torch.long).to(device)

    generated = seed_text
    hidden = None

    with torch.no_grad():
        for _ in range(length):
            output, hidden = model(input_seq, hidden)
            output = output[:, -1, :] / temperature
            probs = torch.softmax(output, dim=-1)
            next_char_idx = torch.multinomial(probs, 1).item()
            next_char = dataset.idx_to_char[next_char_idx]
            generated += next_char
            input_seq = torch.tensor([[next_char_idx]], dtype=torch.long).to(device)

    return generated


def train_epoch(model, dataloader, criterion, optimizer, device, clip=1.0):
    """한 에폭 학습"""
    model.train()
    total_loss = 0

    pbar = tqdm(dataloader, desc='Training')
    for batch_x, batch_y in pbar:
        batch_x, batch_y = batch_x.to(device), batch_y.to(device)

        optimizer.zero_grad()
        output, _ = model(batch_x)
        loss = criterion(output.view(-1, output.size(-1)), batch_y.view(-1))
        loss.backward()

        nn.utils.clip_grad_norm_(model.parameters(), clip)
        optimizer.step()

        total_loss += loss.item()
        pbar.set_postfix({'loss': loss.item()})

    return total_loss / len(dataloader)


def main(args):
    # 설정 로드
    if args.config and Path(args.config).exists():
        with open(args.config, 'r') as f:
            config = yaml.safe_load(f)
    else:
        config = {}

    # 하이퍼파라미터
    seq_length = args.seq_length or config.get('seq_length', 100)
    batch_size = args.batch_size or config.get('batch_size', 64)
    embed_size = config.get('embed_size', 128)
    hidden_size = config.get('hidden_size', 256)
    num_layers = config.get('num_layers', 2)
    dropout = config.get('dropout', 0.5)
    learning_rate = args.learning_rate or config.get('learning_rate', 0.001)
    epochs = args.epochs or config.get('epochs', 20)
    model_type = args.model or config.get('model', 'lstm')

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    logger.info(f"Using device: {device}")

    # 텍스트 로드
    if args.text_file and Path(args.text_file).exists():
        with open(args.text_file, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        # 샘플 텍스트 생성
        logger.info("Using sample text for demonstration")
        text = """To be, or not to be, that is the question:
Whether 'tis nobler in the mind to suffer
The slings and arrows of outrageous fortune,
Or to take arms against a sea of troubles
And by opposing end them. To die—to sleep,
No more; and by a sleep to say we end
The heart-ache and the thousand natural shocks
That flesh is heir to: 'tis a consummation
Devoutly to be wish'd. To die, to sleep;
To sleep, perchance to dream—ay, there's the rub:
For in that sleep of death what dreams may come,
When we have shuffled off this mortal coil,
Must give us pause—there's the respect
That makes calamity of so long life.""" * 10

    logger.info(f"Text length: {len(text)} characters")

    # 데이터셋 생성
    dataset = CharDataset(text, seq_length)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=2)

    logger.info(f"Vocabulary size: {dataset.vocab_size}")
    logger.info(f"Number of sequences: {len(dataset)}")

    # 모델 생성
    if model_type == 'gru':
        model = CharGRU(dataset.vocab_size, embed_size, hidden_size, num_layers, dropout)
    else:
        model = CharRNN(dataset.vocab_size, embed_size, hidden_size, num_layers, dropout)

    model = model.to(device)
    logger.info(f"Model type: {model_type.upper()}")
    logger.info(f"Total parameters: {sum(p.numel() for p in model.parameters()):,}")

    # 손실 함수 및 옵티마이저
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=3, factor=0.5)

    # 학습
    best_loss = float('inf')
    for epoch in range(1, epochs + 1):
        logger.info(f"\nEpoch {epoch}/{epochs}")

        train_loss = train_epoch(model, dataloader, criterion, optimizer, device)
        logger.info(f"Train Loss: {train_loss:.4f}")

        scheduler.step(train_loss)

        # 샘플 생성
        if epoch % 5 == 0:
            sample = generate_text(model, dataset, "To be", 200, device, temperature=0.8)
            logger.info(f"Sample:\n{sample}\n")

        # 모델 저장
        if train_loss < best_loss:
            best_loss = train_loss
            save_path = Path(args.save_dir) / f'{model_type}_best.pth'
            save_path.parent.mkdir(parents=True, exist_ok=True)
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': best_loss,
                'vocab_size': dataset.vocab_size,
                'char_to_idx': dataset.char_to_idx,
                'idx_to_char': dataset.idx_to_char,
            }, save_path)
            logger.info(f"Model saved: {save_path}")

    # 최종 텍스트 생성
    logger.info("\nFinal generated samples:")
    for temp in [0.5, 0.8, 1.0, 1.2]:
        sample = generate_text(model, dataset, "To be", 300, device, temperature=temp)
        logger.info(f"\nTemperature {temp}:\n{sample}")

    logger.info(f"\nTraining completed! Best loss: {best_loss:.4f}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train RNN/LSTM for text generation')
    parser.add_argument('--config', type=str, help='Path to config file')
    parser.add_argument('--text_file', type=str, help='Path to text file')
    parser.add_argument('--save_dir', type=str, default='../checkpoints', help='Save directory')
    parser.add_argument('--seq_length', type=int, help='Sequence length')
    parser.add_argument('--batch_size', type=int, help='Batch size')
    parser.add_argument('--learning_rate', type=float, help='Learning rate')
    parser.add_argument('--epochs', type=int, help='Number of epochs')
    parser.add_argument('--model', type=str, choices=['lstm', 'gru'], help='Model type')

    args = parser.parse_args()
    main(args)
