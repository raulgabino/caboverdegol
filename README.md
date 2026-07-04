# Dos radios, un gol

Análisis comparativo de dos narraciones del gol de Sidny Lopes Cabral (Cabo Verde 2–2 Argentina,
16avos de final, Copa Mundial FIFA 2026): la transmisión de TUDN y el clip de highlights de TV Azteca Deportes.

Visualización interactiva estilo radio Braun: el dial de cada radio es un anillo de espectro real
(48 bandas mel calculadas cada 100 ms) sincronizado con la reproducción. Incluye un comparador de bolsillo
con recorrido guiado por momentos alineados de la jugada, y un banco multibanda con la evidencia medida.

**Demo local:** abrir `index.html` en un navegador (los `.mp3` deben estar en la misma carpeta).

## Metodología (resumen)

- Audio extraído de YouTube; al clip de TUDN se le recortaron los primeros 4.8 s (cortinilla de entrada).
- Características por cuadro de 100 ms: dBFS (RMS), F0 (YIN con gate por energía), centroide espectral,
  48 bandas mel, flux espectral, tasa de onsets, ΔF0.
- Pausas: mezcla < mediana−10 dB durante ≥0.3 s. HNR por autocorrelación; jitter/shimmer aproximados
  con YIN fino (hop 5 ms) — no Praat, no voz aislada.
- Transcripción automática con faster-whisper (modelo base, es), aproximada.

**Límites declarados:** las mediciones son dBFS (volumen digital relativo dentro de cada mezcla), no dB SPL;
ambas pistas mezclan relator + comentarista + estadio y se analizan como una sola señal; la transcripción
contiene errores y el grito de gol es ininteligible para el modelo. Detalle completo en la pestaña «Método»
de la página.

## Nota sobre el audio

Los clips de audio pertenecen a sus emisoras (TUDN México / TV Azteca Deportes) y se incluyen únicamente
como material de análisis y crítica en un proyecto personal sin fines comerciales.

---

Elaborado por **Raúl Gabino** · [WhatsApp +52 834 130 9459](https://wa.me/528341309459)
