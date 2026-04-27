try:
    from langchain_community.vectorstores import Chroma
    print("Imported Chroma")
    from langchain_community.embeddings import SentenceTransformerEmbeddings
    print("Imported SentenceTransformerEmbeddings")
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    print("Imported RecursiveCharacterTextSplitter")
    from langchain_core.documents import Document
    print("Imported Document")
    print("All imports successful!")
except ImportError as e:
    print(f"Import failed: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
