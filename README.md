# 🐺 Wolftrain

**Local LoRA Fine-Tuning, Evolved.**  
Part of the [Wolflow](https://wolflow.ai) ecosystem • Built by [Christopher Messina](https://github.com/CLewisMessina)

> Now with a modern, streamlined interface and GPU acceleration support.

---

## ✨ What is Wolftrain?

Wolftrain is a lightweight desktop application that empowers developers to fine-tune language models locally — using their own datasets, without cloud dependencies.

Built for privacy, speed, and control, it bridges the gap between raw data and custom AI with just a few clicks.

> **No complex setup. No API costs. Just results.**

---

## 📦 Key Features

- 🧠 **Local model fine-tuning** - Run entirely on your own hardware
- 🔥 **GPU acceleration** - Automatic CUDA detection and utilization
- 📊 **Multiple dataset formats** - Support for `.txt` and `.csv` training files
- ✂️ **LoRA adaptation** - Efficient parameter updates with minimal resources
- 🔍 **Live training metrics** - Real-time loss tracking and progress updates
- 📈 **Model comparison tool** - Compare base vs. fine-tuned outputs
- 🖥️ **Simple interface** - Clean, card-based design with minimal workflow
- ❌ **Private by design** - Fully local processing with no cloud dependencies

---

## 🖥️ Screenshots

![Wolftrain Interface](https://github.com/CLewisMessina/wolftrain/blob/main/assets/screenshots/wolftrain-UI.png)


![Wolftrain Training CLI Output](https://github.com/CLewisMessina/wolftrain/blob/main/assets/screenshots/training-cli.png)

---

## 🥚 Why Use Wolftrain?

| Use Case | Example |
|----------|---------|
| Create specialized assistants | Fine-tune models on your documentation or knowledge base |
| Build domain experts | Train models on academic papers or technical content |
| Develop creative writing tools | Adapt models to specific writing styles or genres |
| Personalize responses | Train on conversation logs to match your communication style |
| Educational resources | Create subject-specific tutors from textbook content |

---

## 🚀 Getting Started

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/CLewisMessina/wolftrain.git
cd wolftrain

# 2. Set up your virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install GPU-accelerated PyTorch manually (for CUDA support)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### Running Wolftrain

```bash
python main.py
```

### Workflow

1. **Select Model** - Choose a base Hugging Face model to fine-tune
2. **Select Dataset** - Upload your training data (TXT or CSV format)
3. **Configure** - Set epochs, batch size, and learning rate
4. **Train** - Launch training with live progress updates
5. **Test** - Use comparison tools to evaluate your fine-tuned model

---

## 📁 Supported Formats

- **Models:** Any Hugging Face causal language model
- **Datasets:** 
  - `.txt` (one prompt/example per line)
  - `.csv` (single 'text' column with fully quoted content)
- **Output:** Full model directory compatible with Hugging Face Transformers

---

## ⚙️ Requirements

- Python 3.10+
- Key packages:
  - `ttkbootstrap` - Modern UI components
  - `transformers` - Hugging Face Transformers library
  - `peft` - Parameter-Efficient Fine-Tuning library
  - `datasets` - Dataset handling utilities
  - `torch` - PyTorch deep learning framework (install separately for GPU support)

---

## 🗐 Roadmap

- [x] Multiple dataset format support
- [x] Live training metrics
- [x] GPU acceleration
- [ ] CSV column selector for multi-column datasets
- [ ] Hugging Face model browser (search + download from UI)
- [ ] Adapter-only saving for smaller outputs
- [ ] Export support for Ollama-compatible formats
- [ ] Training visualization with interactive charts
- [ ] Batch inferencing and evaluation

---

## 🧙‍♂️ Part of the Wolflow Ecosystem

- [🐺 Wolfkit](https://github.com/CLewisMessina/wolfkit) – Test harness for LLM-generated code
- [✧ Wolfscribe](https://github.com/CLewisMessina/wolfscribe) – Book to dataset processor
- [📈 Wolftrack](https://github.com/CLewisMessina) – Token usage tracking *(coming soon)*

---

## 🤖 License

Creative Commons CC BY-NC 4.0  
No cloud. No gatekeeping. Just tools.

---

_Your data. Your models. Your control. Wolftrain makes local AI training accessible._