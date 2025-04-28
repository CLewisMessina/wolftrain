# 🐺 Wolftrain

**Local LoRA Fine-Tuning, Evolved.**

Wolftrain is a lightweight desktop application that empowers developers to fine-tune language models locally — using their own datasets, without cloud dependencies.

Built for privacy, speed, and control, Wolftrain currently supports text and CSV dataset formats, GPU acceleration, and private model saving — with more features rapidly evolving.

---

## 🚀 Project Status

⚡ **Active Alpha Development**  
This is an early working version of Wolftrain.  
It can already fine-tune models locally, but feature enhancements and polish are ongoing.

Follow the repo for continuous improvements!

---

## 🎯 Features (Current)

- ✅ Fine-tune Hugging Face models locally
- ✅ GPU and CPU support
- ✅ Train on `.txt` or `.csv` datasets
- ✅ Automatic dataset validation (prevent training crashes)
- ✅ Model saving for private use
- ✅ Local test harness to evaluate fine-tuned models

---

## 🧠 Features Coming Soon

- Dataset preview and column selection for CSVs
- Live training loss tracking
- Advanced training settings (batch size, learning rate, epochs)
- Adapter-only saving and model merging
- Local model browser and downloader

---

## 📋 Quickstart

```bash
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
```

---

## 📂 Project Structure

```plaintext
wolftrain/
├── assets/           # App icons and images
├── datasets/         # User datasets (TXT or CSV)
├── training/         # Training logic (LoRA fine-tuning engine)
├── ui/               # GUI components
├── main.py           # App launcher
├── controller.py     # Backend coordination
├── requirements.txt  # Dependencies
├── README.md         # Project overview (this file)
└── CHANGELOG.md      # Version history
```

---

## 🛡️ License

Currently shared for educational and early development purposes.  
Full licensing and usage guidelines will be finalized upon stable release.

---

## 💬 Built By

A developer passionate about creating open, private, empowering AI tools — one step at a time.