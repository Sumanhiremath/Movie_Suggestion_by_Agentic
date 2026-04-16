# 🎬 Movie Recommendation System using Agentic RAG

## 🚀 Overview

This project is an **Agentic AI-powered Movie Recommendation System** built using **LangChain + LangGraph + Vector Database (Chroma)**.

It uses a **Retrieval-Augmented Generation (RAG)** approach combined with an **LLM-based planner** to intelligently answer user queries like:

* *"Tom Hardy movies"*
* *"Action movies"*

---

## 🧠 Key Features

* 📄 Extracts structured movie data from PDF
* 🔍 Semantic search using vector embeddings
* 🎯 Metadata filtering (Genre, Cast)
* 🤖 LLM-powered query classification (Agentic behavior)
* 🔗 Multi-step reasoning using LangGraph
* ⚡ Fast retrieval using Chroma DB

---

## 🏗️ Architecture

User Query → Planner (LLM) → Tool Selection → Vector DB / Filters → Response Generator

### Flow:

1. **Planner Node (LLM)**

   * Classifies query into:

     * `GENRE`
     * `CAST`
     * `BOTH`

2. **Tool Node**

   * Calls appropriate function:

     * `search_by_genre`
     * `search_by_cast`
     * Combined filtering

3. **Response Node**

   * Formats final output

---

## 🧩 Tech Stack

* **LangChain** – Document loading & embeddings
* **LangGraph** – Agent workflow orchestration
* **Chroma DB** – Vector database
* **HuggingFace Embeddings** – Semantic understanding
* **Ollama (LLaMA 3.1)** – Local LLM
* **Python** – Core implementation

---

## 📂 Project Structure

```
Movie_Suggestion_by_Agents/
│
├── movie_genre_dataset_production.pdf
├── movie_db/                  # Chroma DB storage
├── main.py                    # Core pipeline
├── README.md
└── requirements.txt
```

---

## ⚙️ How It Works

### 1️⃣ Data Processing

* Loads PDF using `PyPDFLoader`
* Extracts:

  * Title
  * Year
  * Genre
  * Cast
  * Description

### 2️⃣ Chunk Creation

Each movie is converted into:

```
"Title. Description. Genre: X. Cast: A, B"
```

### 3️⃣ Embedding + Storage

* Uses `sentence-transformers/all-MiniLM-L6-v2`
* Stores in **Chroma DB**

### 4️⃣ Query Processing

* LLM classifies query
* System routes to correct search logic

---

## 🔎 Example Queries

| Query                           | Output Type     |
| ------------------------------- | --------------- |
| "Action movies"                 | Genre-based     |
| "Tom Hardy movies"              | Cast-based      |
| "Crime movies with Al Pacino"   | Combined        |

---

## 🧠 Agent Logic

The planner uses strict rules:

```
GENRE:<genre>
CAST:<actor>
BOTH:<genre>:<actor>
```

This ensures:

* ✅ Deterministic routing
* ✅ High accuracy

---

## ▶️ How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start Ollama

```bash
ollama run llama3.1:8b
```

### 3. Run the script

```bash
python rag_mv_sg.ipynb
```

---

## 📊 Example Output

```
Query: Crime movies

Here are some movies you might like:
- Pulp Fiction 
- Goodfellas  
- Scarface  
- Departed 
```

---

## 💡 Key Learnings

* How RAG systems work in production
* Vector database design
* Agent-based decision making
* Avoiding hallucination using structured routing

---

## 👩‍💻 Author

**Suman Hiremath**

---

## ⭐ If you like this project

Give it a star on GitHub!
