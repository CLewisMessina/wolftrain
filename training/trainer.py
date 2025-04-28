# training/trainer.py
import time
import os  # <-- Added to handle file type detection
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from peft import LoraConfig, get_peft_model
from datasets import load_dataset

def train_model(base_model_path, dataset_path, progress_callback=None):
    """
    Real mini fine-tuning loop using LoRA adapters.

    Args:
        base_model_path (str): Hugging Face model name or local path.
        dataset_path (str): Path to your dataset (text or CSV).
        progress_callback (function, optional): For UI updates.
    """
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

    # Apply basic LoRA config
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

    # NEW: Detect file type and load accordingly
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
        num_train_epochs=1,
        per_device_train_batch_size=4,
        save_steps=50,
        save_total_limit=1,
        logging_steps=10,
        report_to="none"  # no WANDB/logging
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets['train'],
        tokenizer=tokenizer
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
