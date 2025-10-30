from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

input_text = input("Input your 4 words: ")

input_ids = tokenizer.encode(input_text, return_tensors='pt')


output_ids_1 = model.generate(
    input_ids,
    max_length=len(input_ids[0]) + 2, 
    num_return_sequences=1,
    no_repeat_ngram_size=2,
    pad_token_id=tokenizer.eos_token_id
)

output_text_1 = tokenizer.decode(output_ids_1[0], skip_special_tokens=True)
predicted_part_1 = output_text_1[len(input_text):].strip().split()[0]  

new_input_text = f"{input_text} {predicted_part_1}"
new_input_ids = tokenizer.encode(new_input_text, return_tensors='pt')

output_ids_2 = model.generate(
    new_input_ids,
    max_length=len(new_input_ids[0]) + 2,
    num_return_sequences=1,
    no_repeat_ngram_size=2,
    pad_token_id=tokenizer.eos_token_id
)

output_text_2 = tokenizer.decode(output_ids_2[0], skip_special_tokens=True)
predicted_part_2 = output_text_2[len(new_input_text):].strip().split()[0] 


print(f"\nInput (4 words): {input_text}")
print(f"Predicted 5th word: {predicted_part_1}")
print(f"Predicted 6th word (based on 4+1): {predicted_part_2}")
print(f"Full sentence: {input_text} {predicted_part_1} {predicted_part_2}")
