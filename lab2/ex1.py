from transformers import GPT2LMHeadModel, GPT2Tokenizer


model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

input_text = input("Input your 4 words: ")

input_ids = tokenizer.encode(input_text, return_tensors='pt')

output_ids = model.generate(
    input_ids,
    max_length=len(input_ids[0]) + 6,  
    num_return_sequences=1,
    no_repeat_ngram_size=2,
    pad_token_id=tokenizer.eos_token_id
)


output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)


predicted_part = output_text[len(input_text):].strip()
predicted_words = " ".join(predicted_part.split()[:2])

print(f"Input: {input_text}")
print(f"Predicted next two words: {predicted_words}")
print(f"Full sentence: {input_text} {predicted_words}")
