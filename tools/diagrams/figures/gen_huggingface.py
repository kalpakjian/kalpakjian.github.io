# -*- coding: utf-8 -*-
"""huggingface-notes: 4 ASCII blocks -> SVG.

  art#1  §20.3 子詞分詞的兩條路（top-down / bottom-up）
  art#2  §25.2 PEFT 家族（Adapter 是概念，LoRA / QLoRA 是實作）
  art#3  §32.2 model-repo/ 裡面有什麼
  art#4  §39.2 torchaudio CUDA 版本不符的完整根因鏈
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                     # same dir (figures/)
sys.path.insert(0, os.path.dirname(_HERE))    # parent dir (svglib.py)
from svglib import Svg, C, MUT, TXT, CARD2, MONO  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RAIL = "#30363d"

SUBWORD = [
    (0, "由上而下（top-down，先大後小）", "teal"),
    (1, "Unigram language model（SentencePiece 的一種模式）", None),
    (0, "由下而上（bottom-up，先小後大）", "blue"),
    (1, "BPE　←　貪婪，純計數", None),
    (1, "WordPiece　←　貪婪變體，用似然評分", None),
]

PEFT = [
    (0, "Adapter　——　抽象概念：在模型裡插入小可訓練模組", "violet"),
    (1, "LoRA　：用兩個低秩矩陣 A、B 當作「adapter」", None),
    (1, "QLoRA　：LoRA ＋ 4-bit 量化", None),
]

REPO = [
    ("README.md", "Model Card：Intended use／Limitations／Evaluation／Training data", "amber"),
    ("config.json", "模型架構設定", "teal"),
    ("model.safetensors", "權重本體（就是那幾 GB）", "blue"),
    ("tokenizer_config.json", "分詞器設定", "violet"),
    ("vocab.json", "詞表（token ↔ id）", "green"),
]

CHAIN = [
    ("torchaudio/_extension/utils.py:124",
     "_check_cuda_version() → RuntimeError: PyTorch 與 TorchAudio 的 CUDA 版本不同", "amber"),
    ("transformers/audio_utils.py:58",
     "if is_torchaudio_available():　import torchaudio　← 這一行炸了", "blue"),
    ("transformers/processing_utils.py → modeling_layers.py",
     "→ models/bloom/modeling_bloom.py:26　from ...modeling_layers import ...", "violet"),
    ("transformers 的 lazy-import",
     "對 BloomPreTrainedModel 失敗", "teal"),
    ("peft/utils/constants.py:16",
     "from transformers import BloomPreTrainedModel　← peft 死在這裡", "rose"),
]


def outline_panel(s, x, y, w, h, root, rows, pitch=36, top=84):
    """Bordered panel: root line + a rail/indent tree supporting 3 levels."""
    s.rect(x, y, w, h, fill=CARD2, stroke="#2a6f68", rx=14)
    s.text(x + 28, y + 42, root, 18, TXT, "700")
    rail, sub, sub2 = x + 52, x + 108, x + 164
    ys = [y + top + i * pitch for i in range(len(rows))]
    s.line(rail, ys[0] - 6, rail, ys[-1] - 6, RAIL, 1.5)
    for i, (lvl, txt, stage) in enumerate(rows):
        sy = ys[i] - 6
        if lvl == 0:
            s.line(rail, sy, rail + 14, sy, RAIL, 1.5)
            s.text(rail + 20, ys[i], txt, 13.5, C[stage] if stage else TXT, "700")
        elif lvl == 1:
            s.line(sub, ys[i - 1] - 6 + 10, sub, sy, RAIL, 1.5)
            s.line(sub, sy, sub + 14, sy, RAIL, 1.5)
            s.text(sub + 20, ys[i], txt, 12.5, TXT)
        else:
            s.line(sub2, ys[i - 1] - 6 + 10, sub2, sy, RAIL, 1.5)
            s.line(sub2, sy, sub2 + 14, sy, RAIL, 1.5)
            s.text(sub2 + 20, ys[i], txt, 12, MUT)


def fig_subword(s):
    outline_panel(s, 48, 106, 704, 254, "子詞分詞（subword tokenization）", SUBWORD)
    s.text(48, 396, "兩條路的差別在「合併的方向」：Unigram 從大往小拆，"
                    "BPE／WordPiece 從小往大併。", 13, MUT)


def fig_peft(s):
    outline_panel(s, 48, 106, 704, 182, "PEFT（參數高效微調）", PEFT)
    s.text(48, 322, "考點：Adapter 是一個概念，LoRA 與 QLoRA 是它的具體實作。", 13, MUT)


def fig_repo(s):
    s.rect(48, 106, 804, 254, fill=CARD2, stroke="#2a6f68", rx=14)
    s.text(76, 148, "model-repo/", 18, TXT, "700", "start", MONO)
    s.text(250, 148, "←　Hub 上的一個模型資料夾（repo）", 12.5, MUT)
    ys = [190 + i * 36 for i in range(len(REPO))]
    s.line(100, ys[0] - 6, 100, ys[-1] - 6, RAIL, 1.5)
    for i, (fn, desc, stage) in enumerate(REPO):
        s.line(100, ys[i] - 6, 114, ys[i] - 6, RAIL, 1.5)
        s.text(120, ys[i], fn, 12.5, C[stage], "700", "start", MONO)
        s.text(340, ys[i], "—　" + desc, 11.5, MUT)
    s.text(48, 396, "repo 就是一個資料夾：README.md 是 Model Card，其餘是設定與權重本體。", 13, MUT)

def fig_layers(s):
    """§5.2 資料流向：三層之間用哪些 API 串起來。"""
    layers = [
        ("①  Hugging Face Hub", "靜態資產：模型／資料集／Spaces", "teal"),
        ("②  Core Libraries", "在你的程式裡：transformers／datasets／peft", "blue"),
        ("③  Inference & Deployment", "給別人用：accelerate／optimum／TGI／Endpoints", "violet"),
    ]
    calls = ["from_pretrained() / load_dataset()",
             "LoraConfig() / Trainer / save_pretrained()"]
    for i, (label, sub, stage) in enumerate(layers):
        y = 140 + i * 100
        s.box(200, y, 500, 64, label, sub, stage, tsize=14.5)
        if i < len(calls):
            s.arrow(450, y + 64, 450, y + 98)
            s.text(462, y + 88, calls[i], 11.5, MUT)
    s.text(48, 444, "三層之間只有兩個動作：把資產拿進來（from_pretrained）、"
                    "把結果送出去（save_pretrained / 部署）。", 13, MUT)


def fig_cuda(s):
    s.rect(48, 110, 904, 110, fill=CARD2, stroke=C["amber"] + "66", rx=12)
    s.text(76, 144, "觸發點：兩套 CUDA 版本不一致", 14.5, C["amber"], "700")
    s.text(76, 174, "torch　　　 2.14.1+cu132　（CUDA 13.2）", 12.5, TXT, "normal", "start", MONO)
    s.text(76, 198, "torchaudio　2.11.0+cu130　（CUDA 13.0）　← 版本不符", 12.5, TXT,
           "normal", "start", MONO)

    y, prev = 250, 220
    for i, (path, detail, stage) in enumerate(CHAIN, 1):
        s.arrow(80, prev, 80, y - 2, RAIL)
        s.rect(48, y, 904, 72, fill=CARD2, stroke=C[stage] + "66", rx=12)
        s.badge(80, y + 36, str(i), C[stage], r=15, size=13)
        s.text(108, y + 30, path, 12, C[stage], "700", "start", MONO)
        s.text(108, y + 54, detail, 11.5, MUT)
        prev = y + 72
        y = prev + 20

    s.rect(48, 730, 904, 76, fill="#0d1117", stroke=C["rose"] + "66", rx=12)
    s.text(76, 762, "表面症狀（錯誤訊息完全指錯方向）", 13.5, C["rose"], "700")
    s.text(76, 788, "ModuleNotFoundError: Could not import module 'BloomPreTrainedModel'.",
           12, MUT, "normal", "start", MONO)

    s.text(48, 840, "根因是「torch 與 torchaudio 的 CUDA 版本不一致」；peft 只是最後一個受害者。",
           13, MUT)


FIGS = [
    ("hf-subword", "huggingface-notes", 1, 800, 420,
     "子詞分詞的兩條路", "先大後小（Unigram）vs 先小後大（BPE / WordPiece）", fig_subword,
     "圖 44：子詞分詞的兩條路——由上而下的 Unigram language model，"
     "與由下而上的 BPE（貪婪、純計數）和 WordPiece（貪婪變體、用似然評分）。｜手繪 SVG 圖表"),
    ("hf-peft", "huggingface-notes", 2, 800, 340,
     "PEFT 家族：概念與實作", "Adapter 是概念，LoRA / QLoRA 是它的實作", fig_peft,
     "圖 45：PEFT 家族——Adapter 是「在模型裡插入小可訓練模組」的抽象概念，"
     "LoRA（兩個低秩矩陣 A、B）與 QLoRA（LoRA ＋ 4-bit 量化）是具體實作。｜手繪 SVG 圖表"),
    ("hf-model-repo", "huggingface-notes", 3, 900, 420,
     "model-repo/ 裡面有什麼", "Hub 上一個模型資料夾的標準長相", fig_repo,
     "圖 46：model-repo/ 的內容——README.md 就是 Model Card，其餘是架構設定、權重本體、"
     "分詞器設定與詞表。｜手繪 SVG 圖表"),
    ("hf-cuda-chain", "huggingface-notes", 4, 1000, 870,
     "torchaudio 版本不符的根因鏈", "從 CUDA 版本不一致，一路炸到 peft 匯入失敗", fig_cuda,
     "圖 47：完整根因鏈——torch 與 torchaudio 的 CUDA 版本不一致，"
     "讓 transformers 的 lazy-import 對 BloomPreTrainedModel 失敗，"
     "最後 peft 匯入時報出完全指錯方向的 ModuleNotFoundError。｜手繪 SVG 圖表"),
    # §5.2 的資料流向圖只有 2 個框線字元，inventory.py 的 art# 看不到它，
    # 所以這張由 _work/diagrams/embed_hf_layers.py 直接定點替換（art 記為 0）。
    ("hf-layers", "huggingface-notes", 0, 900, 470,
     "三層生態的資料流向", "從 Hub 拿資產 → 在程式裡用 → 部署給別人用", fig_layers,
     "圖 48：三層生態的資料流向——① Hub（靜態資產）用 from_pretrained()／load_dataset() "
     "進到 ② Core Libraries（在你的程式裡），再用 save_pretrained()／Trainer 交棒給 "
     "③ Inference & Deployment。｜手繪 SVG 圖表"),
]

if __name__ == "__main__":
    for slug, note, art, w, h, title, sub, fn, cap in FIGS:
        s = Svg(w, h, title, title, sub)
        fn(s)
        bad = s.check()
        s.save(os.path.join(HERE, slug + ".svg"),
               os.path.join(HERE, "_m_" + slug + ".html"))
        print("wrote %-30s %-18s art#%d %dx%d  %s"
              % (slug + ".svg", note, art, w, h,
                 "OK" if not bad else "COLLISION x%d" % len(bad)))
        for seg, box in bad:
            print("    line %s runs through text box %s" % (seg, box))
