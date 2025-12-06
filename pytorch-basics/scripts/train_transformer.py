"""
Transformer 모델 학습 스크립트

Usage:
    python train_transformer.py --config ../configs/transformer_config.yaml --epochs 10
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
import math

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PositionalEncoding(nn.Module):
    """위치 인코딩"""
    def __init__(self, d_model, max_len=5000, dropout=0.1):
        super(PositionalEncoding, self).__init__()
        self.dropout = nn.Dropout(p=dropout)

        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))

        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)

        self.register_buffer('pe', pe)

    def forward(self, x):
        x = x + self.pe[:, :x.size(1), :]
        return self.dropout(x)


class MultiHeadAttention(nn.Module):
    """멀티헤드 어텐션"""
    def __init__(self, d_model, num_heads, dropout=0.1):
        super(MultiHeadAttention, self).__init__()
        assert d_model % num_heads == 0

        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)

        self.dropout = nn.Dropout(dropout)

    def scaled_dot_product_attention(self, Q, K, V, mask=None):
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)

        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)

        attn_weights = torch.softmax(scores, dim=-1)
        attn_weights = self.dropout(attn_weights)

        return torch.matmul(attn_weights, V), attn_weights

    def forward(self, query, key, value, mask=None):
        batch_size = query.size(0)

        Q = self.W_q(query).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_k(key).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_v(value).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)

        attn_output, attn_weights = self.scaled_dot_product_attention(Q, K, V, mask)

        attn_output = attn_output.transpose(1, 2).contiguous().view(batch_size, -1, self.d_model)
        output = self.W_o(attn_output)

        return output, attn_weights


class FeedForward(nn.Module):
    """피드포워드 네트워크"""
    def __init__(self, d_model, d_ff, dropout=0.1):
        super(FeedForward, self).__init__()
        self.linear1 = nn.Linear(d_model, d_ff)
        self.linear2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout)
        self.gelu = nn.GELU()

    def forward(self, x):
        return self.linear2(self.dropout(self.gelu(self.linear1(x))))


class TransformerEncoderLayer(nn.Module):
    """트랜스포머 인코더 레이어"""
    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        super(TransformerEncoderLayer, self).__init__()
        self.self_attn = MultiHeadAttention(d_model, num_heads, dropout)
        self.feed_forward = FeedForward(d_model, d_ff, dropout)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        attn_output, _ = self.self_attn(x, x, x, mask)
        x = self.norm1(x + self.dropout(attn_output))
        ff_output = self.feed_forward(x)
        x = self.norm2(x + self.dropout(ff_output))
        return x


class TransformerDecoderLayer(nn.Module):
    """트랜스포머 디코더 레이어"""
    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        super(TransformerDecoderLayer, self).__init__()
        self.self_attn = MultiHeadAttention(d_model, num_heads, dropout)
        self.cross_attn = MultiHeadAttention(d_model, num_heads, dropout)
        self.feed_forward = FeedForward(d_model, d_ff, dropout)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.norm3 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, encoder_output, src_mask=None, tgt_mask=None):
        attn_output, _ = self.self_attn(x, x, x, tgt_mask)
        x = self.norm1(x + self.dropout(attn_output))

        attn_output, _ = self.cross_attn(x, encoder_output, encoder_output, src_mask)
        x = self.norm2(x + self.dropout(attn_output))

        ff_output = self.feed_forward(x)
        x = self.norm3(x + self.dropout(ff_output))
        return x


class Transformer(nn.Module):
    """Transformer 모델"""
    def __init__(self, src_vocab_size, tgt_vocab_size, d_model=512, num_heads=8,
                 num_encoder_layers=6, num_decoder_layers=6, d_ff=2048,
                 max_seq_length=512, dropout=0.1):
        super(Transformer, self).__init__()

        self.d_model = d_model

        self.src_embedding = nn.Embedding(src_vocab_size, d_model)
        self.tgt_embedding = nn.Embedding(tgt_vocab_size, d_model)
        self.positional_encoding = PositionalEncoding(d_model, max_seq_length, dropout)

        self.encoder_layers = nn.ModuleList([
            TransformerEncoderLayer(d_model, num_heads, d_ff, dropout)
            for _ in range(num_encoder_layers)
        ])

        self.decoder_layers = nn.ModuleList([
            TransformerDecoderLayer(d_model, num_heads, d_ff, dropout)
            for _ in range(num_decoder_layers)
        ])

        self.fc_out = nn.Linear(d_model, tgt_vocab_size)
        self.dropout = nn.Dropout(dropout)

        self._init_weights()

    def _init_weights(self):
        for p in self.parameters():
            if p.dim() > 1:
                nn.init.xavier_uniform_(p)

    def generate_mask(self, src, tgt):
        src_mask = (src != 0).unsqueeze(1).unsqueeze(2)
        tgt_mask = (tgt != 0).unsqueeze(1).unsqueeze(2)

        seq_length = tgt.size(1)
        nopeak_mask = torch.triu(torch.ones(1, seq_length, seq_length), diagonal=1).bool()
        nopeak_mask = nopeak_mask.to(tgt.device)
        tgt_mask = tgt_mask & ~nopeak_mask

        return src_mask, tgt_mask

    def encode(self, src, src_mask):
        x = self.src_embedding(src) * math.sqrt(self.d_model)
        x = self.positional_encoding(x)

        for layer in self.encoder_layers:
            x = layer(x, src_mask)
        return x

    def decode(self, tgt, encoder_output, src_mask, tgt_mask):
        x = self.tgt_embedding(tgt) * math.sqrt(self.d_model)
        x = self.positional_encoding(x)

        for layer in self.decoder_layers:
            x = layer(x, encoder_output, src_mask, tgt_mask)
        return x

    def forward(self, src, tgt):
        src_mask, tgt_mask = self.generate_mask(src, tgt)

        encoder_output = self.encode(src, src_mask)
        decoder_output = self.decode(tgt, encoder_output, src_mask, tgt_mask)
        output = self.fc_out(decoder_output)

        return output


class TranslationDataset(Dataset):
    """번역 데이터셋 (데모용)"""
    def __init__(self, num_samples=1000, max_length=20, vocab_size=1000):
        self.num_samples = num_samples
        self.max_length = max_length
        self.vocab_size = vocab_size

        # 더미 데이터 생성
        self.src_data = torch.randint(1, vocab_size, (num_samples, max_length))
        self.tgt_data = torch.randint(1, vocab_size, (num_samples, max_length))

        # 패딩 추가
        for i in range(num_samples):
            pad_len = torch.randint(0, max_length // 2, (1,)).item()
            self.src_data[i, -pad_len:] = 0
            self.tgt_data[i, -pad_len:] = 0

    def __len__(self):
        return self.num_samples

    def __getitem__(self, idx):
        return self.src_data[idx], self.tgt_data[idx]


def train_epoch(model, dataloader, criterion, optimizer, device, clip=1.0):
    """한 에폭 학습"""
    model.train()
    total_loss = 0

    pbar = tqdm(dataloader, desc='Training')
    for src, tgt in pbar:
        src, tgt = src.to(device), tgt.to(device)

        tgt_input = tgt[:, :-1]
        tgt_output = tgt[:, 1:]

        optimizer.zero_grad()
        output = model(src, tgt_input)

        loss = criterion(output.reshape(-1, output.size(-1)), tgt_output.reshape(-1))
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
    src_vocab_size = args.src_vocab_size or config.get('src_vocab_size', 10000)
    tgt_vocab_size = args.tgt_vocab_size or config.get('tgt_vocab_size', 10000)
    d_model = config.get('d_model', 512)
    num_heads = config.get('num_heads', 8)
    num_encoder_layers = config.get('num_encoder_layers', 6)
    num_decoder_layers = config.get('num_decoder_layers', 6)
    d_ff = config.get('d_ff', 2048)
    max_seq_length = args.max_seq_length or config.get('max_seq_length', 512)
    dropout = config.get('dropout', 0.1)
    batch_size = args.batch_size or config.get('batch_size', 32)
    learning_rate = args.learning_rate or config.get('learning_rate', 0.0001)
    epochs = args.epochs or config.get('epochs', 10)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    logger.info(f"Using device: {device}")

    # 데이터셋 (데모용)
    logger.info("Creating demo translation dataset...")
    train_dataset = TranslationDataset(num_samples=5000, max_length=30, vocab_size=src_vocab_size)
    val_dataset = TranslationDataset(num_samples=500, max_length=30, vocab_size=src_vocab_size)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size)

    # 모델 생성
    model = Transformer(
        src_vocab_size=src_vocab_size,
        tgt_vocab_size=tgt_vocab_size,
        d_model=d_model,
        num_heads=num_heads,
        num_encoder_layers=num_encoder_layers,
        num_decoder_layers=num_decoder_layers,
        d_ff=d_ff,
        max_seq_length=max_seq_length,
        dropout=dropout
    ).to(device)

    total_params = sum(p.numel() for p in model.parameters())
    logger.info(f"Total parameters: {total_params:,}")

    # 손실 함수 및 옵티마이저
    criterion = nn.CrossEntropyLoss(ignore_index=0)
    optimizer = optim.Adam(model.parameters(), lr=learning_rate, betas=(0.9, 0.98), eps=1e-9)

    # 학습률 스케줄러 (Warmup)
    warmup_steps = 4000
    def lr_lambda(step):
        step = max(step, 1)
        return min(step ** (-0.5), step * warmup_steps ** (-1.5))

    scheduler = optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)

    # 학습
    best_loss = float('inf')
    for epoch in range(1, epochs + 1):
        logger.info(f"\nEpoch {epoch}/{epochs}")

        train_loss = train_epoch(model, train_loader, criterion, optimizer, device)
        logger.info(f"Train Loss: {train_loss:.4f}")

        # 검증
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for src, tgt in val_loader:
                src, tgt = src.to(device), tgt.to(device)
                tgt_input = tgt[:, :-1]
                tgt_output = tgt[:, 1:]
                output = model(src, tgt_input)
                loss = criterion(output.reshape(-1, output.size(-1)), tgt_output.reshape(-1))
                val_loss += loss.item()

        val_loss /= len(val_loader)
        logger.info(f"Val Loss: {val_loss:.4f}")

        scheduler.step()

        # 모델 저장
        if val_loss < best_loss:
            best_loss = val_loss
            save_path = Path(args.save_dir) / 'transformer_best.pth'
            save_path.parent.mkdir(parents=True, exist_ok=True)
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': best_loss,
                'config': {
                    'd_model': d_model,
                    'num_heads': num_heads,
                    'num_encoder_layers': num_encoder_layers,
                    'num_decoder_layers': num_decoder_layers,
                }
            }, save_path)
            logger.info(f"Model saved: {save_path}")

    logger.info(f"\nTraining completed! Best validation loss: {best_loss:.4f}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train Transformer model')
    parser.add_argument('--config', type=str, help='Path to config file')
    parser.add_argument('--save_dir', type=str, default='../checkpoints', help='Save directory')
    parser.add_argument('--src_vocab_size', type=int, help='Source vocabulary size')
    parser.add_argument('--tgt_vocab_size', type=int, help='Target vocabulary size')
    parser.add_argument('--max_seq_length', type=int, help='Maximum sequence length')
    parser.add_argument('--batch_size', type=int, help='Batch size')
    parser.add_argument('--learning_rate', type=float, help='Learning rate')
    parser.add_argument('--epochs', type=int, help='Number of epochs')

    args = parser.parse_args()
    main(args)
