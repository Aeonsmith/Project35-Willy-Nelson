#!/usr/bin/env python3
"""
render_act_2_audio_stems.py
Renders 24-bit / 48 kHz multi-track audio stems for Act II (Tracks 05-07) of Project 35: Willy Nelson.
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

def render_act_2():
    base_dir = Path(__file__).resolve().parent
    audio_dir = base_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    
    print("Rendering Act II 24-bit / 48 kHz multi-track audio stems...")
    dur = 3.0
    n = int(SAMPLE_RATE * dur)
    
    # -------------------------------------------------------------
    # TRACK 05: A.ROB (PS5) (90 BPM, A Minor)
    # -------------------------------------------------------------
    # Stem 1: Chopped Break Kick (90 BPM)
    sl, sr = [0.0]*n, [0.0]*n
    beat_dur = 60.0 / 90.0
    for i in range(n):
        t = i / SAMPLE_RATE
        pos = t % beat_dur
        # SP-1200 style punchy vinyl kick
        kick = math.sin(2*math.pi*55.0*pos) * math.exp(-pos * 22.0) if pos < 0.25 else 0.0
        sl[i] = kick
        sr[i] = kick
    write_wav(audio_dir / "05_ARob_Stem_ChoppedBreakKick.wav", sl, sr)

    # Stem 2: Gritty Snare & Vinyl Hats
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        sn_pos = (t + beat_dur/2) % beat_dur
        snare = (random.random()*2-1) * math.exp(-sn_pos * 18.0) * 0.7 if sn_pos < 0.25 else 0.0
        vinyl_noise = (random.random()*2-1) * 0.05
        sl[i] = snare + vinyl_noise
        sr[i] = snare + vinyl_noise
    write_wav(audio_dir / "05_ARob_Stem_GrittySnareVinyl.wav", sl, sr)

    # Stem 3: Moog Bass (A Minor: A1 = 55 Hz)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        bass = (math.sin(2*math.pi*55.0*t) + 0.4*math.sin(2*math.pi*110.0*t)) * math.exp(-(t % (beat_dur*2))*1.5)
        sl[i] = bass * 0.7
        sr[i] = bass * 0.7
    write_wav(audio_dir / "05_ARob_Stem_MoogBass_AMinor.wav", sl, sr)

    # Stem 4: Muted Acoustic Guitar (A Minor Plucks)
    sl, sr = [0.0]*n, [0.0]*n
    eighth_dur = beat_dur / 2.0
    for i in range(n):
        t = i / SAMPLE_RATE
        pos = t % eighth_dur
        note = [220.0, 261.63, 329.63, 440.0][int(t / eighth_dur) % 4]
        pluck = math.sin(2*math.pi*note*t) * math.exp(-pos * 25.0) * 0.4
        sl[i] = pluck * 0.9
        sr[i] = pluck * 0.5
    write_wav(audio_dir / "05_ARob_Stem_MutedAcousticGuitar.wav", sl, sr)

    # -------------------------------------------------------------
    # TRACK 06: TOKEN (GENERAL) {METHANE GAS} (150 BPM, E Minor)
    # -------------------------------------------------------------
    # Stem 1: Punch Kick & 32nd Hat Rolls
    sl, sr = [0.0]*n, [0.0]*n
    b_dur_150 = 60.0 / 150.0
    thirtysecond_dur = b_dur_150 / 8.0
    for i in range(n):
        t = i / SAMPLE_RATE
        k_pos = t % b_dur_150
        kick = math.sin(2*math.pi*65.0*k_pos) * math.exp(-k_pos * 30.0) * 0.8 if k_pos < 0.15 else 0.0
        h_pos = t % thirtysecond_dur
        hat = (random.random()*2-1) * math.exp(-h_pos * 80.0) * 0.3
        sl[i] = kick + hat * 0.6
        sr[i] = kick + hat * 0.9
    write_wav(audio_dir / "06_Token_Stem_PunchKick_32ndHats.wav", sl, sr)

    # Stem 2: Clipped Distorted 808 (E1 = 41.2 Hz)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        raw = math.sin(2*math.pi*41.20*t) + 0.5*math.sin(2*math.pi*82.40*t)
        dist = math.tanh(raw * 3.0) * 0.6
        sl[i] = dist
        sr[i] = dist
    write_wav(audio_dir / "06_Token_Stem_ClippedDistorted808.wav", sl, sr)

    # Stem 3: Industrial Siren Lead
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        s_freq = 1400.0 + 400.0 * math.sin(2*math.pi*3.0*t)
        siren = math.sin(2*math.pi*s_freq*t) * 0.35
        sl[i] = siren
        sr[i] = siren * 0.8
    write_wav(audio_dir / "06_Token_Stem_IndustrialSirenLead.wav", sl, sr)

    # Stem 4: Rapid Synth Arp (E Minor)
    sl, sr = [0.0]*n, [0.0]*n
    triplet_dur = b_dur_150 / 3.0
    for i in range(n):
        t = i / SAMPLE_RATE
        pos = t % triplet_dur
        arp_note = [329.63, 392.00, 493.88, 659.25][int(t / triplet_dur) % 4]
        arp = math.sin(2*math.pi*arp_note*t) * math.exp(-pos * 35.0) * 0.4
        sl[i] = arp * 0.4
        sr[i] = arp * 0.9
    write_wav(audio_dir / "06_Token_Stem_RapidSynthArp_EMinor.wav", sl, sr)

    # -------------------------------------------------------------
    # TRACK 07: MAC LETHAL (HEARTBREAK DAYS) (86 BPM, G Minor to G Major)
    # -------------------------------------------------------------
    # Stem 1: Loose Kick & Wood Snare (86 BPM)
    sl, sr = [0.0]*n, [0.0]*n
    b_dur_86 = 60.0 / 86.0
    for i in range(n):
        t = i / SAMPLE_RATE
        k_pos = t % b_dur_86
        kick = math.sin(2*math.pi*48.0*k_pos) * math.exp(-k_pos * 12.0) * 0.7 if k_pos < 0.3 else 0.0
        sn_pos = (t + b_dur_86/2) % b_dur_86
        snare = ((random.random()*2-1)*0.4 + math.sin(2*math.pi*200*sn_pos)*0.4) * math.exp(-sn_pos * 15.0) if sn_pos < 0.3 else 0.0
        sl[i] = kick + snare
        sr[i] = kick + snare
    write_wav(audio_dir / "07_MacLethal_Stem_LooseKickWoodSnare.wav", sl, sr)

    # Stem 2: Deep Sub Bass (G1 = 49.0 Hz)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        sub = math.sin(2*math.pi*49.00*t) * 0.6 * math.exp(-t * 0.2)
        sl[i] = sub
        sr[i] = sub
    write_wav(audio_dir / "07_MacLethal_Stem_DeepSubBass_GMinor.wav", sl, sr)

    # Stem 3: Rhodes Electric Piano (Tremolo)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        rhodes = (math.sin(2*math.pi*196.00*t) + math.sin(2*math.pi*233.08*t) + math.sin(2*math.pi*293.66*t)) * math.exp(-t*0.6) * 0.35
        trem_l = 0.5 + 0.5 * math.sin(2*math.pi*4.0*t)
        trem_r = 0.5 + 0.5 * math.cos(2*math.pi*4.0*t)
        sl[i] = rhodes * trem_l
        sr[i] = rhodes * trem_r
    write_wav(audio_dir / "07_MacLethal_Stem_RhodesEPiano.wav", sl, sr)

    # Stem 4: Acoustic Cello (G Minor to G Major Resolution)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        # Shifts from Bb (Minor 3rd = 116.54Hz) to B natural (Major 3rd = 123.47Hz) at t=1.5s
        c_note = 116.54 if t < 1.5 else 123.47
        cello = (math.sin(2*math.pi*98.00*t) + 0.8*math.sin(2*math.pi*c_note*t) + 0.5*math.sin(2*math.pi*146.83*t)) * 0.35
        sl[i] = cello * 0.7
        sr[i] = cello * 0.9
    write_wav(audio_dir / "07_MacLethal_Stem_AcousticCello_GMinorToMajor.wav", sl, sr)

    print(f"All 12 Act II audio stems successfully rendered in {audio_dir}!")

if __name__ == "__main__":
    render_act_2()
