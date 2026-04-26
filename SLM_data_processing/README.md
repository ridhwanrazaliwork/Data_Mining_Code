Hugging Face Sentiment Pipeline

This folder contains a notebook and minimal requirements to run a Hugging Face `transformers` sentiment pipeline.

Quick start:

1. (Optional) Activate your Conda environment with `torch` installed.
2. Open `huggingface_pipeline.ipynb` in Jupyter.
3. Run the install cell if needed: `!pip install -q transformers torch huggingface-hub`.
4. Run the notebook cells; model weights will download on first run.

Notes:
- Use a GPU kernel for faster inference if available.
- If running offline, pre-download model weights and update the pipeline to use `cache_dir`.
