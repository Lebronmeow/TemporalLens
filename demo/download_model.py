"""
Helper script to download TimeLens2 checkpoint from Hugging Face.
Usage:
    .venv\\Scripts\\python.exe download_model.py --model MCG-NJU/TimeLens2-2B
"""
import argparse
import sys
from huggingface_hub import snapshot_download

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="MCG-NJU/TimeLens2-2B", help="Hugging Face repo ID")
    args = parser.parse_args()

    print(f"📥 Downloading checkpoint '{args.model}' from Hugging Face...")
    try:
        path = snapshot_download(repo_id=args.model)
        print(f"✅ Checkpoint downloaded successfully to:\n{path}")
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
