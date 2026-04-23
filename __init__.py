class AspectResolutionPicker:
    """
    Resolution picker for common aspect ratios and quality levels.

    - Select ratio: Square (1:1), Classic (4:3), Cinematic (16:9), Ultrawide (21:9), Custom
    - Select orientation: Landscape or Portrait
    - Quality levels: Low / Medium / High / Ultra
    
    Returns: width, height, actual_megapixels, description
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "ratio": (
                    [
                        "Square - 1:1",
                        "Classic - 4:3",
                        "Cinematic - 16:9",
                        "Ultrawide - 21:9",
                        "Custom",
                    ],
                ),
                "orientation": (
                    [
                        "Landscape",
                        "Portrait",
                    ],
                ),
                "quality": (
                    [
                        "Low (0.5 MP)",
                        "Medium (1 MP)",
                        "High (2 MP)",
                        "Ultra (4 MP)",
                    ],
                ),
            },
            "optional": {
                "custom_width": (
                    "INT",
                    {
                        "default": 1024,
                        "min": 64,
                        "max": 2048,
                        "step": 16,
                    },
                ),
                "custom_height": (
                    "INT",
                    {
                        "default": 1024,
                        "min": 64,
                        "max": 2048,
                        "step": 16,
                    },
                ),
                "force_multiple_of_16": (
                    "BOOLEAN",
                    {
                        "default": True,
                    },
                ),
            },
        }

    RETURN_TYPES = ("INT", "INT", "FLOAT", "STRING")
    RETURN_NAMES = ("width", "height", "megapixels", "description")

    FUNCTION = "compute"
    CATEGORY = "Resolution"

    PRESET_TABLE = {
        "Square - 1:1": {
            "Low (0.5 MP)": (512, 512),
            "Medium (1 MP)": (1024, 1024),
            "High (2 MP)": (1536, 1536),
            "Ultra (4 MP)": (2048, 2048),
        },
        "Classic - 4:3": {
            "Low (0.5 MP)": (768, 576),
            "Medium (1 MP)": (1024, 768),
            "High (2 MP)": (1600, 1200),
            "Ultra (4 MP)": (2048, 1536),
        },
        "Cinematic - 16:9": {
            "Low (0.5 MP)": (768, 432),
            "Medium (1 MP)": (1280, 720),
            "High (2 MP)": (1920, 1080),
            "Ultra (4 MP)": (2560, 1440),
        },
        "Ultrawide - 21:9": {
            "Low (0.5 MP)": (960, 432),
            "Medium (1 MP)": (1728, 768),
            "High (2 MP)": (2560, 1080),
            "Ultra (4 MP)": (3440, 1440),
        },
    }

    def compute(
        self,
        ratio,
        orientation,
        quality,
        custom_width=1024,
        custom_height=1024,
        force_multiple_of_16=True,
    ):
        if ratio == "Custom":
            width = max(64, min(2048, custom_width))
            height = max(64, min(2048, custom_height))
            if force_multiple_of_16:
                width = int(round(width / 16)) * 16
                height = int(round(height / 16)) * 16
            actual_mp = (width * height) / 1_000_000.0
            desc = f"Custom → {width}×{height} (~{actual_mp:.2f} MP)"
            return width, height, actual_mp, desc

        if ratio not in self.PRESET_TABLE:
            ratio = "Square - 1:1"

        if quality not in self.PRESET_TABLE[ratio]:
            quality = "Medium (1 MP)"

        width, height = self.PRESET_TABLE[ratio][quality]

        if orientation == "Portrait":
            width, height = height, width

        actual_mp = (width * height) / 1_000_000.0
        ratio_label = ratio.replace(" - ", ":")

        desc = f"{ratio_label} {orientation}, {quality} → {width}×{height} (~{actual_mp:.2f} MP)"

        return width, height, actual_mp, desc


NODE_CLASS_MAPPINGS = {
    "AspectResolutionPicker": AspectResolutionPicker,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AspectResolutionPicker": "Standard Resolution Presets",
}