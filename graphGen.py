import pandas as pd  # for handling csv and csv contents
from rdflib import Graph, Literal, RDF, URIRef, Namespace, Dataset  # basic RDF handling
from rdflib.namespace import FOAF, RDFS, XSD  # most common namespaces
import os.path
from os import path
import re
import csv

if __name__ == '__main__':
    print("Generating graph....Please Wait\n")
    url = 'openData/OPENDATACOMBINED.csv'
    encodings_to_try = ['utf-8', 'latin1', 'ISO-8859-1']
    readCsv = pd.read_csv(url, sep=",", quotechar='"', encoding="ISO-8859-1", )

    # Namespaces
    FOCU = Namespace('http://focu.io/schema#')
    FOCUDATA = Namespace('http://focu.io/data#')
    OWL = Namespace('http://www.w3.org/2002/07/owl#')

    # Initialize a graph and bind namespaces
    g = Graph()
    g.bind('focu', FOCU)
    g.bind('focudata', FOCUDATA)
    g.bind('owl', OWL)

    # Create Concordia University
    g.add((URIRef(FOCUDATA + "Concordia_University"), RDF.type, FOCU.University))
    g.add((URIRef(FOCUDATA + "Concordia_University"), RDFS.label, Literal("Concordia University")))
    g.add((URIRef(FOCUDATA + "Concordia_University"), RDFS.comment,
           Literal(
               "Concordia University is a public comprehensive research university located in Montreal, Quebec, Canada.")))
    g.add((URIRef(FOCUDATA + "Concordia_University"), RDFS.seeAlso,
           URIRef("https://dbpedia.org/resource/Concordia_University")))
    g.add((URIRef(FOCUDATA + "Concordia_University"), OWL.sameAs,
           URIRef("https://dbpedia.org/resource/Concordia_University")))

    # Create all courses
    for index, row in readCsv.iterrows():
        g.add((URIRef(FOCUDATA + (row['Subject'] + str(row['Catalog']))), RDF.type, FOCU.Course))
        g.add((FOCUDATA.Concordia_University, FOCU.offers, URIRef(FOCUDATA + (row['Subject'] + str(row['Catalog'])))))
        if not pd.isnull(row['Long Title']):
            g.add((URIRef(FOCUDATA + (row['Subject'] + str(row['Catalog']))), FOCU.courseName, Literal(row['Long Title'])))
        if not pd.isnull(row['Subject']):
            g.add((URIRef(FOCUDATA + (row['Subject'] + str(row['Catalog']))), FOCU.courseSubject, Literal(row['Subject'])))
        if not pd.isnull(row['Catalog']):
            g.add((URIRef(FOCUDATA + (row['Subject'] + str(row['Catalog']))), FOCU.courseNumber, Literal(row['Catalog'])))
        if not pd.isnull(row['Description']):
            g.add((URIRef(FOCUDATA + (row['Subject'] + str(row['Catalog']))), FOCU.description, Literal(row['Description'])))
        if not pd.isnull(row['Website']):
            g.add((URIRef(FOCUDATA + (row['Subject'] + str(row['Catalog']))), RDFS.seeAlso, Literal(row['Website'])))
        if not pd.isnull(row['Class Units']):
            g.add((URIRef(FOCUDATA + (row['Subject'] + str(row['Catalog']))), FOCU.courseCredits, Literal(str(row['Class Units']))))

    with open(url, encoding='ISO-8859-1') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        # Add course contents for COMP6721
        try:
            for row in csv_reader:
                    # -----------------------------------------------------
                    #                   C O M P  6 7 2 1
                    # -----------------------------------------------------
                    if row[1] == "COMP" and row[2] == "6721":
                        # -----------------------------------------------------
                        #           ADD OUTLINE
                        # -----------------------------------------------------
                        course_outline_uri = "courses/COMP6721/OUT/course_outline_comp6721.pdf"
                        if path.exists(course_outline_uri):
                            g.add((URIRef(course_outline_uri), RDF.type, FOCU.courseOutline))
                            g.add((URIRef(FOCUDATA + "COMP6721"), FOCU.courseHas, URIRef(course_outline_uri)))
                        # -----------------------------------------------------
                        #           ADD WORKSHEET
                        # -----------------------------------------------------
                        wks_num = 1
                        wks_path = "courses/COMP6721/WKS/"
                        for filename1 in os.listdir(wks_path):
                            if filename1.endswith(".pdf"):
                                pdfFileName = wks_path + filename1
                                activity = pdfFileName.split("/")[1] + "-" + pdfFileName.split("/")[2] + "-" + \
                                            re.findall('[0-9]+', pdfFileName.split("/")[-1])[0]
                                g.add((URIRef(FOCUDATA + activity), RDF.type, FOCU.Worksheet))
                                g.add((URIRef(FOCUDATA + activity), FOCU.lectureNumber,
                                       Literal(wks_num)))
                                g.add((URIRef(wks_path + filename1), RDF.type, FOCU.Worksheet))
                                g.add((URIRef(FOCUDATA + activity), FOCU.hasContent,
                                       URIRef(wks_path + filename1)))
                                g.add((URIRef(FOCUDATA + URIRef("COMP6721-LEC-" + str(wks_num).zfill(2))), FOCU.hasContent,
                                       URIRef(FOCUDATA + activity)))
                                wks_num = wks_num + 1
                        # -----------------------------------------------------
                        #           ADD LAB
                        # -----------------------------------------------------
                        labCount = 1
                        labPath = "courses/COMP6721/LAB/"
                        for filename1 in os.listdir(labPath):
                            if filename1.endswith(".pdf"):
                                pdfFileName = labPath + filename1
                                activity = pdfFileName.split("/")[1] + "-" + pdfFileName.split("/")[2] + "-" + \
                                            re.findall('[0-9]+', pdfFileName.split("/")[-1])[0]
                                g.add((URIRef(FOCUDATA + activity), RDF.type, FOCU.Lab))
                                g.add((URIRef(FOCUDATA + activity), FOCU.lectureNumber,
                                       Literal(labCount)))
                                g.add((URIRef(labPath + filename1), RDF.type, FOCU.Lab))
                                g.add((URIRef(FOCUDATA + activity), FOCU.hasContent,
                                       URIRef(labPath + filename1)))
                                g.add((URIRef(FOCUDATA + URIRef("COMP6721-LEC-" + str(labCount).zfill(2))), FOCU.hasContent,
                                       URIRef(FOCUDATA + activity)))
                                labCount = labCount + 1
                        # -----------------------------------------------------
                        #           ADD TOPIC
                        # -----------------------------------------------------
                        topics = open("manualTopics.txt").readlines()
                        for topic in topics:
                            if "COMP6721" in topic:
                                topic = topic.replace("\n", "")
                                topic = topic.split()
                                label = topic[0]
                                uri = topic[1]
                                pdf = topic[2]
                                event = topic[3]
                                g.add((URIRef(FOCUDATA + label), RDF.type, FOCU.topic))
                                g.add((URIRef(FOCUDATA + label), RDFS.seeAlso, URIRef(uri)))
                                g.add((URIRef(FOCUDATA + label), RDFS.label, Literal(label)))
                                g.add((URIRef(FOCUDATA + "COMP6721"), FOCU.coversTopic, URIRef(FOCUDATA + label)))
                                g.add((URIRef(pdf), FOCU.coversTopic, URIRef(FOCUDATA + label)))
                        # -----------------------------------------------------
                        #           ADD LECTURE
                        # -----------------------------------------------------
                        lectureCount = 1
                        lectures_path = "courses/COMP6721/LEC/"
                        for filename in os.listdir(lectures_path):
                            if filename.endswith(".pdf"):
                                pdfFileName = lectures_path + filename
                                activity = pdfFileName.split("/")[1] + "-" + pdfFileName.split("/")[2] + "-" + \
                                            re.findall('[0-9]+', pdfFileName.split("/")[-1])[0]
                                g.add((URIRef(FOCUDATA + activity), RDF.type, FOCU.Lecture))
                                g.add((URIRef(FOCUDATA + activity), FOCU.lectureNumber,
                                       Literal(lectureCount)))
                                g.add((URIRef(lectures_path + filename), RDF.type, FOCU.Slides))
                                g.add((URIRef(FOCUDATA + activity), FOCU.hasContent,
                                       URIRef(lectures_path + filename)))
                                g.add((URIRef(FOCUDATA + "COMP6721"), FOCU.courseHas, URIRef(FOCUDATA + activity)))
                                lectureCount = lectureCount + 1


                    # Add course contents for COMP6721
                    # -----------------------------------------------------
                    #                   C O M P 6 7 4 1
                    # -----------------------------------------------------
                    if row[1] == "COMP" and row[2] == "6741":
                        # -----------------------------------------------------
                        #           ADD OUTLINE
                        # -----------------------------------------------------
                        course_outline_uri = "courses/COMP6741/OUT/course_outline_comp6741.pdf"
                        if path.exists(course_outline_uri):
                            g.add((URIRef(course_outline_uri), RDF.type, FOCU.courseOutline))
                            g.add((URIRef(FOCUDATA + "COMP6741"), FOCU.courseHas, URIRef(course_outline_uri)))
                        # -----------------------------------------------------
                        #           ADD WORKSHEET
                        # -----------------------------------------------------
                        worksheetCount = 1
                        worksheetPath = "courses/COMP6741/WKS/"
                        for filename in os.listdir(worksheetPath):
                            if filename.endswith(".pdf"):
                                g.add((URIRef(worksheetPath + filename), RDF.type, FOCU.Worksheet))
                                g.add((URIRef(FOCUDATA + "COMP6741-LEC-" + str(worksheetCount).zfill(2)), FOCU.hasContent,
                                       URIRef(worksheetPath + filename)))
                                worksheetCount = worksheetCount + 1

                        # -----------------------------------------------------
                        #           ADD TOPIC
                        # -----------------------------------------------------
                        topics = open("manualTopics.txt").readlines()
                        for topic in topics:
                            if "COMP6741" in topic:
                                topic = topic.replace("\n", "")
                                topic = topic.split()
                                label = topic[0]
                                uri = topic[1]
                                pdf = topic[2]
                                event = topic[3]
                                g.add((URIRef(FOCUDATA + label), RDF.type, FOCU.topic))
                                g.add((URIRef(FOCUDATA + label), RDFS.seeAlso, URIRef(uri)))
                                g.add((URIRef(FOCUDATA + label), RDFS.label, Literal(label)))
                                g.add((URIRef(FOCUDATA + "COMP6741"), FOCU.coversTopic, URIRef(FOCUDATA + label)))
                                g.add((URIRef(pdf), FOCU.coversTopic, URIRef(FOCUDATA + label)))
                        # --------------------------
                        #           ADD LECTURE
                        # --------------------------
                        lectureCount = 1
                        lectures_path = "courses/COMP6741/LEC/"
                        for filename in os.listdir(lectures_path):
                            if filename.endswith(".pdf"):
                                pdfFileName = lectures_path + filename
                                activity = pdfFileName.split("/")[1] + "-" + pdfFileName.split("/")[2] + "-" + \
                                            re.findall('[0-9]+', pdfFileName.split("/")[-1])[0]
                                g.add((URIRef(FOCUDATA + activity), RDF.type, FOCU.Lecture))
                                g.add((URIRef(FOCUDATA + activity), FOCU.lectureNumber,
                                       Literal(lectureCount)))
                                g.add((URIRef(lectures_path + filename), RDF.type, FOCU.Slides))
                                g.add((URIRef(FOCUDATA + activity), FOCU.hasContent,
                                       URIRef(lectures_path + filename)))
                                g.add((URIRef(FOCUDATA + "COMP6741"), FOCU.courseHas, URIRef(FOCUDATA + activity)))
                                lectureCount = lectureCount + 1

        except csv.Error as e:
            # Handle CSV errors
            print(f"CSV file error at line {csv_reader.line_num}: {e}")

        except Exception as e:
            # Handle other unexpected errors
            print(f"Unexpected error: {e}")


    g.serialize('GraphData.ttl', format='turtle')
    # g.serialize('GraphDataN3.ttl', format='nt')

    print("Graph successfully generated. Enjoy!")
