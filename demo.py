from SnakeEngine import *


class FPSLabelUpdate(GameScript):
    def OnUpdate(self, DeltaTime):
        fps_counter.Text = f"FPS: {game.FPS}"


class Rotating(GameScript):
    def OnUpdate(self, DeltaTime):
        self.Entity.Transform.Rotation.Y += 1.0 * DeltaTime
        self.Entity.Transform.Rotation.X += 0.5 * DeltaTime


if __name__ == "__main__":
    settings = GameSettings()
    settings.title = "Snake Engine Demo"
    settings.company_name = "SnakeEngineTeam"
    settings.project_name = "SnakeEngineDemo"

    settings.screen_width = 1024
    settings.screen_height = 768
    settings.fullscreen = False

    game = Game(settings)
    scene = Scene()

    camera_entity = scene.CreateEntity()
    camera_entity.AddComponent(Camera)
    camera_entity.Transform.Position.Z = -3.0

    global_entity = scene.CreateEntity()
    global_entity.AddComponent(Skybox)

    cube_entity = scene.CreateEntity()
    cube_entity.AddComponent(MeshRenderer)
    cube_entity.AddComponent(Rotating)

    panel = scene.CreateEntity()
    panel.Name = "SideMenuPanel"
    panel.AddComponent(
        UIFrame, x=20, y=60, width=250, height=400, color=(0.1, 0.1, 0.15, 0.85)
    )

    def OnStartClicked():
        Logger.info("Button clicked! Locking mouse...")
        game.LockMouse()

    button = scene.CreateEntity()
    button.Name = "MouseLockButton"
    button.AddComponent(
        UIButton,
        text="Lock mouse",
        x=40,
        y=90,
        width=210,
        height=40,
        bg_color=(0.2, 0.5, 0.2, 1.0),
        callback=OnStartClicked,
    )

    button2 = scene.CreateEntity()
    button2.Name = "Button"
    button2.AddComponent(
        UIButton,
        text="Button",
        x=40,
        y=150,
        width=210,
        height=40,
        bg_color=(0.3, 0.3, 0.3, 1.0),
        callback=None,
    )

    slider = scene.CreateEntity()
    slider.Name = "Slider"
    slider.AddComponent(UISlider, x=40, y=230, width=210, height=20, value=0.7)

    image_placeholder = scene.CreateEntity()
    image_placeholder.Name = "Image"
    image_placeholder.AddComponent(
        UIImage, x=40, y=280, width=210, height=150, color=(1.0, 1.0, 1.0, 1.0), path=DefaultAssets.ENGINE_ICON
    )

    fps_entity = scene.CreateEntity()
    fps_entity.Name = "FPS_Display"
    fps_counter = fps_entity.AddComponent(
        UILabel, text="FPS: 0", x=20, y=20, scale=0.6, color=(1.0, 1.0, 0.0, 1.0)
    )
    fps_entity.AddComponent(FPSLabelUpdate)

    game.ActiveScene = scene

    game.Run()
