# EB-1 Letter Generator

This repository contains a minimal setup for generating draft recommendation letters using your local documents as a knowledge base.

## Structure

- `knowledge_base/` — store text files with drafts, resume excerpts, thesis summaries, quotes, etc.
- `build_index.py` — indexes documents into a local FAISS database.
- `generate_letter.py` — generates a draft letter using the indexed documents and a language model.
- `drafts/` — suggested folder for saving generated letters.

The repository includes a few example documents inside `knowledge_base/` so
the tools work out of the box. Feel free to replace or delete these files.
If your own documents contain sensitive information, consider expanding
`.gitignore` to exclude them from commits.

## Requirements

Install dependencies:

```bash
pip install langchain openai faiss-cpu tiktoken
```

If you want to run without OpenAI, replace `OpenAIEmbeddings` with `sentence-transformers` and use a local model.

## Usage

1. Populate `knowledge_base/` with your source documents.
2. Run the indexer once:

```bash
python build_index.py
```

3. Generate a draft letter:

```bash
python generate_letter.py
```

The script prints the draft to stdout. You can modify the parameters in `generate_letter.py` or extend the code to save outputs in `drafts/`.
