import re
from dataclasses import dataclass, field
from typing import Optional, Union
from OpenGL.GL import *
from ..Core.Logger import Logger

GLSL_TYPE_MAP = {
    GL_FLOAT: ("float", float),
    GL_FLOAT_VEC2: ("vec2", None),
    GL_FLOAT_VEC3: ("vec3", None),
    GL_FLOAT_VEC4: ("vec4", None),
    GL_INT: ("int", int),
    GL_INT_VEC2: ("ivec2", None),
    GL_INT_VEC3: ("ivec3", None),
    GL_INT_VEC4: ("ivec4", None),
    GL_BOOL: ("bool", bool),
    GL_FLOAT_MAT2: ("mat2", None),
    GL_FLOAT_MAT3: ("mat3", None),
    GL_FLOAT_MAT4: ("mat4", None),
    GL_SAMPLER_2D: ("sampler2D", None),
    GL_SAMPLER_CUBE: ("samplerCube", None),
}

_ENGINE_UNIFORMS = {"model", "view", "projection", "viewPos", "time", "resolution"}

_UNIFORM_RE = re.compile(
    r"^\s*uniform\s+"
    r"(?:(?:lowp|mediump|highp)\s+)?"
    r"(\w+)\s+"
    r"(\w+)"
    r"(?:\[(\d+)\])?"
    r"\s*;",
    re.MULTILINE,
)


@dataclass
class UniformInfo:
    name: str
    glsl_type: str
    location: int = -1
    array_size: int = 1
    is_engine: bool = False
    value: object = None


@dataclass
class ShaderProgram:
    name: str
    gl_id: int
    vert_path: Optional[str] = None
    frag_path: Optional[str] = None
    vert_source: str = ""
    frag_source: str = ""
    uniforms: dict[str, UniformInfo] = field(default_factory=dict)
    is_valid: bool = True


class _ShaderManagerSingleton:
    def __init__(self):
        self._programs: dict[str, ShaderProgram] = {}

    def load(
        self, name: str, vert_path: str, frag_path: str, force_recompile: bool = False
    ) -> int:
        if name in self._programs and not force_recompile:
            return self._programs[name].gl_id

        try:
            with open(vert_path, encoding="utf-8") as f:
                vert_src = f.read()
            with open(frag_path, encoding="utf-8") as f:
                frag_src = f.read()
        except OSError as e:
            Logger.error(
                f"Failed to read shader file source for '{name}': {e}", exc_info=True
            )
            return 0

        program = self._compile(name, vert_src, frag_src)
        program.vert_path = vert_path
        program.frag_path = frag_path
        self._programs[name] = program

        if program.is_valid:
            Logger.info(
                f"Shader '{name}' loaded successfully. (vert={vert_path}, frag={frag_path})"
            )
        else:
            Logger.error(f"Failed to load shader '{name}'. Compilation/Linking failed.")

        return program.gl_id

    def load_source(
        self, name: str, vert_src: str, frag_src: str, force_recompile: bool = False
    ) -> int:
        if name in self._programs and not force_recompile:
            return self._programs[name].gl_id

        program = self._compile(name, vert_src, frag_src)
        self._programs[name] = program

        if program.is_valid:
            Logger.info(f"Shader '{name}' loaded successfully from inline source.")
        else:
            Logger.error(f"Failed to load shader '{name}' from inline source.")

        return program.gl_id

    def get(self, name: str) -> int:
        prog = self._programs.get(name)
        return prog.gl_id if prog else 0

    def get_program(self, name: str) -> Optional[ShaderProgram]:
        return self._programs.get(name)

    def get_uniforms(self, name: str, skip_engine: bool = True) -> list[UniformInfo]:
        prog = self._programs.get(name)
        if not prog:
            return []
        return [u for u in prog.uniforms.values() if not (skip_engine and u.is_engine)]

    def reload(self, name: str) -> bool:
        prog = self._programs.get(name)
        if not prog:
            Logger.warning(f"Shader reload failed: Unknown shader program '{name}'.")
            return False
        if not prog.vert_path or not prog.frag_path:
            Logger.warning(
                f"Shader reload failed: Program '{name}' has no registered file paths."
            )
            return False

        if prog.gl_id:
            try:
                glDeleteProgram(prog.gl_id)
            except Exception as e:
                Logger.error(
                    f"Error deleting old OpenGL shader program '{name}': {e}",
                    exc_info=True,
                )

        Logger.info(f"Reloading shader '{name}'...")
        self.load(name, prog.vert_path, prog.frag_path, force_recompile=True)
        return self._programs[name].is_valid

    def reload_all(self):
        Logger.info("Reloading all active shader programs...")
        for name in list(self._programs.keys()):
            self.reload(name)

    def cleanup(self):
        Logger.info("Cleaning up active shader programs...")
        for prog in self._programs.values():
            if prog.gl_id:
                try:
                    glDeleteProgram(prog.gl_id)
                except Exception as e:
                    Logger.error(
                        f"Failed to delete shader program ID {prog.gl_id} on cleanup: {e}",
                        exc_info=True,
                    )
        self._programs.clear()

    def list_shaders(self) -> list[str]:
        return list(self._programs.keys())

    def _compile(self, name: str, vert_src: str, frag_src: str) -> ShaderProgram:
        prog = ShaderProgram(
            name=name, gl_id=0, vert_source=vert_src, frag_source=frag_src
        )

        prog.uniforms = self._parse_uniforms_from_source(vert_src, frag_src)

        vs = self._compile_stage(name, vert_src, GL_VERTEX_SHADER, "VERTEX")
        fs = self._compile_stage(name, frag_src, GL_FRAGMENT_SHADER, "FRAGMENT")

        if not vs or not fs:
            prog.is_valid = False
            if vs:
                glDeleteShader(vs)
            if fs:
                glDeleteShader(fs)
            return prog

        gl_id = glCreateProgram()
        glAttachShader(gl_id, vs)
        glAttachShader(gl_id, fs)
        glLinkProgram(gl_id)

        if not glGetProgramiv(gl_id, GL_LINK_STATUS):
            log = glGetProgramInfoLog(gl_id)
            if isinstance(log, bytes):
                log = log.decode(errors="replace")

            Logger.error(f"Shader Program '{name}' LINK ERROR:\n{log}")

            glDeleteProgram(gl_id)
            glDeleteShader(vs)
            glDeleteShader(fs)
            prog.is_valid = False
            return prog

        glDeleteShader(vs)
        glDeleteShader(fs)
        prog.gl_id = gl_id

        self._query_uniforms_gl(prog)

        return prog

    def _compile_stage(
        self, shader_name: str, source: str, stage: int, stage_label: str
    ) -> int:
        shader = glCreateShader(stage)
        glShaderSource(shader, source)
        glCompileShader(shader)

        if not glGetShaderiv(shader, GL_COMPILE_STATUS):
            log = glGetShaderInfoLog(shader)
            if isinstance(log, bytes):
                log = log.decode(errors="replace")

            annotated_log = self._annotate_errors(source, log)
            Logger.error(
                f"Shader '{shader_name}' {stage_label} COMPILE ERROR:\n{annotated_log}"
            )

            glDeleteShader(shader)
            return 0

        return shader

    def _parse_uniforms_from_source(
        self, vert_src: str, frag_src: str
    ) -> dict[str, UniformInfo]:
        uniforms: dict[str, UniformInfo] = {}

        for src in (vert_src, frag_src):
            for match in _UNIFORM_RE.finditer(src):
                glsl_type = match.group(1)
                uname = match.group(2)
                array_size = int(match.group(3)) if match.group(3) else 1

                if uname in uniforms:
                    continue

                uniforms[uname] = UniformInfo(
                    name=uname,
                    glsl_type=glsl_type,
                    array_size=array_size,
                    is_engine=uname in _ENGINE_UNIFORMS,
                )

        return uniforms

    def _query_uniforms_gl(self, prog: ShaderProgram):
        count = glGetProgramiv(prog.gl_id, GL_ACTIVE_UNIFORMS)

        active_names: set[str] = set()
        for i in range(count):
            uname, size, utype = glGetActiveUniform(prog.gl_id, i)
            if isinstance(uname, bytes):
                uname = uname.decode(errors="replace")

            uname = re.sub(r"\[\d+\]$", "", uname)
            loc = glGetUniformLocation(prog.gl_id, uname)

            if uname in prog.uniforms:
                prog.uniforms[uname].location = loc
                type_info = GLSL_TYPE_MAP.get(utype)
                if type_info:
                    prog.uniforms[uname].glsl_type = type_info[0]
            else:
                type_info = GLSL_TYPE_MAP.get(utype)
                glsl_type_str = type_info[0] if type_info else f"gl_{utype}"
                prog.uniforms[uname] = UniformInfo(
                    name=uname,
                    glsl_type=glsl_type_str,
                    location=loc,
                    is_engine=uname in _ENGINE_UNIFORMS,
                )

            active_names.add(uname)

        for uname, info in prog.uniforms.items():
            if uname not in active_names:
                info.location = -1

    @staticmethod
    def _annotate_errors(source: str, log: str) -> str:
        lines = source.splitlines()
        annotated = []
        for log_line in log.splitlines():
            annotated.append(log_line)

            m = re.search(r":(\d+)[:(]", log_line)
            if m:
                lineno = int(m.group(1)) - 1
                if 0 <= lineno < len(lines):
                    annotated.append(f"   >>> {lines[lineno].strip()}")
        return "\n".join(annotated)


ShaderManager = _ShaderManagerSingleton()
