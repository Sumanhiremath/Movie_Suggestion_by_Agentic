from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOllama
from langgraph.graph import StateGraph
import re


# -----------------------------
# 🔹 BUILD GRAPH FUNCTION
# -----------------------------
def create_graph():

    llm = ChatOllama(
        model="llama3.1:8b",
        temperature=0
    )


    loader = PyPDFLoader("c:/Users/Suman/Downloads/movie_genre_dataset_production.pdf")
    docs = loader.load()

    current_genre = None


    chunks = []

    for doc in docs:
        lines = doc.page_content.split("\n")
        current_genre = None

        for line in lines:
            if "Genre:" in line:
                current_genre = line.replace("Genre:", "").strip()

            elif line.startswith("-"):
                # Example line:
                # - Mad Max: Fury Road (2015) | Cast: Tom Hardy, Charlize Theron — Desc
                
                # Extract title + year
                title_year = re.search(r"- (.*?) \((\d{4})\)", line)
                title = title_year.group(1)
                year = int(title_year.group(2))

                # Extract cast
                cast_match = re.search(r"Cast: (.*?) —", line)
                cast = [c.strip() for c in cast_match.group(1).split(",")]

                # Extract description
                desc_match = re.search(r"— (.*)", line)
                description = desc_match.group(1)

                # Clean text for embedding
                text = f"{title}. {description}. Genre: {current_genre}. Cast: {', '.join(cast)}"

                chunks.append({
                    "text": text,
                    "metadata": {
                        "title": title,
                        "genre": current_genre,
                        "cast": cast,
                        "year": year
                    }
                })


    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    documents = [
        Document(page_content=c["text"], metadata=c["metadata"])
        for c in chunks
    ]

    db = Chroma(
    persist_directory="./movie_db",
    embedding_function=embedding
    )


    def search_by_genre(genre: str):
        genre = genre.lower().strip()

        data = db.get()

        results = []
        for meta in data["metadatas"]:
            meta_genre = meta.get("genre")

            # ✅ skip bad entries
            if not meta_genre:
                continue

            # ✅ normalize
            meta_genre = str(meta_genre).lower().strip()

            # ✅ flexible match
            if genre in meta_genre:
                results.append(meta.get("title"))

        return list(dict.fromkeys(results))



    def search_by_cast(cast_name: str):
        cast_name = cast_name.lower().strip()

        data = db.get()   # ✅ get ALL documents

        results = []

        for meta in data["metadatas"]:
            cast_list = meta.get("cast", [])

            # normalize at runtime (no chunk change)
            cast_list = [c.lower().strip() for c in cast_list]

            if cast_name in cast_list:
                results.append(meta.get("title"))

        return list(dict.fromkeys(results))[:10]


    def planner(query):
        prompt = f"""
    You are a strict classifier.

    Rules:
    - If query contains a PERSON NAME → return CAST
    - If query contains a GENRE → return GENRE
    - If BOTH present → return BOTH

    Examples:
    "Tom Hardy movies" → CAST:Tom Hardy
    "movies of Tom Hardy" → CAST:Tom Hardy
    "action movies" → GENRE:action
    "romance movies with Shah Rukh Khan" → BOTH:romance:Shah Rukh Khan

    Output ONLY one line:
    GENRE:<genre>
    CAST:<actor>
    BOTH:<genre>:<actor>

    NO explanation.

    Query: {query}
    """

        response = llm.invoke(prompt)
        raw = response.content.strip()

        print("🧠 LLM RAW OUTPUT:", raw)

        return raw.split("\n")[0]


    def planner_node(state):
        decision = planner(state["query"])

        state["decision"] = decision
        print("planner_node",state["decision"])
        return state


    def tool_node(state):
        decision = state.get("decision", "")
        print(decision)
        query = state.get("query", "")


        results = []  # ✅ always initialize

        try:
            if decision.startswith("GENRE"):
                parts = decision.split(":")
                if len(parts) >= 2:
                    genre = parts[1].strip()
                    results = search_by_genre(genre)

            elif decision.startswith("CAST"):
                parts = decision.split(":")
                if len(parts) >= 2:
                    cast = parts[1].strip().lower()
                    results = search_by_cast(cast)


            elif decision.startswith("BOTH"):
                parts = decision.split(":")
                if len(parts) >= 3:
                    _, genre, cast = parts[:3]

                    genre = genre.strip().lower()
                    cast = cast.strip().lower()

                    data = db.get()

                    results = []
                    for meta in data["metadatas"]:
                        meta_genre = str(meta.get("genre", "")).lower()
                        cast_list = [c.lower() for c in meta.get("cast", [])]

                        if genre in meta_genre and cast in cast_list:
                            results.append(meta.get("title"))

                    results = list(dict.fromkeys(results))


            else:
                # ✅ fallback: semantic search
                docs = db.similarity_search(query, k=5)
                results = [r.metadata.get("title", "") for r in docs]

        except Exception as e:
            print("ERROR in tool_node:", e)
            results = []

        state["results"] = results
        return state


    def response_node(state):
        results = state["results"]
        print(results)
        
        return {
            "response": f"Here are some movies you might like:\n" + "\n".join(results)
        }




    builder = StateGraph(dict)

    builder.add_node("planner", planner_node)
    builder.add_node("tool", tool_node)
    builder.add_node("response", response_node)

    builder.set_entry_point("planner")

    builder.add_edge("planner", "tool")
    builder.add_edge("tool", "response")

    graph = builder.compile()


    return graph


graph = create_graph()