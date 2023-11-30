import os

PROMPT_DIR = "prompts/"

def _load_prompt_from_txt_file(file_path: str) -> str:
    with open(file_path, "r") as f:
        return f.read()


def get_system_prompt() -> str:
    return _load_prompt_from_txt_file(os.path.join("system_prompt.txt"))