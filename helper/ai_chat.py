import os
from pathlib import Path
from typing import Optional
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

class AIChat:
    def __init__(self):
        self.model_id = "Qwen/Qwen2.5-0.5B-Instruct"
        self.cache_dir = Path(__file__).resolve().parents[1] / ".model"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ai_ready = False

        os.environ["HF_HOME"] = str(self.cache_dir)
        os.environ["TRANSFORMERS_CACHE"] = str(self.cache_dir)
        os.environ["HF_HUB_CACHE"] = str(self.cache_dir)

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_id,
                cache_dir=str(self.cache_dir),
                # local_files_only=True,
            )
            model = AutoModelForCausalLM.from_pretrained(
                self.model_id,
                cache_dir=str(self.cache_dir),
                torch_dtype=torch.float32,
                low_cpu_mem_usage=True,
                device_map="auto",
            )
            self.pipe = pipeline(
                "text-generation",
                model=model,
                tokenizer=self.tokenizer,
            )
            self.ai_ready = True
        except Exception as e:
            print(f"Unable to connect to Hugging Face: {e}")

    def answer(self, query: str, context: str) -> str:
        if self.ai_ready == False:
            return "Your model is not ready"

        if not query or not query.strip():
            return "Please type a question."

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a chart/data summarizer. Answer only from the provided "
                    "dataframe and chart context. Be concise and factual. Do not "
                    f"invent numbers or values.\n\nContext:\n{context}"
                ),
            },
            {"role": "user", "content": query},
        ]
        prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        outputs = self.pipe(prompt, max_new_tokens=256, do_sample=False)
        generated_text = outputs[0]["generated_text"]
        return generated_text[len(prompt):].strip()
