# Prompt Generator Node for ComfyUI
from comfy.comfy_types import IO, ComfyNodeABC, InputTypeDict


class PromptGenerator(ComfyNodeABC):
    CATEGORY = "Goez/Prompt"
    RETURN_TYPES = (IO.STRING, IO.STRING)
    RETURN_NAMES = ("positive", "negative")
    FUNCTION = "generate"
    TITLE = "Prompt Generator"
    DESCRIPTION = "Combine multiple positive/negative prompts with custom delimiter and whitespace cleaning."

    @classmethod
    def INPUT_TYPES(cls) -> InputTypeDict:
        return {
            "optional": {
                "positive_1": (IO.STRING, {"multiline": True, "default": ""}),
                "positive_2": (IO.STRING, {"multiline": True, "default": ""}),
                "positive_3": (IO.STRING, {"multiline": True, "default": ""}),
                "positive_4": (IO.STRING, {"multiline": True, "default": ""}),
                "positive_extra1": (IO.STRING, {"default": ""}),
                "positive_extra2": (IO.STRING, {"default": ""}),
                "negative": (IO.STRING, {"multiline": True, "default": ""}),
            },
            "required": {
                "delimiter": (IO.STRING, {"default": ","}),
            },
        }

    def generate(
        self,
        positive_1=None,
        positive_2=None,
        positive_3=None,
        positive_4=None,
        positive_extra1=None,
        positive_extra2=None,
        negative=None,
        delimiter=",",
    ):
        positives = [
            positive_1 or "",
            positive_2 or "",
            positive_3 or "",
            positive_4 or "",
            positive_extra1 or "",
            positive_extra2 or "",
        ]
        # Split multiline and flatten, skip empty
        parts = []
        for p in positives:
            if isinstance(p, str) and p.strip():
                lines = p.split("\n")
                for line in lines:
                    line = line.strip()
                    if line.endswith(","):
                        line = line[:-1].rstrip()
                    if line:
                        parts.append(line)
        positive = (delimiter + "\n").join(parts)
        return (positive, negative or "")


NODE_CLASS_MAPPINGS = {
    "PromptGenerator": PromptGenerator,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptGenerator": "Prompt Generator",
}
