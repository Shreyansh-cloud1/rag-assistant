# Text Embedding:
from sentence_transformers import SentenceTransformer
# Imports the SentenceTransformer class from the sentence-transformers library.
# This library provides pre-trained models that convert text into numerical vectors
# called embeddings, which capture the semantic meaning of the text.


model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
# Loads the pre-trained embedding model named "all-MiniLM-L6-v2" from Hugging Face.
# This model:
# - Converts text into 384-dimensional vectors.
# - Is lightweight and fast.
# - Works well for semantic search and RAG applications.
# - Runs efficiently on CPU.
#
# On the first run, the model is downloaded and cached locally.
# On subsequent runs, it is loaded from the local cache.


def embed_text(text: str):
    # Defines a function named embed_text.
    # Returns:
    # A Python list of 384 floating-point numbers representing the text.


    return model.encode(text).tolist()
    # model.encode(text)
    # Converts the input text into a NumPy array containing the embedding vector.
    # tolist() converts it into a list.
    #
    # This list can be:
    # - Stored in a vector database such as Chroma, FAISS, or PostgreSQL with pgvector.
    # - Compared with other embeddings using cosine similarity.
    # - Used for semantic search in a RAG system.

 
# Chunking strategy:
# This function splits a large text into smaller overlapping chunks.
# Chunking is essential in RAG systems because embedding models and LLMs
# work better with smaller pieces of text rather than very large documents.
from langchain_text_splitters import RecursiveCharacterTextSplitter
def chunk_text(text, chunk_size=1000, chunk_overlap=200):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)



# PDF Extraction:
import fitz
# Imports the fitz module from the PyMuPDF library.


def extract_pdf_text(path):
    # Defines a function named extract_pdf_text.
    # Returns:
    #   A single string containing all text extracted from every page
    #   in the PDF, with each page separated by a newline character.


    doc = fitz.open(path)
    # Opens the PDF file located at the specified path.
    

    return "\n".join(page.get_text() for page in doc)
    # Iterates through every page in the PDF document.
    #
    # For each page:
    #   page.get_text()
    #   extracts all text content from that page as a string.

    # The generator expression:
    #   (page.get_text() for page in doc)
    # produces the text of each page one by one.
    
    # "\n".join(...)
    # combines all page texts into a single string, inserting a newline
    # between each page.
    
    # This combined text is ideal for:
    # - Chunking into smaller pieces
    # - Creating embeddings
    # - Storing in a vector database
    # - Performing semantic search in a RAG application



# Insert Chunks into PostgreSQL:
from sqlalchemy import text
# Imports the text() function from SQLAlchemy.
# text() allows us to write raw SQL statements as strings and execute them safely.

from app.db import engine
# Imports the SQLAlchemy Engine object from the app.db module.
# This engine is used to open connections and execute SQL statements.

def insert_chunk(source, chunk_index, content, embedding):
    # Defines a function named insert_chunk.
    #
    # Purpose:
    #   Inserts one document chunk and its embedding into the documents table.
    #
    # Parameters:
    #   source
    #       The name of the source file (e.g., "manual.pdf").
    #
    #   chunk_index
    #       The position of the chunk within the source document.
    #       Example: 0, 1, 2, ...
    #
    #   content
    #       The actual text content of the chunk.
    #
    #   embedding
    #       The vector representation of the chunk.
    #       Usually a Python list of floating-point numbers generated
    #       by an embedding model.
    
    with engine.begin() as conn:
        # Opens a database connection and starts a transaction.
        #
        # engine.begin() provides:
        # - Automatic transaction management
        # - Automatic commit if all operations succeed
        # - Automatic rollback if an error occurs
        #
        # conn is a Connection object used to execute SQL commands.

        conn.execute(
            # Executes the SQL statement below using the provided parameters.

            text("""
                INSERT INTO documents (
                    source,
                    chunk_index,
                    content,
                    embedding
                )
                VALUES (
                    :source,
                    :chunk_index,
                    :content,
                    :embedding
                )
            """),
            # Converts the multi-line SQL string into a SQLAlchemy TextClause object.
            #
            # SQL Explanation:
            #   INSERT INTO documents (...)
            #   Adds a new row to the documents table.
            #
            # Columns:
            # - source: Name of the original document
            # - chunk_index: Position of the chunk
            # - content: Chunk text
            # - embedding: Vector representation
            #
            # Named placeholders:
            # - :source
            # - :chunk_index
            # - :content
            # - :embedding
            #
            # SQLAlchemy safely replaces these placeholders with actual values.

            {
                "source": source,
                # Binds the Python variable 'source' to the SQL parameter :source.

                "chunk_index": chunk_index,
                # Binds the Python variable 'chunk_index'
                # to the SQL parameter :chunk_index.

                "content": content,
                # Binds the Python variable 'content'
                # to the SQL parameter :content.

                "embedding": embedding,
                # Binds the Python variable 'embedding'
                # to the SQL parameter :embedding.
                #
                # If the database column type is VECTOR (pgvector),
                # SQLAlchemy stores this list as a vector.

            },
        )
        # Executes the INSERT statement with the parameter values.
        #
        # If successful:
        # - A new row is inserted into the documents table.
        # - The transaction is committed automatically.
        #
        # If an error occurs:
        # - The transaction is rolled back automatically.
        # - No partial data is saved.