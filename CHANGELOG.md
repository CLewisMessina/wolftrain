# 🐺 Wolftrain Changelog

## [0.3.1-beta] — 2025-05-08

### Added
- Learning Rate Preset system with beginner-friendly options
- Rainbow-coded `Radiobuttons` with Lucide icons (e.g., flame, shield, zap)
- Auto-fill behavior to update the learning rate field when a preset is clicked

### Changed
- Replaced emoji-based labels with icon + text layout for better alignment and visual clarity
- Tightened UI spacing and layout in the Training Settings section

---

## [0.2.0-beta] — 2025-04-29

### Added
- Dataset preview popup (for both .txt and .csv)
- Live training loss display during training
- Configurable training parameters (epochs, batch size, learning rate)
- Clear console button in GUI
- Enhanced CSV structure validation (detect malformed rows or quoting issues)

### Changed
- GUI polish with dynamic form entries and ttkbootstrap styling
- Training callback now displays loss per step via `TrainerCallback`

### Known Upcoming Features
- CSV column selector (if multiple fields detected)
- Hugging Face model browsing inside app
- Adapter-only saving (for smaller outputs)
- Export-ready format for tools like Ollama
