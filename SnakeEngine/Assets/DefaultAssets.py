import os


class DefaultAssets:
    _BaseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def GetAssetsPath():
        return DefaultAssets._BaseDir

    SHADER_VERT = os.path.join(_BaseDir, "Assets", "Shaders", "DefaultShader.vert")
    SHADER_FRAG = os.path.join(_BaseDir, "Assets", "Shaders", "DefaultShader.frag")
    SKYBOX_SHADER_FRAG = os.path.join(
        _BaseDir, "Assets", "Shaders", "SkyboxDefaultShader.frag"
    )
    SKYBOX_SHADER_VERT = os.path.join(
        _BaseDir, "Assets", "Shaders", "SkyboxDefaultShader.vert"
    )
    UI_SHADER_VERT = "SnakeEngine/Assets/Shaders/UIDefaultShader.vert"
    UI_SHADER_FRAG = "SnakeEngine/Assets/Shaders/UIDefaultShader.frag"

    FONT_ATLAS_PNG = os.path.join(_BaseDir, "Assets", "OpenSansRegular_atlas.png")
    FONT_ATLAS_JSON = os.path.join(_BaseDir, "Assets", "OpenSansRegular_atlas.json")
    ENGINE_ICON = os.path.join(_BaseDir, "Assets", "Icon.png")
