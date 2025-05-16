# File: models/model_loader.py

import os
from typing import Optional

class ModelLoader:
    def __init__(self, model_dir: str = "models"):
        self.model_dir = model_dir
        self.local_model_file = "mistral_quantized.gguf"
        self.loaded = False
        self.model_path = None

    def check_local_model(self) -> bool:
        """Check if the quantized GGUF model is present locally."""
        full_path = os.path.join(self.model_dir, self.local_model_file)
        if os.path.exists(full_path):
            self.model_path = full_path
            self.loaded = True
            return True
        return False

    def get_model_path(self) -> Optional[str]:
        """Returns the local model path if loaded."""
        if self.loaded and self.model_path:
            return self.model_path
        if self.check_local_model():
            return self.model_path
        return None

    def load_model(self) -> str:
        """Simulates model loading (for CLI / agent use)."""
        if self.check_local_model():
            return f"[✅] Local model loaded: {self.model_path}"
        return "[❌] Model not found. Please download the .gguf file and place it in the /models directory."

if __name__ == "__main__":
    loader = ModelLoader()
    print(loader.load_model())
