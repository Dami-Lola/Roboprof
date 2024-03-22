# RDF data
from rdflib import Graph, Literal, RDF, URIRef, Namespace
if __name__ == '__main__':
    rdf_data = """
    @prefix focu: <http://focu.io/schema#> .
    @prefix focudata: <http://focu.io/data#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix ex: <http://example.org/> .
    
    ex:AyakaKamisotu a focu:Student ;
        focu:studentEmail "ayakakamisotu@live.concordia.ca" ;
        focu:studentID "12346" ;
        focu:studentName "Ayaka Kamisotu" ;
        focu:completedCourse [
            focu:courseCode focudata:COMP6721 ;
            focu:gradeAchieved "A" ;
            focu:competencyInTopic focudata:Alpha_Beta_Pruning,
                                   focudata:Artificial_Intelligence,
                                   focudata:Artificial_Neural_Networks,
                                   focudata:Decision_Trees
        ],
        [
            focu:courseCode focudata:COMP6741 ;
            focu:gradeAchieved "B+" ;
            focu:competencyInTopic focudata:Intelligent_Agents,
                                   focudata:Intelligent_Systems,
                                   focudata:Introduction_to_Machine_Learning
        ],
        [
            focu:courseCode focudata:COMP691 ;
            focu:gradeAchieved "A-"
        ],
        [
            focu:courseCode focudata:COMS205 ;
            focu:gradeAchieved "B"
        ],
        [
            focu:courseCode focudata:COMS276 ;
            focu:gradeAchieved "C"
        ],
        [
            focu:courseCode focudata:COMS284 ;
            focu:gradeAchieved "C-"
        ].
    
    ex:RaidenShogun a focu:Student ;
        focu:studentEmail "raidenshogun@live.concordia.ca" ;
        focu:studentID "12348" ;
        focu:studentName "Raiden Shogun" ;
        focu:completedCourse [
            focu:courseCode focudata:COMP6721 ;
            focu:gradeAchieved "B+" ;
            focu:competencyInTopic focudata:Deep_Learning_CNNs,
                                   focudata:Deep_Learning_NLP,
                                   focudata:Deep_Learning_for_NLP,
                                   focudata:Intelligent_Agents
        ],
        [
            focu:courseCode focudata:COMP6741 ;
            focu:gradeAchieved "B+" ;
            focu:competencyInTopic focudata:Knowledge_Base_Queries,
                                   focudata:Knowledge_Graphs,
                                   focudata:Linked_Open_Data
        ],
        [
            focu:courseCode focudata:COMP691 ;
            focu:gradeAchieved "C-"
        ],
        [
            focu:courseCode focudata:COMS205 ;
            focu:gradeAchieved "C"
        ],
        [
            focu:courseCode focudata:COMS276 ;
            focu:gradeAchieved "A"
        ],
        [
            focu:courseCode focudata:COMS284 ;
            focu:gradeAchieved "A-"
        ].
    
    ex:SaraKujou a focu:Student ;
        focu:studentEmail "sarakujou@live.concordia.ca" ;
        focu:studentID "12345" ;
        focu:studentName "Sara Kujou" ;
        focu:completedCourse [
            focu:courseCode focudata:COMP6721 ;
            focu:gradeAchieved "A+" ;
            focu:competencyInTopic focudata:Naive_Bayes_Classification,
                                   focudata:Neural_Networks,
                                   focudata:SPARQL,
                                   focudata:k_means_Clustering
        ],
        [
            focu:courseCode focudata:COMP6741 ;
            focu:gradeAchieved "A+" ;
            focu:competencyInTopic focudata:Recommender_Systems,
                                   focudata:Text_Mining,
                                   focudata:Vocabularies_Ontologies
        ],
        [
            focu:courseCode focudata:COMP890 ;
            focu:gradeAchieved "A-"
        ],
        [
            focu:courseCode focudata:COMS300 ;
            focu:gradeAchieved "B"
        ],
        [
            focu:courseCode focudata:ELEC390 ;
            focu:gradeAchieved "B"
        ],
        [
            focu:courseCode focudata:FMAN225 ;
            focu:gradeAchieved "B-"
        ].
    
    ex:ShinobuKuki a focu:Student ;
        focu:studentEmail "shinobukuki@live.concordia.ca" ;
        focu:studentID "12347" ;
        focu:studentName "Shinobu Kuki" ;
        focu:completedCourse [
            focu:courseCode focudata:COMS274 ;
            focu:gradeAchieved "A+"
        ],
        [
            focu:courseCode focudata:COMS354 ;
            focu:gradeAchieved "A-"
        ],
        [
            focu:courseCode focudata:COMS398 ;
            focu:gradeAchieved "B+"
        ],
        [
            focu:courseCode focudata:COMS442 ;
            focu:gradeAchieved "B+"
        ],
        [
            focu:courseCode focudata:COMS499 ;
            focu:gradeAchieved "A-"
        ],
        [
            focu:courseCode focudata:COMS672 ;
            focu:gradeAchieved "A-"
        ].
    
    ex:YunJin a focu:Student ;
        focu:studentEmail "yunjin@live.concordia.ca" ;
        focu:studentID "12349" ;
        focu:studentName "Yun Jin" ;
        focu:completedCourse [
            focu:courseCode focudata:FLIZ230 ;
            focu:gradeAchieved "A+"
        ],
        [
            focu:courseCode focudata:FMAN256 ;
            focu:gradeAchieved "A-"
        ],
        [
            focu:courseCode focudata:FMAN308 ;
            focu:gradeAchieved "A"
        ],
        [
            focu:courseCode focudata:FMAN311 ;
            focu:gradeAchieved "A"
        ],
        [
            focu:courseCode focudata:FMAN398 ;
            focu:gradeAchieved "A-"
        ],
        [
            focu:courseCode focudata:FMPR435 ;
            focu:gradeAchieved "A+"
        ].
    """

    g = Graph()
    g.parse(data=rdf_data, format="turtle")
    g.serialize('studentN3.ttl', format='nt')
