# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
import rasa_sdk
# This is a simple example for a custom action which utters "Hello World!"
import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

#
#

# Q1) List all courses offered by [university]
class ActionQueryAllCourses(Action):
    def name(self) -> Text:
        return "action_query_all_courses"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        query = """
                PREFIX fo: <http://www.w3.org/1999/XSL/Format#>
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                PREFIX focu: <http://focu.io/schema#>
                PREFIX focudata: <http://focu.io/data#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX ex: <http://example.org/>
                
                #1. List all courses offered by [university]
                SELECT ?course ?courseName ?courseSubject ?courseNumber ?courseUrl ?courseCredits ?description
                WHERE {
                  focudata:Concordia_University focu:offers ?course .
                  ?course a focu:Course ;
                      focu:courseSubject ?courseSubject ;
                      focu:courseName ?courseName ;
                      focu:courseNumber ?courseNumber;
                      focu:courseSubject ?courseSubject ;
                      focu:courseCredits ?courseCredits .
                    OPTIONAL{?course rdfs:seeAlso ?courseUrl .}
                    OPTIONAL{?course focu:description ?description .}
                }
                ORDER BY DESC (?courseCredits)
                LIMIT 20
        """
        try:
            response = requests.post('http://localhost:3030/play/sparql', data={'query': query})
            response_json = response.json()
            if response_json.get('results') and response_json['results'].get('bindings'):
                results = response_json['results']['bindings']
                dispatcher.utter_message(text=f"Please wait as i retrieve this information for you")
                count = 0
                for result in results:
                    courseName = ''
                    courseSubject = ''
                    courseNumber = ''
                    courseCredits = ''
                    for key in result:
                        count += 1
                        if key == "courseName":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    courseName = result[key][innerKey]
                        if key == "courseSubject":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    courseSubject = result[key][innerKey]
                        if key == "courseNumber":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    courseNumber = result[key][innerKey]
                        if key == "courseCredits":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    courseCredits = result[key][innerKey]
                    dispatcher.utter_message(text=f"CourseName: {courseName}\n"
                                                  f"CourseCode: {courseSubject}{courseNumber}\n"
                                                  f"CourseCredit: {courseCredits}\n\n")
                dispatcher.utter_message(
                    text=f"Concordia University has {count} courses in total. Listed above are just 20 of them.\n"
                         f"You may visit this link https://www.concordia.ca/academics.html for more course information")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find course information in Concordia University")
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f"Encountered an error while fetching data: {e}")
        return []


# Q2) In which courses is [topic] discussed?
class ActionCourseTopics(Action):
    def name(self) -> Text:
        return "action_course_topics"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        topic_name = tracker.get_slot('topic')
        query = """
                PREFIX fo: <http://www.w3.org/1999/XSL/Format#>
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                PREFIX focu: <http://focu.io/schema#>
                PREFIX focudata: <http://focu.io/data#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX ex: <http://example.org/>
                
                #2. In which courses is [topic] discussed?
                SELECT ?courseSubject ?courseNumber ?courseName ?topicLabel
                WHERE {
                
                  ?course a focu:Course;
                  focu:coversTopic ?topic ;
                  focu:courseNumber ?courseNumber;
                  focu:courseSubject ?courseSubject;
                  focu:courseName ?courseName .
                
                
                  ?topic a focu:topic;
                  rdfs:label ?topicLabel .
                
                  FILTER (?topicLabel = "%s")
                }
        """ % topic_name
        try:
            response = requests.post('http://localhost:3030/play/sparql', data={'query': query})
            response_json = response.json()
            if response_json.get('results') and response_json['results'].get('bindings'):
                results = response_json['results']['bindings']
                for result in results:
                    courseName = ''
                    courseSubject = ''
                    courseNumber = ''
                    topicLabel = ''
                    for key in result:
                        if key == "courseName":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    courseName = result[key][innerKey]
                        if key == "courseSubject":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    courseSubject = result[key][innerKey]
                        if key == "courseNumber":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    courseNumber = result[key][innerKey]
                        if key == "topicLabel":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    topicLabel = result[key][innerKey]
                    dispatcher.utter_message(text=f"{courseName}({courseSubject}{courseNumber}) covers {topicLabel}\n")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find course information in Concordia University")
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f"Encountered an error while fetching data: {e}")
        return []


# Q3) Which [topics] are covered in [course] during [lecture number]?
class ActionCourseLectureTopics(Action):
    def name(self) -> Text:
        return "action_course_lecture_topics"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course = tracker.slots['course']
        lecture = tracker.slots['lecture']

        course_parts = course.split(" ")
        lecture_parts = lecture.split(" ")
        course_subject = course_parts[0]
        course_number = course_parts[1]
        lecture_number = lecture_parts[1]

        query = """
                PREFIX fo: <http://www.w3.org/1999/XSL/Format#>
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                PREFIX focu: <http://focu.io/schema#>
                PREFIX focudata: <http://focu.io/data#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX ex: <http://example.org/>
                
                #3. Which [topics] are covered in [course] during [lecture number]?
                SELECT DISTINCT ?courseName ?topicLabel
                WHERE {
                  ?course a focu:Course ;
                  focu:courseNumber ?courseNumber;
                  focu:courseSubject ?courseSubject;
                  focu:courseName ?courseName ;
                  focu:coversTopic ?topic .
                
                  ?lecture a focu:Lecture ;
                  focu:lectureNumber ?lectureNumber ;
                  focu:hasContent ?content .
                
                  ?content a focu:Slides ;
                  focu:coversTopic ?topic .
                
                  ?topic a focu:topic ;
                  rdfs:label ?topicLabel.
                
                  FILTER(?lectureNumber = "%s"^^xsd:int)
                  FILTER(?courseNumber = "%s" && ?courseSubject = "%s")
                }
        """ % (lecture_number, course_number, course_subject)
        try:
            response = requests.post('http://localhost:3030/play/sparql', data={'query': query})
            response_json = response.json()
            if response_json.get('results') and response_json['results'].get('bindings'):
                results = response_json['results']['bindings']
                courseName = ''
                topicsList = []
                for result in results:
                    for key in result:
                        if key == "courseName":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    courseName = result[key][innerKey]
                        if key == "topicLabel":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    topicsList.append(result[key][innerKey])
                dispatcher.utter_message(text=f"In Lecture {lecture_number}, {courseName}({course_subject}{course_number}) "
                                              f"covered the following topics: \n")
                for topic in topicsList:
                    dispatcher.utter_message(text=f"{topic}\n")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find course information in Concordia University")
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f"Encountered an error while fetching data: {e}")
        return []


# Q4) List all [courses] offered by [university] within the [subject] (e.g., “COMP”, “SOEN”).
class ActionSpecificUniCourses(Action):
    def name(self) -> Text:
        return "action_specific_uni_courses"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        subject = tracker.slots['subject']
        query = """
            PREFIX fo: <http://www.w3.org/1999/XSL/Format#>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX focu: <http://focu.io/schema#>
            PREFIX focudata: <http://focu.io/data#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX ex: <http://example.org/>
            
            #4. List all [courses] offered by [university] within the [subject] (e.g., “COMP”, “SOEN”).
            SELECT ?courseName
            WHERE {
              focudata:Concordia_University focu:offers ?course .
              ?course a focu:Course ;
                  focu:courseSubject ?courseSubject ;
                  focu:courseName ?courseName ;
                  focu:courseNumber ?courseNumber;
                  focu:courseSubject ?courseSubject.
              FILTER (?courseSubject = "%s")
            }
            LIMIT 20
        """ % subject
        try:
            response = requests.post('http://localhost:3030/play/sparql', data={'query': query})
            response_json = response.json()
            if response_json.get('results') and response_json['results'].get('bindings'):
                results = response_json['results']['bindings']
                courseName = []
                for result in results:
                    for key in result:
                        if key == "courseName":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    courseName.append(result[key][innerKey])

                dispatcher.utter_message(text=f"Find below 20 {subject} courses offered in the university.\n"
                                              f"You may visit this link https://www.concordia.ca/academics.html for more course information\n")
                for course in courseName:
                    dispatcher.utter_message(text=f"{course}")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find course information in Concordia University")
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f"Encountered an error while fetching data: {e}")
        return []


# Q5) What [materials] (slides, readings) are recommended for [topic] in [course] [number]?
class ActionRecommendedMaterials(Action):
    def name(self) -> Text:
        return "action_recommended_materials"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course = tracker.slots['course']
        topic = tracker.slots['topic']
        course_parts = course.split(" ")
        course_subject = course_parts[0]
        course_number = course_parts[1]

        query = """
                PREFIX fo: <http://www.w3.org/1999/XSL/Format#>
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                PREFIX focu: <http://focu.io/schema#>
                PREFIX focudata: <http://focu.io/data#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX ex: <http://example.org/>
                
                #5. What [materials] (slides, readings) are recommended for [topic] in [course] [number]?
                SELECT DISTINCT ?courseName ?slide ?topicLabel
                WHERE {
                
                  ?slide a focu:Slides ;
                  focu:coversTopic ?topic .
                
                  focudata:%s a focu:topic ;
                  rdfs:label ?topicLabel .
                
                  ?course a focu:Course ;
                  focu:courseNumber ?courseNumber;
                  focu:courseSubject ?courseSubject;
                  focu:courseName ?courseName ;
                  focu:coversTopic focudata:%s .
                  
                  FILTER (?courseNumber = "%s" && ?courseSubject = "%s")
                }
        """ % (topic, topic, course_number, course_subject)
        try:
            response = requests.post('http://localhost:3030/play/sparql', data={'query': query})
            response_json = response.json()
            if response_json.get('results') and response_json['results'].get('bindings'):
                results = response_json['results']['bindings']
                slides = []
                courseName =''
                topicLabel =''
                for result in results:
                    for key in result:
                        if key == "slide":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    slides.append(result[key][innerKey])
                        if key == "courseName":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    courseName = result[key][innerKey]
                        if key == "topicLabel":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    topicLabel = result[key][innerKey]

                dispatcher.utter_message(text=f"Here are the reading materials for {courseName}({course_subject}{course_number}) on {topicLabel}.\n")
                for slide in slides:
                    sampleString = slide
                    slideString = sampleString.split('/')
                    dispatcher.utter_message(text=f"{slideString[len(slideString) - 1]}")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find course information in Concordia University")
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f"Encountered an error while fetching data: {e}")
        return []


# Q6) How many credits is [course] [number] worth?
class ActionCourseCredits(Action):
    def name(self) -> Text:
        return "action_course_credits"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course = tracker.slots['course']

        course_parts = course.split(" ")
        course_subject = course_parts[0]
        course_number = course_parts[1]


        query = """
                PREFIX fo: <http://www.w3.org/1999/XSL/Format#>
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                PREFIX focu: <http://focu.io/schema#>
                PREFIX focudata: <http://focu.io/data#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX ex: <http://example.org/>
                
                #6. How many credits is [course] [number] worth?
                SELECT ?courseName ?courseCredit
                WHERE {
                
                  ?course a focu:Course ;
                  focu:courseNumber ?courseNumber;
                  focu:courseSubject ?courseSubject;
                  focu:courseName ?courseName ;
                  focu:courseCredits ?courseCredit .
                
                  FILTER(?courseNumber = "%s" && ?courseSubject = "%s")
                }
        """ % (course_number, course_subject)
        try:
            response = requests.post('http://localhost:3030/play/sparql', data={'query': query})
            response_json = response.json()
            if response_json.get('results') and response_json['results'].get('bindings'):
                results = response_json['results']['bindings']
                courseName = ''
                credit = ''
                for result in results:
                    for key in result:
                        if key == "courseName":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    courseName = result[key][innerKey]
                        if key == "courseCredit":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    credit = result[key][innerKey]
                dispatcher.utter_message(
                    text=f"{courseName}({course_subject}{course_number}) is {credit} credits")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find course information in Concordia University")
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f"Encountered an error while fetching data: {e}")
        return []


# Q7) For [course] [number], what additional resources (links to web pages) are available?
class ActionAdditionalResources(Action):
    def name(self) -> Text:
        return "action_additional_resources"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course = tracker.slots['course']
        course_parts = course.split(" ")
        course_subject = course_parts[0]
        course_number = course_parts[1]

        query = """
                    PREFIX fo: <http://www.w3.org/1999/XSL/Format#>
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    PREFIX focu: <http://focu.io/schema#>
                    PREFIX focudata: <http://focu.io/data#>
                    PREFIX owl: <http://www.w3.org/2002/07/owl#>
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                    PREFIX ex: <http://example.org/>
                    
                    #7. For [course] [number], what additional resources (links to web pages) are available?
                    SELECT ?courseNumber ?courseSubject ?courseName ?courseUrl
                    WHERE {
                    
                      ?course a focu:Course ;
                      focu:courseNumber ?courseNumber;
                      focu:courseSubject ?courseSubject;
                      focu:courseName ?courseName ;
                      rdfs:seeAlso ?courseUrl .
                    
                      FILTER (?courseNumber = "%s" && ?courseSubject = "%s")
                    }
        """ % (course_number, course_subject)
        try:
            response = requests.post('http://localhost:3030/play/sparql', data={'query': query})
            response_json = response.json()
            if response_json.get('results') and response_json['results'].get('bindings'):
                results = response_json['results']['bindings']
                courseName = ''
                courseUrl = ''
                for result in results:
                    for key in result:
                        if key == "courseName":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    courseName = result[key][innerKey]
                        if key == "courseUrl":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    courseUrl = result[key][innerKey]

                dispatcher.utter_message(
                    text=f"You may find additional resources to {courseName}({course_subject}{course_number}) at {courseUrl}.\n")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find course information in Concordia University")
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f"Encountered an error while fetching data: {e}")
        return []


# Q8) Detail the content (slides, worksheets, readings) available for [lecture number] in [course] [number].
class ActionContentCourseLecture(Action):
    def name(self) -> Text:
        return "action_content_course_lecture"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course = tracker.slots['course']
        lecture = tracker.slots['lecture']

        course_parts = course.split(" ")
        lecture_parts = lecture.split(" ")
        course_subject = course_parts[0]
        course_number = course_parts[1]
        lecture_number = lecture_parts[1]

        query = """
                PREFIX fo: <http://www.w3.org/1999/XSL/Format#>
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                PREFIX focu: <http://focu.io/schema#>
                PREFIX focudata: <http://focu.io/data#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX ex: <http://example.org/>
                
                #8. Detail the content (slides, worksheets, readings) available for [lecture number] in [course] [number].
                SELECT DISTINCT ?courseName ?lecture ?content ?lab ?worksheet
                WHERE {
                  ?course a focu:Course ;
                  focu:courseNumber ?courseNumber;
                  focu:courseSubject ?courseSubject;
                  focu:courseName ?courseName ;
                  focu:coversTopic ?topic .
                
                  ?lecture a focu:Lecture ;
                  focu:lectureNumber ?lectureNumber ;
                  focu:hasContent ?content .
                
                  OPTIONAL{?content a focu:Slides ;
                  focu:coversTopic ?topic .}
                
                  OPTIONAL
                  {?content a focu:Lab ;
                  focu:hasContent ?lab .}
                
                  OPTIONAL
                  {?content a focu:Worksheet ;
                  focu:hasContent ?worksheet .
                 }
                
                  FILTER(?lectureNumber = "%s"^^xsd:int)
                  FILTER(?courseNumber = "%s" && ?courseSubject = "%s")
                }
        """ % (lecture_number, course_number, course_subject)
        try:
            response = requests.post('http://localhost:3030/play/sparql', data={'query': query})
            response_json = response.json()
            if response_json.get('results') and response_json['results'].get('bindings'):
                results = response_json['results']['bindings']
                courseName = ''
                courseContent = []
                labContent = []
                worksheetContent = []
                for result in results:
                    for key in result:
                        if key == "courseName":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    courseName = result[key][innerKey]
                        if key == "content":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    courseContent.append(result[key][innerKey])
                        if key == "lab":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    labContent.append(result[key][innerKey])
                        if key == "worksheet":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    worksheetContent.append(result[key][innerKey])
                dispatcher.utter_message(
                    text=f"Find below detailed content for lecture {lecture_number}, in {courseName}({course_subject}{course_number}) "
                         f"covered the following topics: \n")
                for content in courseContent:
                    sampleString = content
                    contentString = sampleString.split('/')
                    if 'data#' not in contentString[len(contentString) - 1]:
                        dispatcher.utter_message(text=f"{contentString[len(contentString) - 1]}")
                    # dispatcher.utter_message(text=f"{content}\n")
                if len(labContent) != 0:
                    for labCon in labContent:
                        sampleString = labCon
                        labString = sampleString.split('/')
                        dispatcher.utter_message(text=f"{labString[len(labString) - 1]}")
                if len(worksheetContent) != 0:
                    for workSCon in worksheetContent:
                        sampleString = workSCon
                        worksheetString = sampleString.split('/')
                        dispatcher.utter_message(text=f"{worksheetString[len(worksheetString) - 1]}")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find course information in Concordia University")
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f"Encountered an error while fetching data: {e}")
        return []


# Q9) What reading materials are recommended for studying [topic] in [course]?
class ActionMaterials(Action):
    def name(self) -> Text:
        return "action_course_reading_materials"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course = tracker.slots['course']
        topic = tracker.slots['topic']
        course_parts = course.split(" ")
        course_subject = course_parts[0]
        course_number = course_parts[1]

        query = """
                PREFIX fo: <http://www.w3.org/1999/XSL/Format#>
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                PREFIX focu: <http://focu.io/schema#>
                PREFIX focudata: <http://focu.io/data#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX ex: <http://example.org/>
                
                #9. What reading materials are recommended for studying [topic] in [course]?
                
                SELECT ?courseSubject ?courseNumber ?courseName ?topicLabel ?slide ?worksheet ?lab
                WHERE {
                
                  ?course a focu:Course ;
                  focu:coversTopic ?topic ;
                  focu:courseNumber ?courseNumber;
                  focu:courseSubject ?courseSubject;
                  focu:courseName ?courseName .
                
                  ?topic a focu:topic;
                  rdfs:label ?topicLabel .
                
                  ?slide a focu:Slides;
                  focu:coversTopic ?topic.
                
                  ?worksheet a focu:Worksheet;
                  focu:coversTopic ?topic.
                
                  ?lab a focu:Lab;
                  focu:coversTopic ?topic.
                
                  FILTER (?topicLabel = "%s")
                  FILTER(?courseNumber = "%s" && ?courseSubject = "%s")
                }
        """ % (topic, course_number, course_subject)
        try:
            response = requests.post('http://localhost:3030/play/sparql', data={'query': query})
            response_json = response.json()
            if response_json.get('results') and response_json['results'].get('bindings'):
                results = response_json['results']['bindings']
                slides = []
                courseName = ''
                topicLabel = ''
                for result in results:
                    for key in result:
                        if key == "slides":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    slides.append(result[key][innerKey])
                        if key == "worksheet":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    slides.append(result[key][innerKey])
                        if key == "lab":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    slides.append(result[key][innerKey])
                        if key == "courseName":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    courseName = result[key][innerKey]
                        if key == "topicLabel":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    topicLabel = result[key][innerKey]

                dispatcher.utter_message(
                    text=f"Here are the recommended reading materials for {courseName}({course_subject}{course_number}) on {topicLabel}.\n")
                for slide in slides:
                    sampleString = slide
                    slideString = sampleString.split('/')
                    dispatcher.utter_message(text=f"{slideString[len(slideString) - 1]}")
                    # dispatcher.utter_message(text=f"{slide}")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find course information in Concordia University")
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f"Encountered an error while fetching data: {e}")
        return []


# Q10) What competencies [topics] does a student gain after completing [course] [number]?
class ActionStudentCompetencies(Action):
    def name(self) -> Text:
        return "action_student_competencies"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        student = tracker.slots['student']
        course = tracker.slots['course']
        course_parts = course.split(" ")
        course_subject = course_parts[0]
        course_number = course_parts[1]

        query = """
                PREFIX fo: <http://www.w3.org/1999/XSL/Format#>
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                PREFIX focu: <http://focu.io/schema#>
                PREFIX focudata: <http://focu.io/data#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX ex: <http://example.org/>

                #10. What competencies [topics] does a student gain after completing [course] [number]?

                SELECT  ?studentName ?courseName ?topiclabel
                WHERE {

                  ex:%s a focu:Student ;
                  focu:studentName ?studentName ;
                  focu:studentID ?studentID ;
                  focu:completedCourse [
                      focu:courseCode ?course ;
                      focu:competencyInTopic ?topic ;
                      focu:gradeAchieved ?grade  ].

                  ?topic a focu:topic ;
                  rdfs:label ?topiclabel .

                  ?course a focu:Course ;
                  focu:courseNumber ?courseNumber;
                  focu:courseSubject ?courseSubject;
                  focu:courseName ?courseName .

                  FILTER (?courseNumber = "%s" && ?courseSubject = "%s")
                }
        """ % (student, course_number, course_subject)
        try:
            response = requests.post('http://localhost:3030/play/sparql', data={'query': query})
            response_json = response.json()
            if response_json.get('results') and response_json['results'].get('bindings'):
                results = response_json['results']['bindings']
                courseName = ''
                studentName =''
                topics = []
                for result in results:
                    for key in result:
                        if key == "studentName":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    studentName = result[key][innerKey]
                        if key == "courseName":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    courseName = result[key][innerKey]
                        if key == "topiclabel":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    topics.append(result[key][innerKey])
                dispatcher.utter_message(
                    text=f"Find below topics {studentName} is competent in for {courseName}({course_subject}{course_number})\n")
                for topic in topics:
                    dispatcher.utter_message(text=f"{topic}")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find course information in Concordia University")
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f"Encountered an error while fetching data: {e}")
        return []


# Q11) What grades did [student] achieve in [course] [number]?
class ActionStudentGrades(Action):
    def name(self) -> Text:
        return "action_student_grades"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        student = tracker.slots['student']
        course = tracker.slots['course']
        course_parts = course.split(" ")
        course_subject = course_parts[0]
        course_number = course_parts[1]

        query = """
                PREFIX fo: <http://www.w3.org/1999/XSL/Format#>
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                PREFIX focu: <http://focu.io/schema#>
                PREFIX focudata: <http://focu.io/data#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX ex: <http://example.org/>
                
                #11. What grades did [student] achieve in [course] [number]?
                
                SELECT ?studentName ?courseName ?grade
                WHERE {
                
                  ex:%s a focu:Student ;
                  focu:studentName ?studentName ;
                  focu:studentID ?studentID ;
                  focu:completedCourse [
                      focu:courseCode ?course ;
                      focu:gradeAchieved ?grade ; ].
                
                  ?course a focu:Course ;
                  focu:courseNumber ?courseNumber;
                  focu:courseSubject ?courseSubject;
                  focu:courseName ?courseName .
                
                  FILTER (?courseNumber = "%s" && ?courseSubject = "%s")
                }
        """ % (student, course_number, course_subject)
        try:
            response = requests.post('http://localhost:3030/play/sparql', data={'query': query})
            response_json = response.json()
            if response_json.get('results') and response_json['results'].get('bindings'):
                results = response_json['results']['bindings']
                courseName = ''
                studentName =''
                grade = ''
                for result in results:
                    for key in result:
                        if key == "studentName":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    studentName = result[key][innerKey]
                        if key == "courseName":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    courseName = result[key][innerKey]
                        if key == "grade":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    grade = result[key][innerKey]
                dispatcher.utter_message(
                    text=f"{studentName} has {grade} in {courseName}({course_subject}{course_number})\n")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find course information in Concordia University")
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f"Encountered an error while fetching data: {e}")
        return []


# Q12) Which [students] have completed [course] [number]?
class ActionStudentCompletedCourse(Action):
    def name(self) -> Text:
        return "action_student_completed_course"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course = tracker.slots['course']
        course_parts = course.split(" ")
        course_subject = course_parts[0]
        course_number = course_parts[1]

        query = """
                PREFIX fo: <http://www.w3.org/1999/XSL/Format#>
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                PREFIX focu: <http://focu.io/schema#>
                PREFIX focudata: <http://focu.io/data#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX ex: <http://example.org/>
                
                #12. Which [students] have completed [course] [number]?
                
                SELECT DISTINCT ?studentName ?studentID ?courseName
                WHERE {
                  ?student a focu:Student ;
                  focu:studentName ?studentName ;
                  focu:studentID ?studentID ;
                  focu:completedCourse [
                      focu:courseCode ?course ].
                
                  ?course a focu:Course ;
                  focu:courseNumber ?courseNumber;
                  focu:courseSubject ?courseSubject;
                  focu:courseName ?courseName .
                
                  FILTER (?courseNumber = "%s" && ?courseSubject = "%s")
                }
        """ % (course_number, course_subject)
        try:
            response = requests.post('http://localhost:3030/play/sparql', data={'query': query})
            response_json = response.json()
            if response_json.get('results') and response_json['results'].get('bindings'):
                results = response_json['results']['bindings']
                students = []
                courseName = ''
                for result in results:
                    for key in result:
                        if key == "studentName":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    students.append(result[key][innerKey])
                        if key == "courseName":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    courseName = result[key][innerKey]
                dispatcher.utter_message(
                    text=f"Find below students that completed {courseName}({course_subject}{course_number})\n")
                for student in students:
                    dispatcher.utter_message(text=f"{student}")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find course information in Concordia University")
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f"Encountered an error while fetching data: {e}")
        return []


# Q13) Print a transcript for a [student], listing all the course taken with their grades.
class ActionStudentTranscript(Action):
    def name(self) -> Text:
        return "action_student_transcript"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        student = tracker.slots['student']

        query = """
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                PREFIX focu: <http://focu.io/schema#>
                PREFIX focudata: <http://focu.io/data#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX ex: <http://example.org/>
                
                #13. Print a transcript for a [student], listing all the course taken with their grades.
                SELECT ?studentName ?studentID ?courseSubject ?courseNumber ?courseName ?grade
                WHERE {
                  ex:%s a focu:Student ;
                  focu:studentName ?studentName ;
                  focu:studentID ?studentID ;
                  focu:completedCourse [
                      focu:courseCode ?course ;
                      focu:gradeAchieved ?grade ] .
                
                  ?course a focu:Course ;
                  focu:courseNumber ?courseNumber ;
                  focu:courseSubject ?courseSubject ;
                  focu:courseName ?courseName .
                }
        """ % student
        try:
            response = requests.post('http://localhost:3030/play/sparql', data={'query': query})
            response_json = response.json()
            if response_json.get('results') and response_json['results'].get('bindings'):
                results = response_json['results']['bindings']
                transcript_dict = {}
                student_name = ''
                for result in results:
                    student_name = result['studentName']['value']
                    course_name = result['courseName']['value']
                    course_subject = result['courseSubject']['value']
                    course_number = result['courseNumber']['value']
                    grade = result['grade']['value']
                    value_list = [course_name, f"{course_subject}{course_number}", grade]
                    if student_name not in transcript_dict:
                        transcript_dict[student_name] = []
                    transcript_dict[student_name].append(value_list)
                dispatcher.utter_message(
                    text=f"Find below {student_name} transcript\n")
                for student_name, courses in transcript_dict.items():
                    for course_info in courses:
                        course_name, course_subject_number, grade = course_info
                        dispatcher.utter_message(
                            text=f"{course_name}({course_subject_number}), Grade: {grade}")

            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find course information in Concordia University")
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f"Encountered an error while fetching data: {e}")
        return []


# Q14) What is the <course> about?
class ActionCourseInfo(Action):
    def name(self) -> Text:
        return "action_course_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course = tracker.slots['course']
        course_parts = course.split(" ")
        course_subject = course_parts[0]
        course_number = course_parts[1]

        query = """
                PREFIX fo: <http://www.w3.org/1999/XSL/Format#>
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                PREFIX focu: <http://focu.io/schema#>
                PREFIX focudata: <http://focu.io/data#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX ex: <http://example.org/>

                SELECT ?description ?courseName
                WHERE {

                  ?course a focu:Course ;
                  focu:courseNumber ?courseNumber;
                  focu:courseSubject ?courseSubject;
                  focu:courseName ?courseName ;
                  focu:description ?description .

                  FILTER(?courseNumber = "%s" && ?courseSubject = "%s")
                }
        """ % (course_number, course_subject)
        try:
            response = requests.post('http://localhost:3030/play/sparql', data={'query': query})
            response_json = response.json()
            if response_json.get('results') and response_json['results'].get('bindings'):
                results = response_json['results']['bindings']
                courseName = ''
                description = ''
                for result in results:
                    courseName = result['courseName']['value']
                    description = result['description']['value']
                dispatcher.utter_message(
                    text=f"About {courseName}({course_subject}{course_number}): \n{description}")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find course information in Concordia University")
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f"Encountered an error while fetching data: {e}")
        return []


# Q15) Which topics are covered in <course event>?
class ActionCourseEvent(Action):
    def name(self) -> Text:
        return "action_course_event"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        courseEvent = tracker.slots['courseEvent']
        courseEvent_parts = courseEvent.split(" ")
        courseEventName = courseEvent_parts[0]
        courseEventNumber = courseEvent_parts[1]
        query = ""
        if courseEventName.lower() == "lab":
            query = """
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    PREFIX focu: <http://focu.io/schema#>
                    PREFIX focudata: <http://focu.io/data#>
                    PREFIX owl: <http://www.w3.org/2002/07/owl#>
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                    PREFIX ex: <http://example.org/>

                    SELECT DISTINCT ?lab ?topicLabel ?topicURL
                    WHERE {
                      <http://localhost:3030/play/courses/COMP6721/LAB/LE%s.pdf> a focu:Lab ;
                      focu:coversTopic ?topic .

                      ?topic a focu:topic ;
                      rdfs:label ?topicLabel ;
                      rdfs:seeAlso ?topicURL .
                    }
            """ % courseEventNumber
        elif courseEventName.lower() == "slide":
            query = """
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    PREFIX focu: <http://focu.io/schema#>
                    PREFIX focudata: <http://focu.io/data#>
                    PREFIX owl: <http://www.w3.org/2002/07/owl#>
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                    PREFIX ex: <http://example.org/>

                    SELECT DISTINCT ?lab ?topicLabel ?topicURL
                    WHERE {
                      <http://localhost:3030/play/courses/COMP6721/LEC/LS%s.pdf> a focu:Slides ;
                      focu:coversTopic ?topic .

                      ?topic a focu:topic ;
                      rdfs:label ?topicLabel ;
                      rdfs:seeAlso ?topicURL .
                    }
            """ % courseEventNumber
        elif courseEventName.lower() == "worksheet":
            query = """
                    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    PREFIX focu: <http://focu.io/schema#>
                    PREFIX focudata: <http://focu.io/data#>
                    PREFIX owl: <http://www.w3.org/2002/07/owl#>
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                    PREFIX ex: <http://example.org/>

                    SELECT DISTINCT ?topicLabel ?topicURL
                    WHERE {
                      <http://localhost:3030/play/courses/COMP6721/WKS/WS%s.pdf> a focu:Worksheet ;
                      focu:coversTopic ?topic .

                      ?topic a focu:topic ;
                      rdfs:label ?topicLabel ;
                      rdfs:seeAlso ?topicURL .
                    }
            """ % courseEventNumber
        try:
            response = requests.post('http://localhost:3030/play/sparql', data={'query': query})
            response_json = response.json()
            if response_json.get('results') and response_json['results'].get('bindings'):
                results = response_json['results']['bindings']
                dispatcher.utter_message(
                    text=f"Find below topics covered with their respective resources:\n")
                topicLabel = ''
                topicURL = ''
                for result in results:
                    for key in result:
                        if key == "topicLabel":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    topicLabel = result[key][innerKey]
                        if key == "topicURL":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    topicURL = result[key][innerKey]

                    dispatcher.utter_message(text=f"Topic: {topicLabel}\n"
                                                  f"Resource: {topicURL}\n")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find course information in Concordia University")
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f"Encountered an error while fetching data: {e}")
        return []


# Q16) Which course events cover <Topic>?
class ActionCourseTopicevent(Action):
    def name(self) -> Text:
        return "action_course_topicevent"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        topic = tracker.slots['topic']
        query = """
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                PREFIX focu: <http://focu.io/schema#>
                PREFIX focudata: <http://focu.io/data#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX ex: <http://example.org/>
                
                SELECT DISTINCT ?courseNumber ?courseName ?topicLabel ?topicURL ?lab ?slide ?worksheet (COUNT(?topic) as ?occurrences)
                WHERE {
                
                  ?topic a focu:topic ;
                  rdfs:label ?topicLabel ;
                  rdfs:seeAlso ?topicURL .
                
                  ?course a focu:Course ;
                  focu:courseNumber ?courseNumber ;
                  focu:courseSubject ?courseSubject ;
                  focu:courseName ?courseName ;
                  focu:coversTopic ?topic.
                
                  {
                  ?lab a focu:Lab;
                  focu:coversTopic ?topic.}
                
                   FILTER(?topicLabel = "%s")
                }
                
                GROUP BY ?courseNumber ?courseName ?topicLabel ?topicURL ?lab ?slide ?worksheet
                ORDER BY DESC(?topic)
        """ % topic
        try:
            response = requests.post('http://localhost:3030/play/sparql', data={'query': query})
            response_json = response.json()
            if response_json.get('results') and response_json['results'].get('bindings'):
                results = response_json['results']['bindings']
                dispatcher.utter_message(
                    text=f"Find below detailed course contents")
                for result in results:
                    courseName = ''
                    courseSubject = ''
                    courseNumber = ''
                    lab = ''
                    slide = ''
                    worksheet = ''

                    for key in result:
                        if key == "courseName":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    courseName = result[key][innerKey]
                        if key == "courseSubject":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    courseSubject = result[key][innerKey]
                        if key == "courseNumber":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    courseNumber = result[key][innerKey]
                        if key == "lab":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    lab = result[key][innerKey]
                        if key == "slide":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    slide = result[key][innerKey]
                        if key == "worksheet":
                            for innerKey in result[key]:
                                if innerKey == "value":
                                    worksheet = result[key][innerKey]


                    labString = lab.split('/')  if len(lab) > 0 else ''
                    slideString = slide.split('/') if len(slide) > 0 else ''
                    worksheetString = worksheet.split('/') if len(worksheet) > 0 else ''

                    # dispatcher.utter_message(text=f"{slideString[len(slideString) - 1]}")
                    dispatcher.utter_message(text=f"CourseName: {courseName}\n"
                                                  f"CourseCode: {courseSubject}{courseNumber}\n"
                                                  f"{labString[len(labString) - 1] if + len(labString) > 0 else ''}\n"
                                                  f"{slideString[len(slideString) - 1] if len(slideString) > 0  else ''}\n"
                                                  f"{worksheetString[len(worksheetString) - 1] if len(worksheetString) > 0  else ''}\n")

            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find course information in Concordia University")
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f"Encountered an error while fetching data: {e}")
        return []


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Hello World!")

        return []


class ActionPersonInfo(Action):

    def name(self):
        return "action_person_info"

    def run(self, dispatcher, tracker, domain):
        person_name = tracker.get_slot('person')
        print("person_name:   "+person_name)
        query = """
        PREFIX dbo: <http://dbpedia.org/ontology/>
        SELECT ?description WHERE {
        ?person dbo:birthName '""" + person_name + """'@en.
        ?person dbo:abstract ?description .
            FILTER (lang(?description) = 'en')
        }
        LIMIT 1
        """
        try:
            print("FUCKING QUERY::\n" + query)
            response = requests.post('http://localhost:3030/play/sparql', data={'query': query})
            response_json = response.json()
            if response_json.get('results') and response_json['results'].get('bindings'):
                description = response_json['results']['bindings'][0]['description']['value']
                print("response_json['results']['bindings'][0]\n" + str(response_json['results']['bindings'][0]))
                dispatcher.utter_message(text=f"Here's what I found about {person_name}: {description}")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find information about {person_name}")
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f"Encountered an error while fetching data: {e}")
