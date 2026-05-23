from app.ingest import extract_pdf_text, chunk_text, embed_text
from app.db import engine
from sqlalchemy import text
import sys

pdf_path = sys.argv[1]
text_data = extract_pdf_text(pdf_path)
chunks = chunk_text(text_data)

with engine.begin() as conn:
    for i, chunk in enumerate(chunks):
        embedding = embed_text(chunk)
        conn.execute(
            text(
                "INSERT INTO documents (source, chunk_index, content, embedding) "
                "VALUES (:source, :chunk_index, :content, :embedding)"
            ),
            {
                "source": pdf_path,
                "chunk_index": i,
                "content": chunk,
                "embedding": embedding,
            },
        )

print(f"Inserted {len(chunks)} chunks")
