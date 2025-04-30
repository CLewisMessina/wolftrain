# ui/app_frame.py
import os
import csv
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, Text
from ttkbootstrap import Frame, Label, Button, Entry, Progressbar, Scrollbar
from ttkbootstrap.constants import *
from controller import (
    set_base_model,
    set_dataset,
    clear_base_model,
    clear_dataset,
    start_training
)

MAX_DATASET_SIZE_BYTES = 1 * 1024 * 1024 * 1024  # 1GB

def validate_csv_file(path):
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames

        if not fieldnames:
            raise ValueError("CSV appears empty or improperly formatted.")
        if "text" not in fieldnames:
            raise ValueError("CSV must contain a single column named 'text'.")
        if len(fieldnames) > 1:
            raise ValueError(f"CSV has multiple columns: {fieldnames}. Only a single 'text' column is supported.")

        for i, row in enumerate(reader):
            if set(row.keys()) != {"text"}:
                raise ValueError(f"Row {i+2} appears malformed. Check for commas inside text that need quoting.")
            if i >= 5:
                break

def preview_dataset(path):
    preview_window = Toplevel()
    preview_window.title("📄 Dataset Preview")
    preview_window.geometry("600x300")

    label = Label(preview_window, text=f"First 5 Rows from: {os.path.basename(path)}", anchor="w")
    label.pack(fill=X, padx=10, pady=(10, 0))

    preview_text = Text(preview_window, wrap="word")
    preview_text.pack(fill=BOTH, expand=YES, padx=10, pady=10)

    try:
        if path.endswith(".csv"):
            with open(path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                rows = [row["text"] for _, row in zip(range(5), reader)]
                for i, row in enumerate(rows, 1):
                    preview_text.insert("end", f"{i}: {row}\n\n")
        elif path.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                lines = [next(f).strip() for _ in range(5)]
                for i, line in enumerate(lines, 1):
                    preview_text.insert("end", f"{i}: {line}\n\n")
    except Exception as e:
        preview_text.insert("end", f"Error loading preview: {str(e)}")

    preview_text.config(state="disabled")

class AppFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)

        self.base_model_path = None
        self.dataset_path = None

        self.base_model_label = Label(self, text="📦 No base model selected", anchor="w")
        self.base_model_label.pack(fill=X, pady=(0, 10))

        self.dataset_label = Label(self, text="📁 No dataset selected", anchor="w")
        self.dataset_label.pack(fill=X, pady=(0, 10))

        select_frame = Frame(self)
        select_frame.pack(fill=X, pady=(0, 10))

        self.select_model_btn = Button(select_frame, text="Select Model", command=self.select_model)
        self.select_model_btn.pack(side=LEFT, padx=(0, 5))

        self.clear_model_btn = Button(select_frame, text="Clear", command=self.clear_model)
        self.clear_model_btn.pack(side=LEFT, padx=(0, 10))

        self.select_dataset_btn = Button(select_frame, text="Select Dataset", command=self.select_dataset)
        self.select_dataset_btn.pack(side=LEFT, padx=(0, 5))

        self.clear_dataset_btn = Button(select_frame, text="Clear", command=self.clear_dataset)
        self.clear_dataset_btn.pack(side=LEFT)

        # Training settings inputs
        settings_frame = Frame(self)
        settings_frame.pack(fill=X, pady=(10, 10))

        self.epochs_entry = self._create_labeled_entry(settings_frame, "Epochs:", "1")
        self.batch_size_entry = self._create_labeled_entry(settings_frame, "Batch Size:", "4")
        self.learning_rate_entry = self._create_labeled_entry(settings_frame, "Learning Rate:", "5e-4")

        self.train_btn = Button(self, text="🚀 Start Training", bootstyle="primary", command=self.start_training)
        self.train_btn.pack(fill=X, pady=(10, 10))

        self.progress_bar = Progressbar(self, bootstyle="info-striped", maximum=100)
        self.progress_bar.pack(fill=X, pady=(0, 10))

        # Console header with Clear button
        console_header = Frame(self)
        console_header.pack(fill=X)
        console_label = Label(console_header, text="📈 Training Console:")
        console_label.pack(side=LEFT, padx=(0, 5))
        self.clear_console_btn = Button(console_header, text="Clear Console", command=self.clear_console)
        self.clear_console_btn.pack(side=RIGHT)

        console_frame = Frame(self)
        console_frame.pack(fill=BOTH, expand=YES)

        self.console_text = Text(console_frame, wrap="word", height=20)
        self.console_text.pack(side=LEFT, fill=BOTH, expand=YES)

        scrollbar = Scrollbar(console_frame, command=self.console_text.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.console_text.config(yscrollcommand=scrollbar.set)

    def _create_labeled_entry(self, parent, label_text, default_value):
        frame = Frame(parent)
        frame.pack(fill=X, pady=2)

        label = Label(frame, text=label_text, width=12, anchor="w")
        label.pack(side=LEFT)

        entry = Entry(frame)
        entry.insert(0, default_value)
        entry.pack(side=LEFT, fill=X, expand=YES)

        return entry

    def select_model(self):
        model_name = tk.simpledialog.askstring("Select Base Model", "Enter Hugging Face model name (e.g., sshleifer/tiny-gpt2):")
        if model_name:
            set_base_model(model_name)
            self.base_model_label.config(text=f"📦 {model_name}")

    def clear_model(self):
        clear_base_model()
        self.base_model_label.config(text="📦 No base model selected")

    def select_dataset(self):
        path = filedialog.askopenfilename(title="Select Dataset")
        if path:
            try:
                file_size = os.path.getsize(path)
                if file_size > MAX_DATASET_SIZE_BYTES:
                    raise ValueError("Dataset file too large (max 1GB).")
                if not path.endswith((".txt", ".csv")):
                    raise ValueError("Only .txt or .csv files are supported.")
                if path.endswith(".csv"):
                    validate_csv_file(path)

                set_dataset(path)
                self.dataset_label.config(text=f"📁 {os.path.basename(path)}")
                self._write_console("✅ Dataset valid and ready!")
                preview_dataset(path)  # <-- Launch preview popup
            except Exception as e:
                messagebox.showerror("Invalid Dataset", str(e))
                self._write_console(f"❌ Dataset validation failed: {str(e)}")

    def clear_dataset(self):
        clear_dataset()
        self.dataset_label.config(text="📁 No dataset selected")

    def start_training(self):
        self.progress_bar['value'] = 0

        try:
            epochs = int(self.epochs_entry.get())
            batch_size = int(self.batch_size_entry.get())
            learning_rate = float(self.learning_rate_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Settings", "Please enter valid numbers for training settings.")
            return

        success, message = start_training(self._training_update, epochs, batch_size, learning_rate)
        if not success:
            self._write_console(message)
            messagebox.showerror("Error", message)

    def _training_update(self, text):
        self._write_console(text)
        if "Step" in text:
            try:
                parts = text.split()
                current_step, total_steps = map(int, parts[2].split("/"))
                percent = (current_step / total_steps) * 100
                self.progress_bar['value'] = percent
            except:
                pass

    def _write_console(self, text):
        self.console_text.config(state="normal")
        self.console_text.insert("end", text + "\n")
        self.console_text.see("end")
        self.console_text.config(state="disabled")

    def clear_console(self):
        self.console_text.config(state="normal")
        self.console_text.delete("1.0", "end")
        self.console_text.config(state="disabled")