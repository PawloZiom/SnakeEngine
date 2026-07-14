#version 330 core
in vec2 TexCoord;
in vec4 Color;

out vec4 FragColor;

uniform sampler2D fontTexture;
uniform int isImage;

void main() {
    if (TexCoord == vec2(0.0, 0.0)) {
        FragColor = Color;
    } else if (isImage == 1) {
        vec4 tex = texture(fontTexture, TexCoord);
        if (tex.a < 0.05) discard;
        FragColor = tex * Color;
    } else {
        vec4 tex = texture(fontTexture, TexCoord);
        if (tex.a < 0.05) discard;
        FragColor = vec4(Color.rgb, tex.a * Color.a);
    }
}