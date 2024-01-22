from abc import ABC, abstractmethod

from diffusers import DiffusionPipeline
import torch


class Model(ABC):
    def __init__(self, cuda=True ):
        raise NotImplementedError
    
    @abstractmethod
    def query(self, prompt, negative_prompt=None):
        raise NotImplementedError


class SDModel(Model):
    def __init__(self, cuda=True):
        self.pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", 
                                                      torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
        if cuda and torch.cuda.is_available():
            self.pipe.to('cuda')

    def query(self, prompt, negative_prompt=None):
        return self.pipe(prompt=prompt, negative_prompt=negative_prompt).images[0]
