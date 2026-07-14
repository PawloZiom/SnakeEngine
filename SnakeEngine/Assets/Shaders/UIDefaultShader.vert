#version 330 core
layout (location = 0) in vec2 aPos;
layout (location = 1) in vec2 aTexCoord;
layout (location = 2) in vec4 aColor;

out vec2 TexCoord;
out vec4 Color;

uniform vec2 screenSize;

void main() {
    float x = (aPos.x / screenSize.x) * 2.0 - 1.0;
    float y = 1.0 - (aPos.y / screenSize.y) * 2.0;
    gl_Position = vec4(x, y, 0.0, 1.0);
    TexCoord = aTexCoord;
    Color = aColor;
}