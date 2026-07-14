import math
import time
import platform
from typing import Optional

from .Mathematics.Matrix4 import Matrix4
from .Mathematics.Vector2 import Vector2
from .ArgumentParser import ParseArguments
from .Window import GameWindow
from ..Assets.DefaultAssets import DefaultAssets
from ..Rendering.SnakeGLFW import SnakeGLFW
from ..Rendering.GraphicsContext import GraphicsContext
from ..Rendering.Camera import Camera
from ..Rendering.Skybox import Skybox
from .Input import Input
from ..Audio.AudioManager import AudioManager
from ..Rendering.MeshRenderer import MeshRenderer
from ..UI.Canvas import UICanvas
from ..UI.Button import UIButton
from ..UI.Slider import UISlider
from .ScriptManager import ScriptManager
from .FileSystem import FileSystem
from .GameSettings import GameSettings
from ..Rendering.ShaderManager import ShaderManager
from .Scene import Scene
from .Logger import Logger, InitializeLogger
from .GameEntity import GameEntity

class Game:
    def __init__(self, settings: Optional[GameSettings] = None):
        self._IsRunning = False
        self.GameWindow = None
        self.GraphicsContext = GraphicsContext()
        self.ActiveScene = None
        self.GlobalCanvas = None
        self.MouseLocked = False
        self.FPS = 0

        self.Settings = settings if settings is not None else GameSettings()

        self.ScriptMgr = ScriptManager()

        self._last_time = None
        self._fps_timer = None
        self._frame_count = 0
        self._fixed_timer = 0.0
        self._FIXED_DELTA = 1.0 / 60.0
        self._alt_enter_pressed = False
        self._esc_pressed = False
        self._lpm_pressed = False

        self.Initialize()

    def Initialize(self):
        print(
            "=" * 50
            + "\n Snake Engine \n Python version: "
            + str(platform.python_version())
            + "\n"
            + "=" * 50
        )
        InitializeLogger()

        args = ParseArguments()
        FileSystem.Initialize(self.Settings)

        width = args.width if args.width else self.Settings.screen_width
        height = args.height if args.height else self.Settings.screen_height
        WindowSize = Vector2(width, height)

        Backend = args.backend if args.backend else "opengl"
        Fullscreen = (
            args.fullscreen if args.fullscreen is not None else self.Settings.fullscreen
        )
        SnakeGLFW.Initialize()

        match Backend:
            case "opengl":
                Logger.info("Using backend: OpenGL")
            case "headless":
                raise NotImplementedError("Headless backend is not implemented yet")
            case "vk" | "vulkan":
                raise NotImplementedError("Vulkan backend is not implemented yet")

        Logger.info(
            f"Creating window... Resolution: {width}x{height}, Fullscreen: {Fullscreen}"
        )
        self.GameWindow = GameWindow(
            self.GraphicsContext,
            WindowSize,
            self.Settings.title,
            DefaultAssets.ENGINE_ICON,
        )

        self.GameWindow.Fullscreen = True if Fullscreen else False
        self.GraphicsContext.MakeCurrent(self.GameWindow.Handle)
        
        AudioManager.Get().Initialize()
        Input._Initialize(self.GameWindow.Handle, SnakeGLFW())
        Logger.info("Input system initialized.")

        self.GlobalCanvas = UICanvas()
        self.ActiveScene = Scene()
        self._IsRunning = True
        Logger.info("Ready!")

    def Shutdown(self):
        self._IsRunning = False
        if self.ActiveScene:
            self.ScriptMgr.ClearOrphanedScripts(self.ActiveScene.Entities)
        ShaderManager.cleanup()
        AudioManager.Get().Shutdown()
        SnakeGLFW.Shutdown()

    def LockMouse(self):
        SnakeGLFW.SetCursorMode(self.GameWindow.Handle, "LOCKED")
        self.MouseLocked = True

    def UnlockMouse(self):
        SnakeGLFW.SetCursorMode(self.GameWindow.Handle, "NORMAL")
        self.MouseLocked = False

    def Run(self):
        while self._IsRunning and not self.GameWindow.ShouldClose():
            now = time.perf_counter()
            if self._last_time is None:
                self._last_time = now
                self._fps_timer = now
                continue

            SnakeGLFW.PollEvents()

            current_time = time.perf_counter()
            DeltaTime = current_time - self._last_time
            self._last_time = current_time
            if DeltaTime > 0.1:
                DeltaTime = 0.1

            Input._UpdateStates()

            is_enter = Input.IsKeyPressed("ENTER")
            is_alt = Input.IsKeyPressed("L_ALT") or Input.IsKeyPressed("R_ALT")

            if is_enter and is_alt:
                if not self._alt_enter_pressed:
                    self.GameWindow.Fullscreen = not self.GameWindow.Fullscreen
                    self._alt_enter_pressed = True
            else:
                self._alt_enter_pressed = False

            if Input.IsKeyPressed("ESCAPE"):
                if not self._esc_pressed:
                    if self.MouseLocked:
                        self.UnlockMouse()
                    self._esc_pressed = True
            else:
                self._esc_pressed = False

            mx, my = Input.GetMousePosition()
            lpm_pressed_state = Input.IsMouseButtonPressed("LEFT")

            if self.ActiveScene:
                for entity in self.ActiveScene.Entities:
                    btn = entity.GetComponent(UIButton)
                    if btn:
                        b = btn.Bounds
                        if (
                            b.Position.X <= mx <= b.Position.X + b.Width
                            and b.Position.Y <= my <= b.Position.Y + b.Height
                        ):
                            btn.IsHovered = True
                        else:
                            btn.IsHovered = False

            if lpm_pressed_state:
                if not self._lpm_pressed and self.ActiveScene:
                    for entity in self.ActiveScene.Entities:
                        btn = entity.GetComponent(UIButton)
                        if btn and btn.Callback and btn.IsHovered:
                            btn.Callback()
                    self._lpm_pressed = True

                if self.ActiveScene:
                    for entity in self.ActiveScene.Entities:
                        slider = entity.GetComponent(UISlider)
                        if slider:
                            b = slider.Bounds
                            if slider.IsDragging or (
                                b.Position.X <= mx <= b.Position.X + b.Width
                                and b.Position.Y <= my <= b.Position.Y + b.Height
                            ):
                                slider.IsDragging = True
                                relative_x = mx - b.Position.X
                                new_val = relative_x / b.Width
                                slider.Value = max(0.0, min(1.0, new_val))
            else:
                self._lpm_pressed = False
                if self.ActiveScene:
                    for entity in self.ActiveScene.Entities:
                        slider = entity.GetComponent(UISlider)
                        if slider:
                            slider.IsDragging = False

            if self.ActiveScene:
                self._fixed_timer += DeltaTime
                while self._fixed_timer >= self._FIXED_DELTA:
                    self.ScriptMgr.OnFixedUpdate(
                        self.ActiveScene.Entities, self._FIXED_DELTA
                    )
                    self._fixed_timer -= self._FIXED_DELTA

                self.ScriptMgr.OnUpdate(self.ActiveScene.Entities, DeltaTime)

            self.GameWindow.UpdateDimensions()

            if self.ActiveScene:
                view_matrix = None
                proj_matrix = None
                aspect_ratio = (
                    self.GameWindow.Width / self.GameWindow.Height
                    if self.GameWindow.Height > 0
                    else 1.0
                )

                for entity in self.ActiveScene.Entities:
                    cam = entity.GetComponent(Camera)
                    if cam:
                        view_matrix = cam.GetViewMatrix(entity.Transform)
                        proj_matrix = Matrix4.Perspective(
                            math.radians(cam.Fov), aspect_ratio, cam.Near, cam.Far
                        )
                        break

                self._frame_count += 1
                if current_time - self._fps_timer >= 1.0:
                    self.FPS = self._frame_count
                    self._frame_count = 0
                    self._fps_timer = current_time

                self.GraphicsContext.ScreenClear(
                    self.GameWindow.Handle, 0.05, 0.05, 0.1
                )

                if view_matrix and proj_matrix:
                    for entity in self.ActiveScene.Entities:
                        sky = entity.GetComponent(Skybox)
                        if sky:
                            sky.Render(proj_matrix, view_matrix)

                if view_matrix and proj_matrix:
                    for entity in self.ActiveScene.Entities:
                        mesh = entity.GetComponent(MeshRenderer)
                        if mesh:
                            mesh.Render(entity.Transform, view_matrix, proj_matrix)

                if self.GlobalCanvas:
                    self.GlobalCanvas.Render(
                        self.ActiveScene.Entities,
                        self.GameWindow.Width,
                        self.GameWindow.Height,
                    )

            self.GraphicsContext.ScreenPresent(self.GameWindow.Handle)

        self.Shutdown()
