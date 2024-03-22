# Roboprof
Introducing Roboprof: Illuminating the Academic Seas
An intelligent agent that can answer university course- and student-related questions, using a knowledge graph and natural language processing.

Meet Roboprof. Amidst the labyrinth of academic challenges, where questions about NLP, neural networks, and even cafeteria coffee quality linger, Roboprof emerges as the beacon of enlightenment. This isn't just any digital assistant; Roboprof harnesses the power of Knowledge Graphs, Natural Language Processing (NLP), and Deep Learning to navigate the complexities of academia. With a blend of wisdom and wit, this intelligent agent stands ready to unravel your queries faster than you can utter "eigenvalues". 

This project marks the genesis of a transformative journey, comprised of two interlinked assignments. Our mission? To craft Roboprof—an intelligent agent capable of answering university course- and student-related questions using the fusion of knowledge graphs and NLP. Picture Roboprof effortlessly responding to inquiries like "What does COMP 474 entail?" or "What are Jane's areas of expertise?". 

## Code
* combineCsvData.py: this python file was used to create a new open data csv file that has data from CU_SR_OPEN_DATA_CATALOG and CATALOG.  

* graphGen.py: this python file was used to create the knowledge base itself. 

* studentN3TripleGen.py: generates the student.ttl file into N-Triples

## Files
* student.ttl:  manually created student triples for the knowledgebase

* manualtopic.txt:  manually extracted topics from the course folders and created each entry . 

* schema.ttl: the vocabulary which served as a guideline in creating the knowledge base 

* GraphData.ttl: the generated knowledge base in .ttl formart. The student data is manually added to the file.

* studentN3.ttl: student data in N-Triples format

* GraphDataN3.ttl: Knowledge base in N-Triples format



## Folders
courses: contains all the course contents(lecture slides, worksheet, lab and course outline) for COMP474/6741 and COMP6721
openData: contains the 2 (CU_SR_OPEN_DATA_CATALOG and CATALOG.).csv files from https://opendata.concordia.ca/datasets/ and the generated csv file OPENDATACOMBINED
queries: contains all the queries and their respective outputs.

### Prerequisites
* Python 3.8.8

### Getting Started
These instructions get the files above running on the development environment. 
Have the folders in the same directory as the .py files, the root directory.



## Installing
Install the following libraries in the development env
```
pip install pandas
pip install rdflib
```

## PROCESS
To replicate our knowledge base, follow the steps below:
1) First execute the combineCsvData.py file. This will generate the OPENDATACOMBINED in the openData folder
2) Afterwards, execute the graphGen.py file. This will generate the GraphData file which is the knowledge base itself.


## Testing the Queries
To test the queries, follow the steps below to setup Triplestore and SPARQL Endpoint
1) Downloaded the binary distribution of Fuseki from https://jena.apache.org/download/index.cgi. 
2) After downloading, extract the contents of the archive file, such as 'apache-jena-fuseki-4.10.0,' to a designated directory. 
3) Next, open the terminal and navigated to the directory where Fuseki was extracted. 
4) Using the terminal/cmd, ran the 'fuseki-server' script to initiate the Fuseki server. 
5) Once the server successfully started, you should be able to access the Fuseki web interface by opening a web browser and navigating to http://localhost:3030/.
6) Upload the GraphData.ttl file(including the student.ttl) to the server.
7) Copy and paste each query to run


## Authors (Contributors)
* **Oluwadamilola Okafor - Evaluation Specialist**
* **Ankush Ishwarbhai Desai - Data Specialist**
