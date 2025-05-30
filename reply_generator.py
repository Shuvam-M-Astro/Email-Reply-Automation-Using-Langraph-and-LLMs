from graph_builder import build_email_graph

def generate_reply(email_data):
    graph = build_email_graph()
    result = graph.invoke({"email_body": email_data["email_body"]})

    # Extract the fields from the result dictionary
    category = result["category"]
    intent = result["intent"]
    entities = result["entities"]
    reply = result["reply"]

    return category, intent, entities, reply
