from tika import parser
import spotlight
import os
import re
import spacy
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span
from rdflib import Graph, URIRef, Literal

if __name__ == '__main__':
    pdfs = [os.path.join(dp, f) for dp, dn, filenames in os.walk("courses/") for f in filenames if os.path.splitext(f)[1] == '.pdf']
    nlp = spacy.load("en_core_web_sm")

    # Creating the text file to save topics
    courseTopicsTextFile = open("saveTopics.txt", "w")

    for pdf in pdfs:
        pdf = pdf.replace("\\", "/")

        # Skip Outlines
        if "Outline" in pdf:
            continue

        # Opening PDF file
        parsed_pdf = parser.from_file(pdf)
        print("Processing " + pdf)

        # Saving content of PDF
        data = parsed_pdf['content']
        # courseSample.write(data)

        # Linking of content to dbpedia resource
        annotations = spotlight.annotate('https://api.dbpedia-spotlight.org/en/annotate', data, confidence=0.4, support=20)

        # To keep duplicates from being written to the file
        linesSeen = set()

        # Adding the topics
        for elt in annotations:
            # Extract the text from the annotations
            text = elt['surfaceForm']

            # Process the text with spaCy
            doc = nlp(text)

            # Filter out verbs and pronouns
            filtered_text = ' '.join(token.text for token in doc if token.pos_ not in ['VERB', 'PRON'])

            # Now you can use `filtered_text` for further processing or writing to file
            if filtered_text.strip():  # Check if the filtered text is not empty
                line = re.sub('[^A-Za-z0-9_-]+', '',
                              elt.get("URI").replace("http://dbpedia.org/resource/", "")) + " " + elt.get(
                    "URI") + " " + pdf + " " + pdf.split("/")[1] + "-" + pdf.split("/")[2] + "-" + \
                       re.findall('[0-9]+', pdf.split("/")[-1])[0] + "\n"
                if line not in linesSeen and not line == "":
                    courseTopicsTextFile.write(line)
                    linesSeen.add(line)

    # Showing where the new file can be found
    print("The Course Topics File has been saved as " + courseTopicsTextFile.name + " in " + os.getcwd())

    # Closing and saving the text file with the data
    courseTopicsTextFile.close()
