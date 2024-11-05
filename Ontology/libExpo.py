from rdflib import Graph, RDF, RDFS, OWL, URIRef

# Load the RDF file
g = Graph()
g.parse("/home/muhsin/Desktop/AI-Assignment/Ontology/library.rdf")

print("Ontology loaded with", len(g), "statements.")

# List classes
def list_classes(graph):
    print("\nClasses in the ontology:")
    for s in graph.subjects(RDF.type, OWL.Class):
        class_name = s.split('#')[-1] if '#' in s else s.split('/')[-1]
        print(f" - {class_name}")

# List object properties
def list_object_properties(graph):
    print("\nObject properties in the ontology:")
    for s in graph.subjects(RDF.type, OWL.ObjectProperty):
        property_name = s.split('#')[-1] if '#' in s else s.split('/')[-1]
        print(f" - {property_name}")

# List data properties
def list_data_properties(graph):
    print("\nData properties in the ontology:")
    for s in graph.subjects(RDF.type, OWL.DatatypeProperty):
        property_name = s.split('#')[-1] if '#' in s else s.split('/')[-1]
        print(f" - {property_name}")

# List individuals
def list_individuals(graph):
    print("\nIndividuals in the ontology:")
    for s in graph.subjects(RDF.type, OWL.NamedIndividual):
        individual_name = s.split('#')[-1] if '#' in s else s.split('/')[-1]
        print(f" - {individual_name}")

# Run the exploration functions
list_classes(g)
list_object_properties(g)
list_data_properties(g)
list_individuals(g)
