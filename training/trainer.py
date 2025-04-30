# training/trainer.py
import os
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    TrainerCallback,
)
from peft import LoraConfig, get_peft_model
from datasets import load_dataset

class LossReporterCallback(TrainerCallback):
    def __init__(self, progress_callback):
        self.progress_callback = progress_callback

    def on_step_end(self, args, state, control, **kwargs):
        logs = state.log_history[-1] if state.log_history else {}
        if "loss" in logs and self.progress_callback:
            loss_val = logs["loss"]
            self.progress_callback(f"📉 Loss: {loss_val:.4f}")

def train_model(base_model_path, dataset_path, progress_callback=None, epochs=1, batch_size=4, learning_rate=5e-4):
    if progress_callback:
        progress_callback(f"Loading model from {base_model_path}...")

    model = AutoModelForCausalLM.from_pretrained(base_model_path)
    tokenizer = AutoTokenizer.from_pretrained(base_model_path)

    if torch.cuda.is_available():
        if progress_callback:
            progress_callback("GPU detected! Moving model to GPU...")
        model = model.to("cuda")
    else:
        if progress_callback:
            progress_callback("No GPU detected. Training on CPU.")

    lora_config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    model = get_peft_model(model, lora_config)

    if progress_callback:
        progress_callback(f"Loading dataset from {dataset_path}...")

    dataset_ext = os.path.splitext(dataset_path)[1]

    if dataset_ext == ".csv":
        raw_dataset = load_dataset("csv", data_files=dataset_path)
        dataset = raw_dataset.map(lambda x: {"text": x["text"]})
    elif dataset_ext == ".txt":
        dataset = load_dataset("text", data_files=dataset_path)
    else:
        raise ValueError("Unsupported dataset file type. Only .txt and .csv are supported.")

    def tokenize_function(examples):
        tokens = tokenizer(
            examples["text"],
            padding="max_length",
            truncation=True,
            max_length=512
        )
        tokens["labels"] = tokens["input_ids"].copy()
        return tokens

    tokenized_datasets = dataset.map(tokenize_function, batched=True)

    if progress_callback:
        progress_callback("Setting up training...")

    training_args = TrainingArguments(
        output_dir="./wolftrain-checkpoints",
        overwrite_output_dir=True,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        learning_rate=learning_rate,
        save_steps=50,
        save_total_limit=1,
        logging_steps=1,  # <- Force per-step logging
        disable_tqdm=True,  # <- Avoids progress bar stealing stdout
        logging_dir="./logs",  # <- Needed to make logs work
        report_to="none"      # <- No external tools
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets['train'],
        tokenizer=tokenizer,
        callbacks=[LossReporterCallback(progress_callback)]
    )

    if progress_callback:
        progress_callback("Starting training...")
    trainer.train()

    if progress_callback:
        progress_callback("Saving model...")
    model.save_pretrained("./wolftrain-output")
    tokenizer.save_pretrained("./wolftrain-output")

    if progress_callback:
        progress_callback("Training complete!")
    return True