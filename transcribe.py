#!/usr/bin/env python3
import json, sys
from faster_whisper import WhisperModel

key, path = sys.argv[1], sys.argv[2]
model = WhisperModel("base", device="cpu", compute_type="int8")
segs, info = model.transcribe(path, language="es", vad_filter=True, beam_size=1)
out = [{"t0": round(s.start, 1), "t1": round(s.end, 1), "text": s.text.strip()} for s in segs]
with open(f"/tmp/transcript_{key}.json", "w") as f:
    json.dump(out, f, ensure_ascii=False)
print(key, len(out), "segmentos")
