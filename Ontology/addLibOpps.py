from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF

# Load RDF graph
rdf_path = "/home/muhsin/Desktop/AI-Assignment/Ontology/library.rdf"

g = Graph()
g.parse(rdf_path)

LIB = Namespace("http://www.semanticweb.org/muhsin/ontologies/2024/9/library#")


def add_entity(graph, entity_type, entity_name, properties):
    """
    Adds a new entity to the RDF graph.
    
    Parameters:
    - graph: The RDF graph to modify.
    - entity_type: The type of entity to add (e.g., 'Books').
    - entity_name: The name for the new entity (e.g., 'NewBookTitle').
    - properties: A dictionary of properties to add with the entity, 
                  where keys are property names and values are property values.
                  
    Returns:
    - URI of the newly added entity.
    """
    # Create a new URI for the entity
    entity_uri = LIB[entity_name.replace(" ", "_")]
    
    graph.add((entity_uri, RDF.type, LIB[entity_type]))
    
    # Add each property to the entity
    for prop_name, prop_value in properties.items():
        prop_uri = LIB[prop_name]
        graph.add((entity_uri, prop_uri, Literal(prop_value)))
    
    return entity_uri


def list_loan_options(graph, material_type):
    """
    Lists loan options for a given type of material (e.g., 'Books', 'DVDs').
    
    Parameters:
    - graph: The RDF graph to search.
    - material_type: The type of material to list loan options for (e.g., 'Books').
    
    Returns:
    - A list of dictionaries with loan options for each instance of the specified material type.
    """
    loan_options = []
    
    for subject in graph.subjects(RDF.type, LIB[material_type]):
        # Dictionary to store loan details for each material instance
        material_loan_info = {"Material": str(subject)}
        
        # Check for loan-related properties (e.g., loanTime)
        for prop, value in graph.predicate_objects(subject):
            prop_name = prop.split("#")[-1]
            if "loan" in prop_name.lower():
                material_loan_info[prop_name] = str(value)
        
        if len(material_loan_info) > 1:  # More than just 'Material' key
            loan_options.append(material_loan_info)
    
    return loan_options


# Example usage:
if __name__ == "__main__":
    # Define properties for a new book entity
    book_properties = {
        "ISBM": "099-3-16-276345-0",
        "Author": "Sharifah ",
        "Title": "Introduction to Python",
        "loanTime": "30 days"
                
    }
    
    # Add a new book entity to the RDF graph
    new_book_uri = add_entity(g, "Books", "Conflict Harbits", book_properties)
    print(f"Added new book: {new_book_uri}")
    
    # Retrieve and print loan options for "Books"
    book_loan_options = list_loan_options(g, "Books")
    print("\nLoan options for Books:")
    for option in book_loan_options:
        print(option)
    
    # Optionally, save changes back to the RDF file
    g.serialize(destination=rdf_path, format="xml")
    print(f"\nChanges saved to {rdf_path}")
