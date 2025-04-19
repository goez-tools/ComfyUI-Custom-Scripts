from comfy.comfy_types import IO, ComfyNodeABC, InputTypeDict
import comfy.samplers
import folder_paths


class ConfigLoader(ComfyNodeABC):

    @classmethod
    def INPUT_TYPES(cls) -> InputTypeDict:
        return {
            "required": {
                "model": (IO.MODEL, {}),
                "clip": (IO.CLIP, {}),
                "positive_text": (IO.STRING, {"multiline": True, "default": "", "forceInput": True}),
                "negative_text": (IO.STRING, {"multiline": True, "default": "", "forceInput": True}),
                "model_name": (IO.STRING, {"forceInput": True}),
                "vae_name": (folder_paths.get_filename_list("vae"),),
                "sampler": (comfy.samplers.KSampler.SAMPLERS, {}),
                "scheduler": (comfy.samplers.KSampler.SCHEDULERS, {}),
                "steps": (IO.INT, {"min": 1, "max": 10000, "default": 30}),
                "cfg": (IO.FLOAT, {"min": 0.0, "max": 100.0, "step": 0.1, "default": 3.5}),
                "seed": (IO.INT, {"min": 0, "max": 0xFFFFFFFFFFFFFFFF, "default": 0}),
                "latent": (IO.LATENT, {}),
            },
            "optional": {
                "vae_override": (IO.VAE,),
                "width": (IO.INT, {"default": 1024, "min": 8, "max": 4096, "forceInput": True}),
                "height": (IO.INT, {"default": 1024, "min": 8, "max": 4096, "forceInput": True}),
                "image": (IO.IMAGE, {"forceInput": True}),
                "xyPlot": ("XYPLOT", {"forceInput": True}),
                "stop_at_clip_layer": (IO.INT, {"default": -2, "min": -24, "max": -1, "step": 1}),
            },
        }

    RETURN_TYPES = ("PIPE_LINE",)
    RETURN_NAMES = ("pipe",)
    FUNCTION = "load_config"
    CATEGORY = "Goez/Loader"
    DESCRIPTION = "ConfigLoader (Pipe): Load and combine various generation settings and inputs, then output the complete pipeline information."

    def load_vae(self, vae_name):
        vae_path = folder_paths.get_full_path_or_raise("vae", vae_name)
        sd = comfy.utils.load_torch_file(vae_path)
        vae = comfy.sd.VAE(sd=sd)
        vae.throw_exception_if_invalid()
        return vae

    def set_clip_last_layer(self, clip, stop_at_clip_layer):
        if stop_at_clip_layer is not None:
            clip = clip.clone()
            clip.clip_layer(stop_at_clip_layer)
        return clip

    def load_config(
        self,
        model,
        clip,
        positive_text,
        negative_text,
        model_name,
        vae_name,
        sampler,
        scheduler,
        steps,
        cfg,
        seed,
        vae_override=None,
        width=None,
        height=None,
        latent=None,
        image=None,
        xyPlot=None,
        stop_at_clip_layer=None,
    ):
        clip = self.set_clip_last_layer(clip, stop_at_clip_layer)
        tokens_pos = clip.tokenize(positive_text)
        positive = clip.encode_from_tokens_scheduled(tokens_pos)
        tokens_neg = clip.tokenize(negative_text)
        negative = clip.encode_from_tokens_scheduled(tokens_neg)
        sampler_name = sampler if isinstance(sampler, str) else str(sampler)
        scheduler_name = scheduler if isinstance(scheduler, str) else str(scheduler)
        if vae_override:
            vae = vae_override
        else:
            vae = self.load_vae(vae_name)

        pipe = {
            "model": model,
            "positive": positive,
            "negative": negative,
            "latent": latent,
            "vae": vae,
            "clip": clip,
            "image": image,
            "xyPlot": xyPlot,
            "sampler": sampler,
            "scheduler": scheduler,
            "steps": steps,
            "cfg": cfg,
            "seed": seed,
            "width": width,
            "height": height,
            "model_name": model_name,
            "sampler_name": sampler_name,
            "scheduler_name": scheduler_name,
            "positive_text": positive_text,
            "negative_text": negative_text,
        }
        return (pipe,)


NODE_CLASS_MAPPINGS = {
    "ConfigLoader": ConfigLoader,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "ConfigLoader": "ConfigLoader (Pipe)",
}
