import os
from pathlib import Path

class DefaultAssets:
    _BaseDir = Path(__file__).resolve().parents[0]

    def GetAssetsPath():
        return DefaultAssets._BaseDir

    SHADER_VERT = os.path.join(_BaseDir, "Shaders", "DefaultShader.vert")
    SHADER_FRAG = os.path.join(_BaseDir, "Shaders", "DefaultShader.frag")
    SKYBOX_SHADER_FRAG = os.path.join(_BaseDir, "Shaders", "SkyboxDefaultShader.frag")
    SKYBOX_SHADER_VERT = os.path.join(_BaseDir, "Shaders", "SkyboxDefaultShader.vert")
    UI_SHADER_VERT = os.path.join(_BaseDir, "Shaders", "UIDefaultShader.vert")
    UI_SHADER_FRAG = os.path.join(_BaseDir, "Shaders", "UIDefaultShader.frag")

    FONT_ATLAS_PNG = os.path.join(_BaseDir, "OpenSansRegular_atlas.png")
    FONT_ATLAS_JSON = os.path.join(_BaseDir, "OpenSansRegular_atlas.json")
    ENGINE_ICON = os.path.join(_BaseDir, "Icon.png")
