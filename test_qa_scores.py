from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

model_name = "deepset/roberta-base-squad2-distilled"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)

def check_score(question, context):
    inputs = tokenizer(question, context, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    start_idx = torch.argmax(outputs.start_logits)
    end_idx = torch.argmax(outputs.end_logits)
    score = float(outputs.start_logits[0, start_idx] + outputs.end_logits[0, end_idx])
    answer_tokens = inputs["input_ids"][0][start_idx:end_idx + 1]
    answer = tokenizer.decode(answer_tokens, skip_special_tokens=True)
    print(f"Q: {question}\nAns: {answer}\nScore: {score}\n---")

check_score("what is this article about?", "The secondary market yield curve commenced the week with limited activity and thin trading volumes.")
check_score("When was it declared?", "On the 25th of February 1938, the Wilpattu National Park was declared the second National Park...")
check_score("Who invited EOIs?", "The Finance Ministry this week invited Expressions of Interest (EOIs) from consultancy firms...")
