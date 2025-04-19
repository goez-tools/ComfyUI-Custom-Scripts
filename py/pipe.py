"""
Goez Pipe Nodes for ComfyUI (inspired by comfyui-easy-use)
"""

from comfy.comfy_types import IO, ComfyNodeABC, InputTypeDict
import comfy.samplers


class GoezPipeIn(ComfyNodeABC):
    @classmethod
    def INPUT_TYPES(cls) -> InputTypeDict:
        return {
            "required": {},
            "optional": {
                "pipe": ("PIPE_LINE", {"forceInput": True}),
                "model": (IO.MODEL, {"forceInput": True}),
                "positive": (IO.CONDITIONING, {"forceInput": True}),
                "negative": (IO.CONDITIONING, {"forceInput": True}),
                "latent": (IO.LATENT, {"forceInput": True}),
                "vae": (IO.VAE, {"forceInput": True}),
                "clip": (IO.CLIP, {"forceInput": True}),
                "image": (IO.IMAGE, {"forceInput": True}),
                "xyPlot": ("XYPLOT", {"forceInput": True}),
                "sampler": (comfy.samplers.KSampler.SAMPLERS, {"forceInput": True}),
                "scheduler": (comfy.samplers.KSampler.SCHEDULERS, {"forceInput": True}),
                "steps": (IO.INT, {"default": 20, "min": 1, "max": 10000, "forceInput": True}),
                "cfg": (IO.FLOAT, {"default": 8.0, "min": 0.0, "max": 100.0, "step": 0.1, "forceInput": True}),
                "seed": (IO.INT, {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF, "forceInput": True}),
                "width": (IO.INT, {"default": 1024, "min": 8, "max": 4096, "forceInput": True}),
                "height": (IO.INT, {"default": 1024, "min": 8, "max": 4096, "forceInput": True}),
                "model_name": (IO.STRING, {"forceInput": True}),
                "sampler_name": (IO.STRING, {"forceInput": True}),
                "scheduler_name": (IO.STRING, {"forceInput": True}),
                "positive_text": (IO.STRING, {"multiline": True, "default": "", "forceInput": True}),
                "negative_text": (IO.STRING, {"multiline": True, "default": "", "forceInput": True}),
            },
            "hidden": {"my_unique_id": "UNIQUE_ID"},
        }

    RETURN_TYPES = ("PIPE_LINE",)
    RETURN_NAMES = ("pipe",)
    FUNCTION = "flush"
    CATEGORY = "Goez/Pipe"

    def flush(
        self,
        pipe=None,
        model=None,
        positive=None,
        negative=None,
        latent=None,
        vae=None,
        clip=None,
        image=None,
        xyPlot=None,
        sampler=None,
        scheduler=None,
        steps=None,
        cfg=None,
        seed=None,
        width=None,
        height=None,
        model_name=None,
        sampler_name=None,
        scheduler_name=None,
        positive_text=None,
        negative_text=None,
        my_unique_id=None,
    ):
        new_pipe = dict(pipe) if pipe is not None else {}

        def set_val(key, val):
            if val is not None:
                new_pipe[key] = val
            elif pipe is not None and key in pipe:
                new_pipe[key] = pipe[key]

        set_val("model", model)
        set_val("positive", positive)
        set_val("negative", negative)
        set_val("latent", latent)
        set_val("vae", vae)
        set_val("clip", clip)
        set_val("image", image)
        set_val("xyPlot", xyPlot)
        set_val("sampler", sampler)
        set_val("scheduler", scheduler)
        set_val("steps", steps)
        set_val("cfg", cfg)
        set_val("seed", seed)
        set_val("width", width)
        set_val("height", height)
        set_val("model_name", model_name)
        set_val("sampler_name", sampler_name)
        set_val("scheduler_name", scheduler_name)
        set_val("positive_text", positive_text)
        set_val("negative_text", negative_text)
        return (new_pipe,)


class GoezPipeOut(ComfyNodeABC):
    @classmethod
    def INPUT_TYPES(cls) -> InputTypeDict:
        return {
            "required": {
                "pipe": ("PIPE_LINE", {}),
            },
            "hidden": {"my_unique_id": "UNIQUE_ID"},
        }

    RETURN_TYPES = (
        "PIPE_LINE",
        IO.MODEL,
        IO.CONDITIONING,
        IO.CONDITIONING,
        IO.LATENT,
        IO.VAE,
        IO.CLIP,
        IO.IMAGE,
        "XYPLOT",
        comfy.samplers.KSampler.SAMPLERS,
        comfy.samplers.KSampler.SCHEDULERS,
        IO.INT,
        IO.FLOAT,
        IO.INT,
        IO.INT,
        IO.INT,
        IO.STRING,
        IO.STRING,
        IO.STRING,
        IO.STRING,
        IO.STRING,
    )
    RETURN_NAMES = (
        "pipe",
        "model",
        "positive",
        "negative",
        "latent",
        "vae",
        "clip",
        "image",
        "xyPlot",
        "sampler",
        "scheduler",
        "steps",
        "cfg",
        "seed",
        "width",
        "height",
        "model_name",
        "sampler_name",
        "scheduler_name",
        "positive_text",
        "negative_text",
    )
    FUNCTION = "flush"
    CATEGORY = "Goez/Pipe"

    def flush(self, pipe, my_unique_id=None):
        return (
            pipe,
            pipe.get("model"),
            pipe.get("positive"),
            pipe.get("negative"),
            pipe.get("latent"),
            pipe.get("vae"),
            pipe.get("clip"),
            pipe.get("image"),
            pipe.get("xyPlot"),
            pipe.get("sampler"),
            pipe.get("scheduler"),
            pipe.get("steps"),
            pipe.get("cfg"),
            pipe.get("seed"),
            pipe.get("width"),
            pipe.get("height"),
            pipe.get("model_name"),
            pipe.get("sampler_name"),
            pipe.get("scheduler_name"),
            pipe.get("positive_text"),
            pipe.get("negative_text"),
        )


NODE_CLASS_MAPPINGS = {
    "GoezPipeIn": GoezPipeIn,
    "GoezPipeOut": GoezPipeOut,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GoezPipeIn": "Pipe In",
    "GoezPipeOut": "Pipe Out",
}
