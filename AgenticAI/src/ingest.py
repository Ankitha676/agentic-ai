import os
import pandas as pd
from docx import Document
import pymupdf4llm
from src.config import DATA_DIR

def load_pdf(path):
    return pymupdf4llm.to_markdown(path)


def load_docx(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs])


def load_csv(path):
    df = pd.read_csv(path)
    return df.to_string(), df


def load_excel(path):
    df = pd.read_excel(path)
    return df.to_string(), df


def ingest_data():
    documents = []
    structured_data = []

    for root, _, files in os.walk(DATA_DIR):
        for file in files:
            path = os.path.join(root, file)
            folder = os.path.basename(root)

            try:
                if file.endswith(".pdf"):
                    text = load_pdf(path)
                    documents.append((text, {"source": file, "type": "pdf", "folder": folder}))

                elif file.endswith(".docx"):
                    text = load_docx(path)
                    documents.append((text, {"source": file, "type": "docx", "folder": folder}))

                elif file.endswith(".csv"):
                    text, df = load_csv(path)
                    documents.append((text, {"source": file, "type": "csv", "folder": folder}))
                    structured_data.append((df, file, folder))

                elif file.endswith(".xlsx"):
                    text, df = load_excel(path)
                    documents.append((text, {"source": file, "type": "excel", "folder": folder}))
                    structured_data.append((df, file, folder))

            except Exception as e:
                print(f"⚠️ Error processing {file}: {e}")

    print(f"✅ Documents: {len(documents)}")
    print(f"✅ Structured datasets: {len(structured_data)}")

    return documents, structured_data