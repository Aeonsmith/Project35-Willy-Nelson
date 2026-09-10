#!/usr/bin/env python3
"""
render_act_3_audio_stems.py
Renders 24-bit / 48 kHz multi-track audio stems for Act III (Tracks 08-10) of Project 35: Willy Nelson.
"""

import math
import random
import struct
import wave
from pathlib import Path

SAMPLE_RATE = 48000

def write_wav(filepath: Path, samples_l: list, samples_r: list):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    n = len(samples_l)
    max_val = max(max(abs(s) for s in samples_l), max(abs(s) for s in samples_r), 1e-6)
    target_peak = 0.50  # -6 dBFS headroom
    gain = target_peak / max_val if max_val > 0 else 1.0
    
    with wave.open(str(filepath), 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(3)  # 24-bit
        wf.setframerate(SAMPLE_RATE)
        raw_bytes = bytearray()
        for i in range(n):
            sl = int(max(min(samples_l[i] * gain, 1.0), -1.0) * 8388607.0)
            sr = int(max(min(samples_r[i] * gain, 1.0), -1.0) * 8388607.0)
            raw_bytes.extend(sl.to_bytes(3, byteorder='little', signed=True))
            raw_bytes.extend(sr.to_bytes(3, byteorder='little', signed=True))
        wf.writeframes(raw_bytes)

def render_act_3():
    base_dir = Path(__file__).resolve().parent
    audio_dir = base_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    
    print("Rendering Act III 24-bit / 48 kHz multi-track audio stems...")
    dur = 3.0
    n = int(SAMPLE_RATE * dur)
    
    # -------------------------------------------------------------
    # TRACK 08: MJ (124 BPM, G Major)
    # -------------------------------------------------------------
    # Stem 1: Stadium Kick & Snare/Clap Stack (124 BPM)
    sl, sr = [0.0]*n, [0.0]*n
    beat_dur_124 = 60.0 / 124.0
    for i in range(n):
        t = i / SAMPLE_RATE
        k_pos = t % beat_dur_124
        kick = math.sin(2*math.pi*58.0*k_pos) * math.exp(-k_pos * 20.0) * 0.8 if k_pos < 0.2 else 0.0
        sn_pos = (t + beat_dur_124/2) % beat_dur_124
        snare = ((random.random()*2-1)*0.6 + math.sin(2*math.pi*240.0*sn_pos)*0.4) * math.exp(-sn_pos * 22.0) if sn_pos < 0.2 else 0.0
        sl[i] = kick + snare
        sr[i] = kick + snare
    write_wav(audio_dir / "08_MJ_Stem_StadiumKickSnare.wav", sl, sr)

    # Stem 2: Wide Stereo Bass (G1 = 49 Hz)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        bass = (math.sin(2*math.pi*49.0*t) + 0.3*math.sin(2*math.pi*98.0*t)) * 0.7
        sl[i] = bass * (0.8 + 0.2 * math.sin(2*math.pi*1.0*t))
        sr[i] = bass * (0.8 + 0.2 * math.cos(2*math.pi*1.0*t))
    write_wav(audio_dir / "08_MJ_Stem_WideStereoBass.wav", sl, sr)

    # Stem 3: Brass Fanfare Horns (3 Trumpets, 2 Trombones)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        horns = (math.sin(2*math.pi*196.00*t) + 0.8*math.sin(2*math.pi*246.94*t) + 0.6*math.sin(2*math.pi*293.66*t) + 0.4*math.sin(2*math.pi*392.00*t)) * 0.35
        sl[i] = horns * 0.9
        sr[i] = horns * 0.95
    write_wav(audio_dir / "08_MJ_Stem_BrassFanfareHorns.wav", sl, sr)

    # Stem 4: Anthemic Choir Chops
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        choir = (math.sin(2*math.pi*392.0*t) + math.sin(2*math.pi*493.88*t) + math.sin(2*math.pi*587.33*t)) * 0.25 * (0.5 + 0.5*math.sin(2*math.pi*4.0*t))
        sl[i] = choir
        sr[i] = choir
    write_wav(audio_dir / "08_MJ_Stem_AnthemicChoirChops.wav", sl, sr)

    # -------------------------------------------------------------
    # TRACK 09: MESSI (140 BPM, A Minor)
    # -------------------------------------------------------------
    # Stem 1: Tight Kick & Snap Snare (140 BPM)
    sl, sr = [0.0]*n, [0.0]*n
    b_dur_140 = 60.0 / 140.0
    for i in range(n):
        t = i / SAMPLE_RATE
        k_pos = t % b_dur_140
        kick = math.sin(2*math.pi*62.0*k_pos) * math.exp(-k_pos * 28.0) * 0.85 if k_pos < 0.15 else 0.0
        sn_pos = (t + b_dur_140/2) % b_dur_140
        snap = (random.random()*2-1) * math.exp(-sn_pos * 40.0) * 0.6 if sn_pos < 0.15 else 0.0
        sl[i] = kick + snap
        sr[i] = kick + snap
    write_wav(audio_dir / "09_Messi_Stem_TightKickSnapSnare.wav", sl, sr)

    # Stem 2: Drill Hi-Hat Skips & Glitch Shakers
    sl, sr = [0.0]*n, [0.0]*n
    sixteenth_140 = b_dur_140 / 4.0
    for i in range(n):
        t = i / SAMPLE_RATE
        pos = t % sixteenth_140
        skip = (random.random()*2-1) * math.exp(-pos * 70.0) * 0.4
        sl[i] = skip * 0.6
        sr[i] = skip * 1.0
    write_wav(audio_dir / "09_Messi_Stem_DrillHiHatSkips.wav", sl, sr)

    # Stem 3: Gliding 808 Octaves (A1 = 55 Hz -> A2 = 110 Hz -> E1 = 41.2 Hz)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        # Glide frequency modulation
        g_freq = 55.0 if t < 1.0 else (110.0 if t < 2.0 else 41.20)
        bass = math.sin(2*math.pi*g_freq*t) * 0.7
        sl[i] = bass
        sr[i] = bass
    write_wav(audio_dir / "09_Messi_Stem_Gliding808_Octaves.wav", sl, sr)

    # Stem 4: Kalimba & Marimba Lead (A Minor Pentatonic)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        k_note = [440.0, 523.25, 587.33, 659.25, 783.99][int(t / sixteenth_140) % 5]
        kalimba = math.sin(2*math.pi*k_note*t) * math.exp(-(t % sixteenth_140)*25.0) * 0.4
        sl[i] = kalimba * 0.8
        sr[i] = kalimba * 0.4
    write_wav(audio_dir / "09_Messi_Stem_KalimbaMarimbaLead.wav", sl, sr)

    # -------------------------------------------------------------
    # TRACK 10: (DON’T PLAY GOLF) {GOT TWO GOLF PLANES} (126 BPM, Bb Major)
    # -------------------------------------------------------------
    # Stem 1: Punchy Grime Kick (126 BPM)
    sl, sr = [0.0]*n, [0.0]*n
    b_dur_126 = 60.0 / 126.0
    for i in range(n):
        t = i / SAMPLE_RATE
        k_pos = t % b_dur_126
        kick = math.sin(2*math.pi*60.0*k_pos) * math.exp(-k_pos * 24.0) * 0.8 if k_pos < 0.2 else 0.0
        sl[i] = kick
        sr[i] = kick
    write_wav(audio_dir / "10_DontPlayGolf_Stem_PunchyGrimeKick.wav", sl, sr)

    # Stem 2: Bounce Synth Bass (Bb1 = 58.27 Hz)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        bounce = math.sin(2*math.pi*58.27*t) * math.exp(-(t % (b_dur_126/2))*10.0) * 0.65
        sl[i] = bounce
        sr[i] = bounce
    write_wav(audio_dir / "10_DontPlayGolf_Stem_BounceSynthBass.wav", sl, sr)

    # Stem 3: Gramophone Chops (Phonograph Bandpassed Strings)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        strings = (math.sin(2*math.pi*466.16*t) + math.sin(2*math.pi*587.33*t) + math.sin(2*math.pi*698.46*t)) * 0.3
        phono_noise = (random.random()*2-1) * 0.06
        sl[i] = (strings + phono_noise) * 0.7
        sr[i] = (strings + phono_noise) * 0.4
    write_wav(audio_dir / "10_DontPlayGolf_Stem_GramophoneChops.wav", sl, sr)

    # Stem 4: Satirical Brass Stabs (Bb Major Fanfare)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        stab = (math.sin(2*math.pi*233.08*t) + math.sin(2*math.pi*466.16*t) + math.sin(2*math.pi*698.46*t)) * math.exp(-(t % b_dur_126)*15.0) * 0.45
        sl[i] = stab * 0.4
        sr[i] = stab * 0.9
    write_wav(audio_dir / "10_DontPlayGolf_Stem_SatiricalBrassStabs.wav", sl, sr)

    print(f"All 12 Act III audio stems successfully rendered in {audio_dir}!")

if __name__ == "__main__":
    render_act_3()
