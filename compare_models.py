# compare_models.py
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def load_model(path_or_name):
    model = AutoModelForCausalLM.from_pretrained(path_or_name)
    tokenizer = AutoTokenizer.from_pretrained(path_or_name)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return model.to(device), tokenizer, device

def generate_text(model, tokenizer, device, prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    outputs = model.generate(**inputs, max_new_tokens=100)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def main():
    print("Loading base model (original TinyLlama)...")
    base_model, base_tokenizer, base_device = load_model("TinyLlama/TinyLlama-1.1B-Chat-v1.0")

    print("Loading fine-tuned model (Wolftrain output)...")
    tuned_model, tuned_tokenizer, tuned_device = load_model("./wolftrain-output")

    while True:
        prompt = input("\nEnter your prompt (or type 'exit' to quit):\n> ")

        if prompt.lower() == "exit":
            print("Exiting.")
            break

        print("\n=== Base Model Output ===")
        print(generate_text(base_model, base_tokenizer, base_device, prompt))

        print("\n=== Fine-Tuned Model Output ===")
        print(generate_text(tuned_model, tuned_tokenizer, tuned_device, prompt))

        print("==========================")

if __name__ == "__main__":
    main()
