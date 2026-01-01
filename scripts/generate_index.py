import os
import json
import re

BASE_DIR = "scholars"
OUTPUT = "data/index.json"

def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")

books = []
scholars = []
book_counter = 1

if os.path.exists(BASE_DIR):
    for scholar_folder in sorted(os.listdir(BASE_DIR)):
        scholar_path = os.path.join(BASE_DIR, scholar_folder)
        if not os.path.isdir(scholar_path):
            continue

        scholar_books = []

        for book_folder in sorted(os.listdir(scholar_path)):
            book_path = os.path.join(scholar_path, book_folder)
            if not os.path.isdir(book_path):
                continue

            pdfs = sorted(
                f for f in os.listdir(book_path)
                if f.lower().endswith(".pdf")
            )

            # ❌ No PDFs → skip book
            if not pdfs:
                continue

            book_id = f"b-{book_counter}"
            book_counter += 1

            volume_paths = [
                f"{BASE_DIR}/{scholar_folder}/{book_folder}/{pdf}"
                for pdf in pdfs
            ]

            books.append({
                "id": book_id,
                "title": book_folder.replace("-", " ").title(),
                "author": scholar_folder.replace("-", " ").title(),
                "coverUrl": f"assets/books/{slugify(book_folder)}.jpg",
                "pdfUrl": volume_paths[0],
                "rating": 4.5,
                "pages": 300,
                "volumes": volume_paths
            })

            scholar_books.append(book_id)

        # ❌ Scholar with NO books → skip scholar
        if not scholar_books:
            continue

        scholars.append({
            "id": f"s-{slugify(scholar_folder)}",
            "name": scholar_folder.replace("-", " ").title(),
            "bio": "Islamic scholar and author",
            "avatarUrl": f"assets/scholars/{slugify(scholar_folder)}.png",
            "books": scholar_books
        })

# 🔥 Build final JSON ONLY with existing data
library = {}
if books:
    library["books"] = books
if scholars:
    library["scholars"] = scholars

os.makedirs("data", exist_ok=True)
with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(library, f, ensure_ascii=False, indent=2)

print("✅ index.json generated (only real data included)")
