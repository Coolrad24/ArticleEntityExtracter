import torch
from transformers import BertTokenizer, BertForTokenClassification
from datasets import load_dataset
from tqdm import tqdm
import csv

dataset = load_dataset("drAbreu/bc4chemd_ner")

model_name = "bert-base-cased"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForTokenClassification.from_pretrained(model_name)

label_map = {
    "O": 0,
    "B-Chemical": 1,
    "I-Chemical": 2,
}

# Set the model to evaluation mode
model.eval()

predictions = []

for example in tqdm(dataset['train']):
    try:
        tokens = example['tokens']
        ner_tags = example['ner_tags']

        inputs = tokenizer.encode_plus(
            tokens, add_special_tokens=True, return_tensors='pt'
        )

        with torch.no_grad():
            outputs = model(**inputs)

        logits = outputs.logits
        predicted_labels = torch.argmax(logits, dim=2).squeeze().tolist()

        # Convert predicted label IDs back to NER tags using the label_map
        predicted_ner_tags = [list(label_map.keys())[label_id] for label_id in predicted_labels]

        predictions.append(predicted_ner_tags)
    except:
        print("empty")

# Export predictions to a CSV file
with open("predictions.csv", mode="w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Prediction"])
    for prediction in predictions:
        csv_writer.writerow([" ".join(prediction)])

print("Predictions exported to predictions.csv")
