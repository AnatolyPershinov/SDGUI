from abc import ABC, abstractmethod
import torchvision.transforms as transforms

from diffusers import DiffusionPipeline
import torch

from PIL import Image


class Model(ABC):
    def __init__(self, cuda=True ):
        raise NotImplementedError
    
    @abstractmethod
    def query(self, prompt, negative_prompt=None):
        raise NotImplementedError


class SDModel(Model):
    def __init__(self, cuda=True):
        self.pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
                
        if cuda and torch.cuda.is_available():
            self.pipe.to('cuda')
        
        try:
            self.pipe.unet = torch.compile(self.pipe.unet, mode="reduce-overhead", fullgraph=True)
        except RuntimeError:
            pass

    def query(self, prompt, negative_prompt=None):
        t_img = self.pipe(prompt=prompt, negative_prompt=negative_prompt).images[0] 
        return t_img
