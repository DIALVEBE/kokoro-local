# Kokoro TTS local

Proyecto mínimo para generar voz local con Kokoro TTS en NixOS usando Flakes, direnv y uv.

No requiere API para sintetizar audio. El token de Hugging Face es opcional y solo sirve para autenticar descargas del Hub con mejores límites.

## Requisitos

- Nix con flakes habilitados
- direnv
- Git

## Instalar desde cero

```bash
git clone <URL_DEL_REPO>
cd kokoro-local
direnv allow
uv sync
```

Si no usas direnv:

```bash
nix develop path:$PWD -c uv sync
```

## Login opcional en Hugging Face

Crear un token en:

```text
https://huggingface.co/settings/tokens
```

Luego iniciar sesion:

```bash
hf auth login
hf auth whoami
```

Alternativa con variable local:

```bash
printf 'export HF_TOKEN=hf_xxx\n' > .env.local
direnv allow
```

`.env.local` esta ignorado por git. No guardes tokens en archivos versionados.

## Reconstruir o actualizar el entorno

Recargar el shell despues de cambiar `flake.nix` o `.envrc`:

```bash
direnv reload
```

Actualizar el lock de Nix:

```bash
nix flake update
direnv reload
```

Sin direnv:

```bash
nix develop path:$PWD -c uv sync
```

Actualizar dependencias Python:

```bash
uv lock --upgrade
uv sync
```

## Probar Kokoro

Generar audio con el texto de prueba:

```bash
uv run hablar
```

Generar audio con texto propio:

```bash
uv run hablar "Hola, soy tu asistente local" -o salida.wav
```

Reproducir:

```bash
ffplay salida.wav
```

## Voces documentadas

| Voz | Tipo | Hash |
| --- | --- | --- |
| `ef_dora` | femenina | `d9d69b0f` |
| `em_alex` | masculina | `5eac53f7` |
| `em_santa` | masculina | `aa8620cb` |

Listarlas desde el comando:

```bash
uv run hablar --list-voices
```

Probar las tres voces:

```bash
uv run hablar "Prueba con Dora" --voice ef_dora -o ef_dora.wav
uv run hablar "Prueba con Alex" --voice em_alex -o em_alex.wav
uv run hablar "Prueba con Santa" --voice em_santa -o em_santa.wav
```

## Comandos utiles

Verificar herramientas del entorno:

```bash
python --version
uv --version
hf version
espeak-ng --version
ffmpeg -version
```

Ver ayuda del comando:

```bash
uv run hablar --help
```
