#version 330 core
out vec4 FragColor;
in vec3 TexCoords;
uniform samplerCube skybox;
uniform bool use_fallback;
void main() {
    if (use_fallback) {
        float factor = normalize(TexCoords).y * 0.5 + 0.5;

        vec3 topColor = vec3(0.02, 0.55, 0.9);
        vec3 bottomColor = vec3(0.55, 0.53, 0.53);
        vec3 color = mix(bottomColor, topColor, factor);
        
        FragColor = vec4(color, 1.0);
    } else {
        FragColor = texture(skybox, TexCoords);
    }
}