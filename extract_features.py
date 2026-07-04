#!/usr/bin/env python3
"""Extrae características de audio para la visualización radio-retro.
Salida: features.json con, por clip y por frame de 100 ms:
  - dbfs: volumen RMS en dBFS (relativo digital, NO dB SPL)
  - f0: frecuencia fundamental (pYIN), Hz (0 = sin voz detectada)
  - centroid: centroide espectral, Hz
  - bands: 48 bandas mel de energía normalizada 0-99 (para el anillo)
"""
import json, numpy as np, librosa

SR = 22050
HOP_S = 0.10          # 100 ms
HOP = int(SR * HOP_S)
N_FFT = 2048
N_BANDS = 48

def analyze(path):
    y, _ = librosa.load(path, sr=SR, mono=True)
    dur = len(y) / SR

    # RMS -> dBFS
    rms = librosa.feature.rms(y=y, frame_length=N_FFT, hop_length=HOP)[0]
    dbfs = 20 * np.log10(rms + 1e-10)

    # F0 con YIN (rango voz + exclamaciones: 60-500 Hz), gateado por energía:
    # frames con RMS bajo (< mediana-6dB) se marcan como sin voz (f0=0)
    f0 = librosa.yin(y, fmin=60, fmax=500, sr=SR,
                     frame_length=N_FFT, hop_length=HOP)
    gate_db = 20 * np.log10(rms + 1e-10)
    thr = np.median(gate_db) - 6
    m = min(len(f0), len(gate_db))
    f0 = np.where(gate_db[:m] > thr, f0[:m], 0.0)

    # Centroide espectral
    cent = librosa.feature.spectral_centroid(y=y, sr=SR, n_fft=N_FFT,
                                             hop_length=HOP)[0]

    # Bandas mel para el anillo (48 bandas), escala log, normalizada 0-99
    mel = librosa.feature.melspectrogram(y=y, sr=SR, n_fft=N_FFT,
                                         hop_length=HOP, n_mels=N_BANDS,
                                         fmax=8000)
    meldb = librosa.power_to_db(mel, ref=np.max)          # <=0
    lo, hi = -60.0, 0.0
    bands = np.clip((meldb - lo) / (hi - lo), 0, 1) * 99  # 0-99

    n = min(len(dbfs), len(f0), len(cent), bands.shape[1])
    return {
        "hop": HOP_S,
        "dur": round(dur, 2),
        "dbfs": [round(float(v), 1) for v in dbfs[:n]],
        "f0": [round(float(v)) for v in f0[:n]],
        "centroid": [round(float(v)) for v in cent[:n]],
        # cada frame: string de 48 valores de 2 dígitos -> compacto
        "bands": ["".join(f"{int(v):02d}" for v in bands[:, i]) for i in range(n)],
    }

out = {}
for key, path in [("tudn", "/sessions/elegant-exciting-shannon/mnt/outputs/tudn.mp3"),
                  ("azteca", "/sessions/elegant-exciting-shannon/mnt/outputs/canal2.mp3")]:
    print("analizando", key)
    out[key] = analyze(path)

with open("/tmp/features.json", "w") as f:
    json.dump(out, f, separators=(",", ":"))
print("listo", {k: len(v["dbfs"]) for k, v in out.items()})

# Resumen estadístico para el análisis comparativo
for k, v in out.items():
    db = np.array(v["dbfs"]); f0 = np.array(v["f0"], float); ce = np.array(v["centroid"], float)
    voiced = f0[f0 > 0]
    print(f"\n== {k} ==")
    print(f"dBFS  med={np.median(db):.1f}  p95={np.percentile(db,95):.1f}  max={db.max():.1f}  std={db.std():.1f}")
    print(f"F0    med={np.median(voiced):.0f}Hz  p90={np.percentile(voiced,90):.0f}  max={voiced.max():.0f}  %voz={100*len(voiced)/len(f0):.0f}%")
    print(f"cent  med={np.median(ce):.0f}Hz  p90={np.percentile(ce,90):.0f}")
    # picos: momentos con dbfs > p97
    thr = np.percentile(db, 97)
    idx = np.where(db > thr)[0]
    print("picos(s):", sorted(set((idx * 0.1).round(0).astype(int).tolist()))[:25])
