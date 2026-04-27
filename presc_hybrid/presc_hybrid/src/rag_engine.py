import os
from typing import List
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from rank_bm25 import BM25Okapi
import numpy as np

class MedicalRAGEngine:
    def __init__(self, persist_dir: str = "./data/chroma_db"):
        self.embedding_function = SentenceTransformerEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        self.persist_dir = persist_dir
        self.vector_store = None
        self.bm25 = None
        self.documents = []  # Keep track of docs for BM25
        
        # Initialize or load vector store
        if not os.path.exists(persist_dir):
            os.makedirs(persist_dir)
            
        self.vector_store = Chroma(
            persist_directory=self.persist_dir,
            embedding_function=self.embedding_function
        )

    def ingest_text(self, text: str, source: str = "knowledge_base"):
        """Ingest text into the RAG system."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        docs = text_splitter.create_documents([text], metadatas=[{"source": source}])
        
        # Add to Vector Store
        self.vector_store.add_documents(docs)
        self.vector_store.persist()
        
        # Update BM25 (re-build index - simple approach for small scale)
        # Ideally, you'd load existing docs, but for this demo we'll just track new ones 
        # or rely on what's passed in this session if not persisting BM25 separately.
        # For a robust system, BM25 index should also be serialized. 
        # Here we will just perform vector search if BM25 isn't ready, or rebuild.
        self.documents.extend([d.page_content for d in docs])
        tokenized_corpus = [doc.split(" ") for doc in self.documents]
        self.bm25 = BM25Okapi(tokenized_corpus)

    def retrieve(self, query: str, k: int = 3) -> List[str]:
        """Hybrid retrieval: Vector + Keyword."""
        # 1. Vector Search
        vector_results = self.vector_store.similarity_search(query, k=k)
        vector_docs = [doc.page_content for doc in vector_results]
        
        # 2. Keyword Search (BM25)
        keyword_docs = []
        if self.bm25:
             keyword_docs = self.bm25.get_top_n(query.split(" "), self.documents, n=k)
        
        # 3. Combine and Deduplicate
        all_docs = list(set(vector_docs + keyword_docs))
        
        # Return top k after combination (simplified)
        return all_docs[:k]

# Simple singleton or factory if needed, but class is fine.
