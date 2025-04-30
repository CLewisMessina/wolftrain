# 🐺 Wolftrain Changelog

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
