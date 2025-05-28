from graph_builder import build_email_graph

def generate_reply(email_data):
    graph = build_email_graph()
    result = graph.invoke({"email_body": email_data["email_body"]})
    
    # result is of type EmailState or dict-like
    return result["reply"]  # ✅ access the reply string from the result
