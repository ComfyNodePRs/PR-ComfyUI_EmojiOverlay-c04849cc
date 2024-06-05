from PIL import Image, ImageDraw, ImageFont
import torch
import numpy as np
import cairosvg
import io
import re

class ImageEmojiOverlay:
    def __init__(self, device="cpu"):
        self.device = device
    _alignments = ["left", "right", "center"]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "text": ("STRING", {"multiline": True, "default": "Hello 😊"}),
                "font_size": ("INT", {"default": 16, "min": 1, "max": 256, "step": 1}),
                "x": ("INT", {"default": 0}),
                "y": ("INT", {"default": 0}),
                "emoji_font": ("STRING", {"default": "/tmp/data/ComfyUI/fonts/NotoColorEmoji-Regular.ttf"}),   # Assuming it's a path to a .ttf or .otf file
                "alignment": (cls._alignments, {"default": "left"}),  # ["left", "right", "center"]
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "draw_text_on_image"
    CATEGORY = "image/text"


    def draw_text_on_image(self, image, text, font_size, x, y, emoji_font, alignment):
        # Convert tensor to numpy array and then to PIL Image
        image_tensor = image
        image_np = image_tensor.cpu().numpy()  # Change from CxHxW to HxWxC for Pillow
        image = Image.fromarray((image_np.squeeze(0) * 255).astype(np.uint8))  # Convert float [0,1] tensor to uint8 image

        # Load emoji font
        emoji_loaded_font = ImageFont.truetype(emoji_font, font_size)

        # Prepare to draw on image
        draw = ImageDraw.Draw(image)

        # Adjust x coordinate based on alignment
        text_width, text_height = draw.textsize(text, font=emoji_loaded_font)
        if alignment == "center":
            x -= text_width // 2
        elif alignment == "right":
            x -= text_width

        # Draw emoji text
        draw.text((x, y), text, font=emoji_loaded_font)

        # Convert back to Tensor if needed
        image_tensor_out = torch.tensor(np.array(image).astype(np.float32) / 255.0)  # Convert back to CxHxW
        image_tensor_out = torch.unsqueeze(image_tensor_out, 0)

        return (image_tensor_out,)


NODE_CLASS_MAPPINGS = {
    "Image Emoji Overlay": ImageEmojiOverlay,
}