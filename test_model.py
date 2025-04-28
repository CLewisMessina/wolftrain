# test_model.py
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def main():
    print("Loading fine-tuned model from ./wolftrain-output...")

    model = AutoModelForCausalLM.from_pretrained("./wolftrain-output")
    tokenizer = AutoTokenizer.from_pretrained("./wolftrain-output")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    while True:
        prompt = input("\nEnter your prompt (or type 'exit' to quit):\n> ")

        if prompt.lower() == "exit":
            print("Exiting.")
            break

        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        outputs = model.generate(**inputs, max_new_tokens=100)

        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        print("\n=== Model Output ===")
        print(generated_text)
        print("====================")

if __name__ == "__main__":
    main()
