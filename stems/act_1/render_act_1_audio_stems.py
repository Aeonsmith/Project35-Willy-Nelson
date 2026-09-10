#!/usr/bin/env python3
"""
render_act_1_audio_stems.py
Renders 24-bit / 48 kHz multi-track audio stems for Act I (Tracks 01-04) of Project 35: Willy Nelson.
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

def render_act_1():
    base_dir = Path(__file__).resolve().parent
    audio_dir = base_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    
    print("Rendering Act I 24-bit / 48 kHz multi-track audio stems...")
    dur = 3.0
    n = int(SAMPLE_RATE * dur)
    
    # -------------------------------------------------------------
    # TRACK 01: RESENTFUL (130 BPM, C Minor)
    # -------------------------------------------------------------
    # Stem 1: 808 Sub (C1 = 32.7 Hz)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        sl[i] = math.sin(2 * math.pi * 32.70 * t) * (1.0 - math.exp(-t * 2.0)) * math.exp(-t * 0.4)
        sr[i] = sl[i]
    write_wav(audio_dir / "01_Resentful_Stem_808Sub.wav", sl, sr)
    
    # Stem 2: Trap Drums (Kick at 55Hz + Skeletal Snare)
    sl, sr = [0.0]*n, [0.0]*n
    beat_dur = 60.0 / 130.0
    for i in range(n):
        t = i / SAMPLE_RATE
        pos = (t % beat_dur)
        kick = math.sin(2*math.pi*55.0*pos) * math.exp(-pos * 20.0) if pos < 0.2 else 0.0
        snare_pos = ((t + beat_dur/2) % beat_dur)
        snare = (random.random()*2-1)*math.exp(-snare_pos * 25.0)*0.5 if snare_pos < 0.2 else 0.0
        sl[i] = kick + snare
        sr[i] = kick + snare
    write_wav(audio_dir / "01_Resentful_Stem_TrapDrums.wav", sl, sr)
    
    # Stem 3: Dark Pad (C Minor / Ab Major)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        c_chord = (math.sin(2*math.pi*130.81*t) + math.sin(2*math.pi*155.56*t) + math.sin(2*math.pi*196.00*t)) * 0.3
        sl[i] = c_chord * (0.8 + 0.2 * math.sin(2*math.pi*0.5*t))
        sr[i] = c_chord * (0.8 + 0.2 * math.cos(2*math.pi*0.5*t))
    write_wav(audio_dir / "01_Resentful_Stem_DarkPad.wav", sl, sr)

    # Stem 4: Reverse Chords
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        env = (t / dur) ** 2
        sl[i] = math.sin(2*math.pi*261.63*t) * env * 0.4
        sr[i] = math.sin(2*math.pi*311.13*t) * env * 0.4
    write_wav(audio_dir / "01_Resentful_Stem_ReverseChords.wav", sl, sr)

    # -------------------------------------------------------------
    # TRACK 02: SAVAGE GA$P (128 BPM, D Minor)
    # -------------------------------------------------------------
    # Stem 1: Sub 808 (D1 = 36.7 Hz)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        sl[i] = math.sin(2 * math.pi * 36.71 * t) * math.exp(-t * 0.3)
        sr[i] = sl[i]
    write_wav(audio_dir / "02_SavageGasp_Stem_Sub808.wav", sl, sr)

    # Stem 2: Drill Hats Percussion
    sl, sr = [0.0]*n, [0.0]*n
    trip_dur = (60.0 / 128.0) / 3.0
    for i in range(n):
        t = i / SAMPLE_RATE
        pos = t % trip_dur
        hat = (random.random()*2-1) * math.exp(-pos * 60.0) * 0.4
        sl[i] = hat * 0.7
        sr[i] = hat * 1.0
    write_wav(audio_dir / "02_SavageGasp_Stem_DrillHats_Perc.wav", sl, sr)

    # Stem 3: Gothic Choir Chops (D Minor)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        choir = (math.sin(2*math.pi*146.83*t) + math.sin(2*math.pi*174.61*t) + math.sin(2*math.pi*220.00*t)) * 0.3
        sl[i] = choir * math.sin(2*math.pi*2.0*t)
        sr[i] = choir * math.cos(2*math.pi*2.0*t)
    write_wav(audio_dir / "02_SavageGasp_Stem_GothicChoir.wav", sl, sr)

    # Stem 4: Distorted Pluck
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        pluck = math.sin(2*math.pi*587.33*t) * math.exp(-(t % 0.25)*15.0)
        dist = math.tanh(pluck * 2.5) * 0.4
        sl[i] = dist
        sr[i] = dist * 0.8
    write_wav(audio_dir / "02_SavageGasp_Stem_DistortedPluck.wav", sl, sr)

    # -------------------------------------------------------------
    # TRACK 03: CHRIS BROWN (KING) (135 BPM, F Minor)
    # -------------------------------------------------------------
    # Stem 1: Saturated 808 (F1 = 43.65 Hz)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        raw = math.sin(2*math.pi*43.65*t) + 0.3*math.sin(2*math.pi*87.30*t)
        sl[i] = math.tanh(raw * 2.0) * 0.5
        sr[i] = sl[i]
    write_wav(audio_dir / "03_King_Stem_Saturated808.wav", sl, sr)

    # Stem 2: Stadium Kick & Snare
    sl, sr = [0.0]*n, [0.0]*n
    b_dur = 60.0 / 135.0
    for i in range(n):
        t = i / SAMPLE_RATE
        k_pos = t % b_dur
        kick = math.sin(2*math.pi*60.0*k_pos) * math.exp(-k_pos * 18.0) * 0.8 if k_pos < 0.25 else 0.0
        sn_pos = (t + b_dur/2) % b_dur
        snare = (random.random()*2-1)*math.exp(-sn_pos * 20.0)*0.7 if sn_pos < 0.25 else 0.0
        sl[i] = kick + snare
        sr[i] = kick + snare
    write_wav(audio_dir / "03_King_Stem_StadiumKickSnare.wav", sl, sr)

    # Stem 3: Brass Fanfare (F Minor Octaves)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        brass = (math.sin(2*math.pi*174.61*t) + 0.7*math.sin(2*math.pi*349.23*t) + 0.5*math.sin(2*math.pi*523.25*t)) * 0.35
        sl[i] = brass
        sr[i] = brass * 0.9
    write_wav(audio_dir / "03_King_Stem_BrassFanfare.wav", sl, sr)

    # Stem 4: Grand Piano
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        piano = (math.sin(2*math.pi*87.31*t) + math.sin(2*math.pi*103.83*t) + math.sin(2*math.pi*130.81*t)) * math.exp(-t*0.5) * 0.4
        sl[i] = piano
        sr[i] = piano
    write_wav(audio_dir / "03_King_Stem_GrandPiano.wav", sl, sr)

    # -------------------------------------------------------------
    # TRACK 04: CLEJAN 11 (MIRROR) (132 BPM, G Minor)
    # -------------------------------------------------------------
    # Stem 1: Solo Violin Mic Left (G3 to D5 Runs)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        freq = 392.0 + 50.0 * math.sin(2*math.pi*4.0*t)  # Vibrato G4
        saw = (2.0 * (t * freq - math.floor(0.5 + t * freq))) * 0.4
        sl[i] = saw
        sr[i] = saw * 0.3
    write_wav(audio_dir / "04_Clejan_Stem_SoloViolin_MicL.wav", sl, sr)

    # Stem 2: Solo Violin Mic Right (Stereo Room Ambience)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        freq = 392.0 + 50.0 * math.sin(2*math.pi*4.0*t + 0.5)
        saw = (2.0 * (t * freq - math.floor(0.5 + t * freq))) * 0.4
        sl[i] = saw * 0.3
        sr[i] = saw
    write_wav(audio_dir / "04_Clejan_Stem_SoloViolin_MicR.wav", sl, sr)

    # Stem 3: Violin Cadenza Ostinato (Fast 16th Note Spiccato)
    sl, sr = [0.0]*n, [0.0]*n
    sixteenth_dur = (60.0 / 132.0) / 4.0
    for i in range(n):
        t = i / SAMPLE_RATE
        s_pos = t % sixteenth_dur
        note_idx = int(t / sixteenth_dur) % 4
        notes = [392.0, 466.16, 587.33, 783.99]  # G, Bb, D, G
        f = notes[note_idx]
        spiccato = math.sin(2*math.pi*f*t) * math.exp(-s_pos * 35.0) * 0.45
        sl[i] = spiccato
        sr[i] = spiccato
    write_wav(audio_dir / "04_Clejan_Stem_ViolinCadenza_Ostinato.wav", sl, sr)

    # Stem 4: Glide 808 & Trap Drums
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        glide_freq = 49.0 - 15.0 * (t / dur)  # G1 glide down
        bass = math.sin(2*math.pi*glide_freq*t) * 0.6
        sl[i] = bass
        sr[i] = bass
    write_wav(audio_dir / "04_Clejan_Stem_Glide808_TrapDrums.wav", sl, sr)

    print(f"All 16 Act I audio stems successfully rendered in {audio_dir}!")

if __name__ == "__main__":
    render_act_1()
