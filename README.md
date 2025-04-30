# 🐺 Wolftrain

**Local LoRA Fine-Tuning, Evolved.**

Wolftrain is a lightweight desktop application that empowers developers to fine-tune language models locally — using their own datasets, without cloud dependencies.

Built for privacy, speed, and control, Wolftrain supports text and CSV dataset formats, GPU acceleration, and private model saving — all from a simple GUI.

---

## 🚀 Project Status

🔧 **Beta Preview**  
Wolftrain is now feature-complete for its first open-source release.  
More capabilities and polish are still evolving, but the core loop is solid.

---

## 🎯 Features

- ✅ Fine-tune Hugging Face models locally
- ✅ GPU and CPU support
- ✅ Train on `.txt` or `.csv` datasets
- ✅ Dataset validation with clear errors
- ✅ Dataset preview popup (view first 5 rows before training)
- ✅ Live training loss tracking (shown in console)
- ✅ Set training settings (epochs, batch size, learning rate)
- ✅ Local model saving after training
- ✅ Local test script to compare base vs. fine-tuned output
- ✅ Clear training console between runs

---

## 🧠 Planned Features

- CSV column selector (for multi-column training sets)
- Hugging Face model browser (search + download from UI)
- Adapter-only saving for smaller outputs
- Export support for Ollama-compatible formats

---

## 📋 Quickstart


# 1. Clone the repo
git clone https://github.com/yourusername/wolftrain.git
cd wolftrain

# 2. Set up a virtual environment
python -m venv venv
.\venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run Wolftrain
python main.py
