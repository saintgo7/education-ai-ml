"""
Gradio 텍스트 생성 데모

Usage:
    python text_generator_demo.py
"""

import gradio as gr
import torch
import torch.nn as nn
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CharRNN(nn.Module):
    """문자 단위 RNN 모델"""
    def __init__(self, vocab_size, embed_size=128, hidden_size=256, num_layers=2):
        super(CharRNN, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.rnn = nn.LSTM(embed_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, vocab_size)

    def forward(self, x, hidden=None):
        embed = self.embedding(x)
        output, hidden = self.rnn(embed, hidden)
        output = self.fc(output)
        return output, hidden


# 샘플 텍스트로 간단한 모델 생성
SAMPLE_TEXT = """To be, or not to be, that is the question:
Whether 'tis nobler in the mind to suffer
The slings and arrows of outrageous fortune,
Or to take arms against a sea of troubles
And by opposing end them. To die—to sleep,
No more; and by a sleep to say we end
The heart-ache and the thousand natural shocks
That flesh is heir to: 'tis a consummation
Devoutly to be wish'd. To die, to sleep;
To sleep, perchance to dream—ay, there's the rub."""

chars = sorted(list(set(SAMPLE_TEXT)))
char_to_idx = {ch: i for i, ch in enumerate(chars)}
idx_to_char = {i: ch for i, ch in enumerate(chars)}
vocab_size = len(chars)

# 모델 초기화
model = CharRNN(vocab_size)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
model.eval()


def generate_text(seed_text: str, length: int, temperature: float) -> str:
    """텍스트 생성 함수"""
    if not seed_text:
        seed_text = "To be"

    # 시드 텍스트 처리
    chars_in_seed = [char_to_idx.get(ch, 0) for ch in seed_text if ch in char_to_idx]
    if not chars_in_seed:
        chars_in_seed = [0]

    input_seq = torch.tensor([chars_in_seed], dtype=torch.long).to(device)

    generated = seed_text
    hidden = None

    with torch.no_grad():
        for _ in range(int(length)):
            output, hidden = model(input_seq, hidden)
            output = output[:, -1, :] / max(temperature, 0.1)
            probs = torch.softmax(output, dim=-1)
            next_char_idx = torch.multinomial(probs, 1).item()
            next_char = idx_to_char.get(next_char_idx, ' ')
            generated += next_char
            input_seq = torch.tensor([[next_char_idx]], dtype=torch.long).to(device)

    return generated


def generate_with_multiple_temps(seed_text: str, length: int) -> str:
    """여러 온도로 텍스트 생성"""
    results = []
    for temp in [0.5, 0.8, 1.0, 1.2]:
        text = generate_text(seed_text, length, temp)
        results.append(f"**Temperature {temp}:**\n{text}\n")
    return "\n".join(results)


# Gradio 인터페이스
with gr.Blocks(title="텍스트 생성기", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🔤 RNN 텍스트 생성기

    이 데모는 RNN/LSTM을 사용하여 텍스트를 생성합니다.
    시드 텍스트를 입력하고 생성할 길이와 온도를 조절해보세요.

    **온도 (Temperature):**
    - 낮은 값 (0.5): 더 예측 가능하고 일관된 텍스트
    - 높은 값 (1.2): 더 창의적이고 다양한 텍스트
    """)

    with gr.Row():
        with gr.Column():
            seed_input = gr.Textbox(
                label="시드 텍스트",
                placeholder="텍스트 시작 부분을 입력하세요...",
                value="To be"
            )
            length_slider = gr.Slider(
                minimum=50,
                maximum=500,
                value=200,
                step=10,
                label="생성할 문자 수"
            )
            temp_slider = gr.Slider(
                minimum=0.1,
                maximum=2.0,
                value=0.8,
                step=0.1,
                label="온도 (Temperature)"
            )
            generate_btn = gr.Button("🚀 텍스트 생성", variant="primary")
            compare_btn = gr.Button("📊 온도 비교")

        with gr.Column():
            output_text = gr.Textbox(
                label="생성된 텍스트",
                lines=15,
                max_lines=20
            )

    generate_btn.click(
        fn=generate_text,
        inputs=[seed_input, length_slider, temp_slider],
        outputs=output_text
    )

    compare_btn.click(
        fn=generate_with_multiple_temps,
        inputs=[seed_input, length_slider],
        outputs=output_text
    )

    gr.Markdown("""
    ## 사용 방법

    1. **시드 텍스트**: 생성을 시작할 텍스트를 입력합니다
    2. **생성할 문자 수**: 생성할 텍스트의 길이를 선택합니다
    3. **온도**: 텍스트의 창의성 수준을 조절합니다
    4. **텍스트 생성** 버튼을 클릭하여 결과를 확인합니다

    ## 모델 정보

    - **아키텍처**: LSTM (Long Short-Term Memory)
    - **학습 데이터**: 셰익스피어 텍스트
    - **어휘 크기**: {vocab_size} 문자
    """.format(vocab_size=vocab_size))


if __name__ == "__main__":
    demo.launch(share=False, server_name="0.0.0.0", server_port=7860)
