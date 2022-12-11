from transformers import GPT2LMHeadModel, GPT2Tokenizer
#не запускать, мало оперативки

model_name_ru = "sberbank-ai/rugpt3large_based_on_gpt2"
tokenizer_ru = GPT2Tokenizer.from_pretrained(model_name_ru)
model_ru = GPT2LMHeadModel.from_pretrained(model_name_ru).cuda()
def rugen(text):
    input_ids = tokenizer_ru.encode(text, return_tensors="pt").cuda()
    out = model_ru.generate(input_ids.cuda())
    return list(map(tokenizer_ru.decode, out))[0]


model_name_en = "sberbank-ai/rugpt3large_based_on_gpt2"
tokenizer_en = GPT2Tokenizer.from_pretrained(model_name_en)
model_en = GPT2LMHeadModel.from_pretrained(model_name_en).cuda()
def engen(text):
    input_ids = tokenizer_en.encode(text, return_tensors="pt").cuda()
    out = model_en.generate(input_ids.cuda())
    return list(map(tokenizer_en.decode, out))[0]


if __name__ == '__main__':
    textru = rugen('что то')
    print(textru)