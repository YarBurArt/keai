from transformers import AutoModelForCausalLM, AutoTokenizer


# download & load GPT-2 model
tokenizer = AutoTokenizer.from_pretrained("gpt2-large")
model = AutoModelForCausalLM.from_pretrained("gpt2-large")


def get_gpt2_text(text):
    inputs = tokenizer.encode(text, return_tensors='pt')

    outputs = model.generate(
        inputs, max_length=200, do_sample=True
    )
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return text


if __name__ == "__main__":
    txt = get_gpt2_text("tell me how is my anime girl: hello")
    print(txt)
