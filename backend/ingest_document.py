"""Ingest a text document into the institution-specific ChromaDB collection.

Run from the project root:
python -m backend.ingest_document --institution-id 1 --file data/admission_policy.txt --document-id admission-policy --version 1
"""
import argparse
from pathlib import Path

from .chroma_store import collection

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 80):
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and smaller than chunk_size")

    chunks = []
    start = 0
    while start < len(text):
        chunk = text[start:start + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--institution-id", required=True)
    parser.add_argument("--file", required=True)
    parser.add_argument("--document-id", required=True)
    parser.add_argument("--version", default="1")
    args = parser.parse_args()

    file_path = Path(args.file)
    if not file_path.is_file():
        raise FileNotFoundError(f"Document not found: {file_path}")

    text = file_path.read_text(encoding="utf-8")
    chunks = chunk_text(text)
    if not chunks:
        raise ValueError("The document is empty.")

    ids = [
        f"{args.institution_id}_{args.document_id}_{args.version}_chunk_{i}"
        for i in range(len(chunks))
    ]
    metadatas = [
        {
            "institution_id": str(args.institution_id),
            "document_id": args.document_id,
            "document_version": str(args.version),
            "source": file_path.name,
            "chunk_index": i,
        }
        for i in range(len(chunks))
    ]

    collection.upsert(ids=ids, documents=chunks, metadatas=metadatas)
    print(f"Successfully indexed {len(chunks)} chunks for institution ID {args.institution_id}.")

if __name__ == "__main__":
    main()
