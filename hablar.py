from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import soundfile as sf
from kokoro import KPipeline


VOICES = {
    "ef_dora": {"gender": "femenina", "hash": "d9d69b0f"},
    "em_alex": {"gender": "masculina", "hash": "5eac53f7"},
    "em_santa": {"gender": "masculina", "hash": "aa8620cb"},
}

DEFAULT_TEXT = """
¡Hola! ¿Cómo estás?

Qué gusto saludarte. Hoy quiero contarte algo que, sinceramente, me parece fascinante: esta voz está siendo generada completamente de manera local, desde un computador con NixOS, sin utilizar APIs externas, sin suscripciones y, por supuesto, sin pagar por cada palabra generada.

Suena interesante, ¿verdad?

La idea es probar qué tan natural puede llegar a sentirse una conversación. Por eso estoy utilizando pausas, preguntas, exclamaciones y diferentes ritmos al hablar.

Por ejemplo... imagina que estamos en una clase de inteligencia artificial.

“Buenos días a todos. Antes de comenzar, quiero hacerles una pregunta: ¿ustedes creen que una máquina realmente puede pensar?”

¡No respondan todavía!

Piénsenlo durante unos segundos... porque la respuesta no es tan sencilla como parece.

Ahora cambiemos un poco el tono.

A veces hablamos rápido; otras veces, hacemos una pausa para organizar nuestras ideas. También podemos enfatizar ciertas palabras, expresar sorpresa, alegría o incluso duda.

¿En serio? ¡Eso está increíble!

Bueno... quizá “increíble” sea una palabra un poco exagerada, pero definitivamente estamos llegando a un punto muy interesante.

También quiero probar algunas palabras con tildes y sonidos particulares del español: inteligencia artificial, programación, información, comunicación, tecnología, educación, análisis, investigación, generación, configuración, corazón, canción, acción y precisión.

Probemos también con la letra eñe: niño, mañana, enseñanza, español, diseño, compañero y sueño.

Y ahora una frase un poco más larga:

Aunque la inteligencia artificial ha avanzado rápidamente durante los últimos años, todavía existen muchos desafíos relacionados con la precisión, la interpretación del contexto y la manera en que las personas interactúan con estos sistemas.

¿Se escucha natural?

Perfecto. Entonces, si todo está funcionando correctamente, el siguiente paso será conectar esta voz con un modelo de inteligencia artificial local para poder mantener una conversación completa, de principio a fin, sin depender de servicios externos.

¡Y ahí sí se pone realmente interesante!
"""


def synthesize(text: str, output: Path, voice: str, speed: float) -> None:
    pipeline = KPipeline(lang_code="e")
    generator = pipeline(text, voice=voice, speed=speed)

    audios = [audio for _, _, audio in generator]
    if not audios:
        raise RuntimeError("Kokoro no genero audio para el texto indicado.")

    audio_final = np.concatenate(audios)
    sf.write(output, audio_final, 24000)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Genera audio local con Kokoro TTS.",
    )
    parser.add_argument(
        "texto",
        nargs="*",
        help="Texto a sintetizar. Si se omite, usa una prueba predeterminada.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="prueba.wav",
        type=Path,
        help="Archivo de salida WAV. Valor por defecto: prueba.wav",
    )
    parser.add_argument(
        "--voice",
        default="em_alex",
        choices=sorted(VOICES),
        help="Voz de Kokoro. Valor por defecto: em_alex",
    )
    parser.add_argument(
        "--speed",
        default=1.0,
        type=float,
        help="Velocidad de habla. Valor por defecto: 1.0",
    )
    parser.add_argument(
        "--list-voices",
        action="store_true",
        help="Lista las voces documentadas para este proyecto.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.list_voices:
        for name, metadata in VOICES.items():
            print(f"{name}\t{metadata['gender']}\t{metadata['hash']}")
        return

    text = " ".join(args.texto).strip() or DEFAULT_TEXT
    synthesize(text, args.output, args.voice, args.speed)
    print(f"Audio generado: {args.output}")


if __name__ == "__main__":
    main()
