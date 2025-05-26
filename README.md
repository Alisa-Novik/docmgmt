# EB-1 Letter Generator

This repository contains a minimal setup for generating draft recommendation letters using your local documents as a knowledge base.

## Structure

- `knowledge_base/` — store text files with drafts, resume excerpts, thesis summaries, quotes, etc.
- `build_index.py` — indexes documents into a local FAISS database.
- `generate_letter.py` — generates a draft letter using the indexed documents and a language model.
- `drafts/` — suggested folder for saving generated letters.

## Requirements

Install dependencies:

```bash
pip install langchain openai faiss-cpu tiktoken python-docx
```

If you want to run without OpenAI, replace `OpenAIEmbeddings` with `sentence-transformers` and use a local model.

## Configuration

Copy `.env.example` to `.env` and replace `your-api-key` with your OpenAI API key:

```bash
cp .env.example .env
# edit .env and set your real key
```

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

The script writes the generated letter to `letters/letter.txt`.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
