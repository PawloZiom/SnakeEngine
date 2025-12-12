"""Moduł logowania projektu.

Funkcje: `Setup(debugMode)`, `Info()`, `Debug()`, `Warning()`, `Error()`, `Exception()`.
Funkcje automatycznie dobierają loggera na podstawie modułu wywołującego;
można dodatkowo podać `component` (np. 'Audio') lub `namespace` (np. 'Game').
"""

import logging
import sys
import inspect
from datetime import datetime


class _EngineGameFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        # Timestamp HH:MM:SS
        ct = datetime.fromtimestamp(record.created)
        ts = ct.strftime("%H:%M:%S")

        # Use logger name, convert dots to slashes for display
        name = getattr(record, "name", "") or "Unknown"
        src = name.replace('.', '/')

        level = record.levelname
        msg = record.getMessage()
        return f"[{ts}] [{src}({level})] {msg}"


def _choose_logger_name(caller_module: str | None, component: str | None = None, namespace: str | None = None) -> str:
    """Wybiera nazwę loggera na podstawie modułu wywołującego.

    - Jeśli `namespace` jest podane, używa go jako bazowego (np. 'Game').
    - W przeciwnym razie próbuje wykryć 'Engine' lub 'Game' z nazwy modułu.
    - `component` (opcjonalny) jest dopisywany jako podkomponent.
    Zwraca nazwę loggera w postaci 'Engine' lub 'Engine.Audio'.
    """
    base = None
    mod = (caller_module or "").lower()

    if namespace:
        base = namespace.capitalize()
    elif 'snakeengine' in mod or mod.startswith('snakeengine') or 'engine' in mod:
        base = 'Engine'
    elif 'game' in mod:
        base = 'Game'
    else:
        # Fallback: pierwsza część modułu
        parts = (caller_module or '').split('.')
        if parts:
            base = parts[0].capitalize()
        else:
            base = 'Unknown'

    if component:
        return f"{base}.{component}"
    else:
        # spróbuj wydobyć podkomponent z modułu (np. SnakeEngine.audio -> Audio)
        parts = (caller_module or '').split('.')
        # jeśli moduł zaczyna się od snakeengine/engine, sprawdź kolejny segment
        if parts:
            # znajdź index 'engine' lub 'game' jeśli istnieje
            idx = None
            for i, p in enumerate(parts):
                if p.lower() in ('engine', 'snakeengine', 'game'):
                    idx = i
                    break
            if idx is not None and len(parts) > idx + 1:
                sub = parts[idx + 1].capitalize()
                return f"{base}.{sub}"

        return base


def Setup(debugMode: bool):
    """Konfiguruje logowanie konsolowe (bez zapisu do pliku)."""

    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)

    level = logging.DEBUG if debugMode else logging.INFO
    root.setLevel(level)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    ch.setFormatter(_EngineGameFormatter())
    root.addHandler(ch)


# Funkcje ułatwiające logowanie — wywołania z kodu: Debug.Info(...)
def _get_caller_module(skip: int = 2) -> str | None:
    # skip=2 => caller of the public wrapper (Info/Error/etc.)
    stack = inspect.stack()
    if len(stack) > skip:
        frame = stack[skip].frame
        mod = inspect.getmodule(frame)
        if mod and getattr(mod, '__name__', None):
            return mod.__name__
        # fallback to file name
        return frame.f_globals.get('__name__')
    return None


def Info(msg: str, *args, component: str | None = None, namespace: str | None = None, **kwargs):
    caller = _get_caller_module()
    name = _choose_logger_name(caller, component=component, namespace=namespace)
    logging.getLogger(name).info(msg, *args, **kwargs)


def Debug(msg: str, *args, component: str | None = None, namespace: str | None = None, **kwargs):
    caller = _get_caller_module()
    name = _choose_logger_name(caller, component=component, namespace=namespace)
    logging.getLogger(name).debug(msg, *args, **kwargs)


def Warning(msg: str, *args, component: str | None = None, namespace: str | None = None, **kwargs):
    caller = _get_caller_module()
    name = _choose_logger_name(caller, component=component, namespace=namespace)
    logging.getLogger(name).warning(msg, *args, **kwargs)


def Error(msg: str, *args, component: str | None = None, namespace: str | None = None, **kwargs):
    caller = _get_caller_module()
    name = _choose_logger_name(caller, component=component, namespace=namespace)
    logging.getLogger(name).error(msg, *args, **kwargs)


def Exception(msg: str, *args, component: str | None = None, namespace: str | None = None, **kwargs):
    caller = _get_caller_module()
    name = _choose_logger_name(caller, component=component, namespace=namespace)
    logging.getLogger(name).exception(msg, *args, **kwargs)


__all__ = ["Setup", "Info", "Debug", "Warning", "Error", "Exception"]