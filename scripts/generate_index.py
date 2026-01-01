import os
import json

BASE_DIR = "scholars"
OUTPUT = "data/index.json"

library = {"scholars": []}

for scholar_name in sorted(os.listdir(BASE_DIR)):
    scholar_path = os.path.join(BASE_DIR, scholar_name)
    if not os.path.isdir(scholar_path):
        continue

    scholar = {
        "id": scholar_name.lower().replace(" ", "-"),
        "name": scholar_name,
        "books": []
    }

    # Treat PDFs directly under scholar as ONE book
    pdfs = [f for f in os.listdir(scholar_path) if f.lower().endswith(".pdf")]

    if pdfs:
        book = {
            "title": "Collected Works",
            "volumes": []
        }

        for pdf in sorted(pdfs):
            book["volumes"].append({
                "title": pdf.replace(".pdf", ""),
                "pdf": f"{BASE_DIR}/{scholar_name}/{pdf}"
            })

        scholar["books"].append(book)

    library["scholars"].append(scholar)

os.makedirs("data", exist_ok=True)
with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(library, f, ensure_ascii=False, indent=2)

print("index.json generated")
