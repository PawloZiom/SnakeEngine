import os
import sys
import json
from pathlib import Path
from typing import Optional, IO, Union
from .GameSettings import GameSettings
from .Logger import Logger, EnableFileLogging

_FALLBACK_APP_NAME = "SnakeEngine"


class _FileSystemSingleton:
    def __init__(self):
        self._user_data_dir: Optional[Path] = None
        self._assets_dir: Optional[Path] = None
        self._initialized: bool = False

    def Initialize(self, settings: Optional[GameSettings] = None):
        if self._initialized:
            return

        if settings is None:
            settings = GameSettings()

        if settings.CustomAssetsPath:
            self._assets_dir = Path(settings.CustomAssetsPath).resolve()
        else:
            self._assets_dir = Path.cwd()

        if settings.CustomUserDataPath:
            self._user_data_dir = Path(settings.CustomUserDataPath).resolve()
        else:
            self._user_data_dir = self._resolve_user_data_dir(
                settings.CompanyName, settings.ProjectName
            )

        self._user_data_dir.mkdir(parents=True, exist_ok=True)

        EnableFileLogging(self._user_data_dir)

        self._initialized = True
        Logger.info("FileSystem initialized successfully.")
        Logger.info(f"User data path: {self._user_data_dir}")
        Logger.info(f"Assets path:    {self._assets_dir}")

    def _resolve_user_data_dir(self, company: str, project: str) -> Path:
        if sys.platform == "win32":
            base = Path(
                os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local")
            )
        elif sys.platform == "darwin":
            base = Path.home() / "Library" / "Application Support"
        else:
            base = Path(
                os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")
            )

        c_clean = self._sanitize(company)
        p_clean = self._sanitize(project)

        if c_clean != _FALLBACK_APP_NAME and p_clean != _FALLBACK_APP_NAME:
            return base / c_clean / p_clean
        if p_clean != _FALLBACK_APP_NAME:
            return base / p_clean
        return base / _FALLBACK_APP_NAME

    @staticmethod
    def _sanitize(name: str) -> str:
        forbidden = r'\/:*?"<>|'
        for c in forbidden:
            name = name.replace(c, "_")
        return name.strip(". ") or _FALLBACK_APP_NAME

    def _ensure_init(self):
        if not self._initialized:
            self.Initialize()

    @property
    def user_data_path(self) -> Path:
        self._ensure_init()
        return self._user_data_dir

    def _resolve_user_path(self, relative: str) -> Path:
        self._ensure_init()
        path = self._user_data_dir / relative
        path = path.resolve()
        if not str(path).startswith(str(self._user_data_dir.resolve())):
            err_msg = f"Path traversal attempt detected: '{relative}' is outside of user data folder!"
            Logger.error(err_msg)
            raise ValueError(f"[FileSystem] {err_msg}")
        return path

    def write(
        self, relative_path: str, data: Union[str, bytes], encoding: str = "utf-8"
    ) -> bool:
        try:
            path = self._resolve_user_path(relative_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            mode = "wb" if isinstance(data, bytes) else "w"
            kwargs = {} if isinstance(data, bytes) else {"encoding": encoding}
            with open(path, mode, **kwargs) as f:
                f.write(data)
            return True
        except Exception as e:
            Logger.error(f"Failed to write file '{relative_path}': {e}", exc_info=True)
            return False

    def read(self, relative_path: str, encoding: str = "utf-8") -> Optional[str]:
        try:
            path = self._resolve_user_path(relative_path)
            if not path.exists():
                Logger.warning(
                    f"Attempted to read non-existent file: '{relative_path}'"
                )
                return None
            return path.read_text(encoding=encoding)
        except Exception as e:
            Logger.error(f"Failed to read file '{relative_path}': {e}", exc_info=True)
            return None

    def read_bytes(self, relative_path: str) -> Optional[bytes]:
        try:
            path = self._resolve_user_path(relative_path)
            if not path.exists():
                Logger.warning(
                    f"Attempted to read bytes from non-existent file: '{relative_path}'"
                )
                return None
            return path.read_bytes()
        except Exception as e:
            Logger.error(
                f"Failed to read bytes from '{relative_path}': {e}", exc_info=True
            )
            return None

    def exists(self, relative_path: str) -> bool:
        try:
            return self._resolve_user_path(relative_path).exists()
        except Exception:
            return False

    def delete(self, relative_path: str) -> bool:
        try:
            path = self._resolve_user_path(relative_path)
            if path.is_file():
                path.unlink()
                Logger.info(f"Deleted file: '{relative_path}'")
                return True
            Logger.warning(
                f"Cannot delete. Target does not exist or is not a file: '{relative_path}'"
            )
            return False
        except Exception as e:
            Logger.error(f"Failed to delete file '{relative_path}': {e}", exc_info=True)
            return False

    def list_files(self, relative_dir: str = "", pattern: str = "*") -> list[str]:
        try:
            base = (
                self._resolve_user_path(relative_dir)
                if relative_dir
                else self._user_data_dir
            )
            if not base.exists():
                return []
            return [
                str(p.relative_to(self._user_data_dir))
                for p in base.glob(pattern)
                if p.is_file()
            ]
        except Exception as e:
            Logger.error(
                f"Failed to list files in directory '{relative_dir}': {e}",
                exc_info=True,
            )
            return []

    @property
    def assets_path(self) -> Path:
        self._ensure_init()
        return self._assets_dir

    def resolve_asset_path(self, relative: str) -> Optional[str]:
        self._ensure_init()
        path = self._assets_dir / relative
        if path.exists():
            return str(path)
        for sub in ("Assets", "assets", "Resources", "resources"):
            path = self._assets_dir / sub / relative
            if path.exists():
                return str(path)
        return None

    def asset_exists(self, relative: str) -> bool:
        return self.resolve_asset_path(relative) is not None

    def open_asset(self, relative: str, binary: bool = False) -> IO:
        path = self.resolve_asset_path(relative)
        if path is None:
            err_msg = f"Asset not found: '{relative}'"
            Logger.error(err_msg)
            raise FileNotFoundError(f"[FileSystem] {err_msg}")
        mode = "rb" if binary else "r"
        kwargs = {} if binary else {"encoding": "utf-8"}
        return open(path, mode, **kwargs)

    def read_asset(self, relative: str) -> Optional[str]:
        try:
            with self.open_asset(relative) as f:
                return f.read()
        except FileNotFoundError:
            return None
        except Exception as e:
            Logger.error(f"Failed to read asset '{relative}': {e}", exc_info=True)
            return None

    def read_asset_bytes(self, relative: str) -> Optional[bytes]:
        try:
            with self.open_asset(relative, binary=True) as f:
                return f.read()
        except FileNotFoundError:
            return None
        except Exception as e:
            Logger.error(f"Failed to read asset bytes '{relative}': {e}", exc_info=True)
            return None

    def write_json(
        self, relative_path: str, data: Union[dict, list], indent: int = 2
    ) -> bool:
        return self.write(
            relative_path, json.dumps(data, indent=indent, ensure_ascii=False)
        )

    def read_json(self, relative_path: str) -> Optional[Union[dict, list]]:
        raw = self.read(relative_path)
        if raw is None:
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            Logger.error(
                f"Failed to decode JSON from file '{relative_path}': {e}", exc_info=True
            )
            return None


FileSystem = _FileSystemSingleton()
