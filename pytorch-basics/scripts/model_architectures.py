"""
PyTorch 모델 아키텍처 모음

다양한 신경망 아키텍처를 구현합니다.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math


# =============================================================================
# 기본 신경망 (Basic Neural Networks)
# =============================================================================

class MLP(nn.Module):
    """다층 퍼셉트론 (Multi-Layer Perceptron)"""
    def __init__(self, input_size, hidden_sizes, output_size, dropout=0.5):
        super(MLP, self).__init__()
        layers = []
        prev_size = input_size

        for hidden_size in hidden_sizes:
            layers.extend([
                nn.Linear(prev_size, hidden_size),
                nn.BatchNorm1d(hidden_size),
                nn.ReLU(),
                nn.Dropout(dropout)
            ])
            prev_size = hidden_size

        layers.append(nn.Linear(prev_size, output_size))
        self.network = nn.Sequential(*layers)

    def forward(self, x):
        return self.network(x.view(x.size(0), -1))


# =============================================================================
# CNN 아키텍처 (Convolutional Neural Networks)
# =============================================================================

class LeNet(nn.Module):
    """LeNet-5 아키텍처"""
    def __init__(self, num_classes=10):
        super(LeNet, self).__init__()
        self.conv1 = nn.Conv2d(1, 6, kernel_size=5, padding=2)
        self.conv2 = nn.Conv2d(6, 16, kernel_size=5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, num_classes)
        self.pool = nn.AvgPool2d(2, 2)

    def forward(self, x):
        x = self.pool(torch.tanh(self.conv1(x)))
        x = self.pool(torch.tanh(self.conv2(x)))
        x = x.view(x.size(0), -1)
        x = torch.tanh(self.fc1(x))
        x = torch.tanh(self.fc2(x))
        x = self.fc3(x)
        return x


class AlexNet(nn.Module):
    """AlexNet 아키텍처 (간소화 버전)"""
    def __init__(self, num_classes=1000):
        super(AlexNet, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=11, stride=4, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.Conv2d(64, 192, kernel_size=5, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.Conv2d(192, 384, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(384, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
        )
        self.avgpool = nn.AdaptiveAvgPool2d((6, 6))
        self.classifier = nn.Sequential(
            nn.Dropout(),
            nn.Linear(256 * 6 * 6, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x


class VGGBlock(nn.Module):
    """VGG 블록"""
    def __init__(self, in_channels, out_channels, num_convs):
        super(VGGBlock, self).__init__()
        layers = []
        for i in range(num_convs):
            layers.append(nn.Conv2d(in_channels if i == 0 else out_channels,
                                   out_channels, kernel_size=3, padding=1))
            layers.append(nn.BatchNorm2d(out_channels))
            layers.append(nn.ReLU(inplace=True))
        layers.append(nn.MaxPool2d(kernel_size=2, stride=2))
        self.block = nn.Sequential(*layers)

    def forward(self, x):
        return self.block(x)


class VGG16(nn.Module):
    """VGG16 아키텍처"""
    def __init__(self, num_classes=1000):
        super(VGG16, self).__init__()
        self.features = nn.Sequential(
            VGGBlock(3, 64, 2),
            VGGBlock(64, 128, 2),
            VGGBlock(128, 256, 3),
            VGGBlock(256, 512, 3),
            VGGBlock(512, 512, 3),
        )
        self.avgpool = nn.AdaptiveAvgPool2d((7, 7))
        self.classifier = nn.Sequential(
            nn.Linear(512 * 7 * 7, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(4096, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x


class ResidualBlock(nn.Module):
    """ResNet 잔차 블록"""
    def __init__(self, in_channels, out_channels, stride=1):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3,
                               stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3,
                               stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1,
                         stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out


class ResNet18(nn.Module):
    """ResNet-18 아키텍처"""
    def __init__(self, num_classes=1000):
        super(ResNet18, self).__init__()
        self.in_channels = 64

        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        self.layer1 = self._make_layer(64, 2, stride=1)
        self.layer2 = self._make_layer(128, 2, stride=2)
        self.layer3 = self._make_layer(256, 2, stride=2)
        self.layer4 = self._make_layer(512, 2, stride=2)

        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512, num_classes)

    def _make_layer(self, out_channels, num_blocks, stride):
        layers = [ResidualBlock(self.in_channels, out_channels, stride)]
        self.in_channels = out_channels
        for _ in range(1, num_blocks):
            layers.append(ResidualBlock(out_channels, out_channels))
        return nn.Sequential(*layers)

    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.maxpool(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x


# =============================================================================
# RNN 아키텍처 (Recurrent Neural Networks)
# =============================================================================

class SimpleRNN(nn.Module):
    """간단한 RNN"""
    def __init__(self, input_size, hidden_size, output_size, num_layers=1):
        super(SimpleRNN, self).__init__()
        self.rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out, _ = self.rnn(x)
        out = self.fc(out[:, -1, :])
        return out


class LSTMClassifier(nn.Module):
    """LSTM 분류기"""
    def __init__(self, vocab_size, embed_size, hidden_size, output_size,
                 num_layers=2, dropout=0.5, bidirectional=True):
        super(LSTMClassifier, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.lstm = nn.LSTM(
            embed_size, hidden_size, num_layers,
            batch_first=True, dropout=dropout if num_layers > 1 else 0,
            bidirectional=bidirectional
        )
        self.dropout = nn.Dropout(dropout)
        direction_factor = 2 if bidirectional else 1
        self.fc = nn.Linear(hidden_size * direction_factor, output_size)

    def forward(self, x):
        embed = self.embedding(x)
        lstm_out, (hidden, cell) = self.lstm(embed)

        if self.lstm.bidirectional:
            hidden = torch.cat((hidden[-2,:,:], hidden[-1,:,:]), dim=1)
        else:
            hidden = hidden[-1,:,:]

        out = self.dropout(hidden)
        out = self.fc(out)
        return out


class GRUClassifier(nn.Module):
    """GRU 분류기"""
    def __init__(self, vocab_size, embed_size, hidden_size, output_size,
                 num_layers=2, dropout=0.5):
        super(GRUClassifier, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.gru = nn.GRU(
            embed_size, hidden_size, num_layers,
            batch_first=True, dropout=dropout if num_layers > 1 else 0
        )
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        embed = self.embedding(x)
        _, hidden = self.gru(embed)
        out = self.dropout(hidden[-1])
        out = self.fc(out)
        return out


class Seq2Seq(nn.Module):
    """Sequence-to-Sequence 모델"""
    def __init__(self, encoder_vocab_size, decoder_vocab_size, embed_size,
                 hidden_size, num_layers=2, dropout=0.5):
        super(Seq2Seq, self).__init__()

        self.encoder_embedding = nn.Embedding(encoder_vocab_size, embed_size)
        self.decoder_embedding = nn.Embedding(decoder_vocab_size, embed_size)

        self.encoder = nn.LSTM(embed_size, hidden_size, num_layers,
                               batch_first=True, dropout=dropout)
        self.decoder = nn.LSTM(embed_size, hidden_size, num_layers,
                               batch_first=True, dropout=dropout)

        self.fc = nn.Linear(hidden_size, decoder_vocab_size)
        self.dropout = nn.Dropout(dropout)

    def forward(self, src, tgt):
        # 인코딩
        src_embed = self.dropout(self.encoder_embedding(src))
        _, (hidden, cell) = self.encoder(src_embed)

        # 디코딩
        tgt_embed = self.dropout(self.decoder_embedding(tgt))
        output, _ = self.decoder(tgt_embed, (hidden, cell))
        output = self.fc(output)

        return output


# =============================================================================
# Attention 메커니즘
# =============================================================================

class Attention(nn.Module):
    """Bahdanau Attention"""
    def __init__(self, hidden_size):
        super(Attention, self).__init__()
        self.attn = nn.Linear(hidden_size * 2, hidden_size)
        self.v = nn.Linear(hidden_size, 1, bias=False)

    def forward(self, hidden, encoder_outputs):
        batch_size = encoder_outputs.size(0)
        seq_len = encoder_outputs.size(1)

        hidden = hidden.unsqueeze(1).repeat(1, seq_len, 1)
        energy = torch.tanh(self.attn(torch.cat((hidden, encoder_outputs), dim=2)))
        attention = self.v(energy).squeeze(2)

        return F.softmax(attention, dim=1)


class AttentionSeq2Seq(nn.Module):
    """Attention이 있는 Seq2Seq"""
    def __init__(self, encoder_vocab_size, decoder_vocab_size, embed_size,
                 hidden_size, num_layers=2, dropout=0.5):
        super(AttentionSeq2Seq, self).__init__()

        self.encoder_embedding = nn.Embedding(encoder_vocab_size, embed_size)
        self.decoder_embedding = nn.Embedding(decoder_vocab_size, embed_size)

        self.encoder = nn.LSTM(embed_size, hidden_size, num_layers,
                               batch_first=True, dropout=dropout, bidirectional=True)
        self.decoder = nn.LSTM(embed_size + hidden_size * 2, hidden_size, num_layers,
                               batch_first=True, dropout=dropout)

        self.attention = Attention(hidden_size)
        self.fc = nn.Linear(hidden_size * 3, decoder_vocab_size)
        self.dropout = nn.Dropout(dropout)

    def forward(self, src, tgt):
        # 인코딩
        src_embed = self.dropout(self.encoder_embedding(src))
        encoder_outputs, (hidden, cell) = self.encoder(src_embed)

        # hidden 상태 조정 (bidirectional)
        hidden = hidden.view(2, 2, -1, hidden.size(-1))
        hidden = torch.cat((hidden[0], hidden[1]), dim=-1)

        # 디코딩 (간소화된 버전)
        tgt_embed = self.dropout(self.decoder_embedding(tgt))

        outputs = []
        for t in range(tgt.size(1)):
            attn_weights = self.attention(hidden[-1], encoder_outputs)
            context = torch.bmm(attn_weights.unsqueeze(1), encoder_outputs)

            decoder_input = torch.cat((tgt_embed[:, t:t+1, :], context), dim=2)
            output, (hidden, cell) = self.decoder(decoder_input, (hidden[:2], cell[:2]))

            output = torch.cat((output, context), dim=2)
            output = self.fc(output)
            outputs.append(output)

        return torch.cat(outputs, dim=1)


# =============================================================================
# 유틸리티 함수
# =============================================================================

def count_parameters(model):
    """모델 파라미터 수 계산"""
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def get_model(model_name, **kwargs):
    """모델 이름으로 모델 가져오기"""
    models = {
        'mlp': MLP,
        'lenet': LeNet,
        'alexnet': AlexNet,
        'vgg16': VGG16,
        'resnet18': ResNet18,
        'simple_rnn': SimpleRNN,
        'lstm': LSTMClassifier,
        'gru': GRUClassifier,
        'seq2seq': Seq2Seq,
        'attention_seq2seq': AttentionSeq2Seq,
    }

    if model_name.lower() not in models:
        raise ValueError(f"Unknown model: {model_name}. Available: {list(models.keys())}")

    return models[model_name.lower()](**kwargs)


if __name__ == '__main__':
    # 테스트
    print("Testing model architectures...")

    # MLP
    mlp = MLP(784, [256, 128], 10)
    x = torch.randn(32, 1, 28, 28)
    print(f"MLP output shape: {mlp(x).shape}")
    print(f"MLP parameters: {count_parameters(mlp):,}")

    # ResNet18
    resnet = ResNet18(num_classes=10)
    x = torch.randn(4, 3, 224, 224)
    print(f"ResNet18 output shape: {resnet(x).shape}")
    print(f"ResNet18 parameters: {count_parameters(resnet):,}")

    # LSTM
    lstm = LSTMClassifier(10000, 128, 256, 2)
    x = torch.randint(0, 10000, (32, 50))
    print(f"LSTM output shape: {lstm(x).shape}")
    print(f"LSTM parameters: {count_parameters(lstm):,}")

    print("\nAll tests passed!")
