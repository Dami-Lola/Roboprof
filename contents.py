import spacy
import csv
import os
# coursesTexts.txt
nlp = spacy.load("en_core_web_sm")  # Load the model and your custom pipeline
nlp.add_pipe("custom_matcher", last=True)

directory_path = 'courses'
csv_file = open('coursesTexts.txt', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Document Name", "Entities"])

for filename in os.listdir(directory_path):
    if filename.endswith(".pdf"):
        doc = nlp(open(os.path.join(directory_path, filename), 'r').read())
        entities = [ent.text for ent in doc.ents]
        csv_writer.writerow([filename, ', '.join(entities)])

csv_file.close()