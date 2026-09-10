#!/usr/bin/env python3
"""
render_act_4_audio_stems.py
Renders 24-bit / 48 kHz multi-track audio stems for Act IV (Tracks 11-12) of Project 35: Willy Nelson.
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

def render_act_4():
    base_dir = Path(__file__).resolve().parent
    audio_dir = base_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    
    print("Rendering Act IV 24-bit / 48 kHz multi-track audio stems...")
    dur = 3.0
    n = int(SAMPLE_RATE * dur)
    
    # -------------------------------------------------------------
    # TRACK 11: ARMANI WHITE (WINNING MY FUTURE) (104 BPM, G Minor to G Major)
    # -------------------------------------------------------------
    # Stem 1: Four-on-the-Floor 909 Kick & Analog Claps
    sl, sr = [0.0]*n, [0.0]*n
    b_dur_104 = 60.0 / 104.0
    for i in range(n):
        t = i / SAMPLE_RATE
        k_pos = t % b_dur_104
        kick = math.sin(2*math.pi*55.0*k_pos) * math.exp(-k_pos * 18.0) * 0.85 if k_pos < 0.25 else 0.0
        sn_pos = (t + b_dur_104/2) % b_dur_104
        clap = ((random.random()*2-1)*0.6 + math.sin(2*math.pi*1800.0*sn_pos)*0.4) * math.exp(-sn_pos * 30.0) if sn_pos < 0.2 else 0.0
        sl[i] = kick + clap
        sr[i] = kick + clap
    write_wav(audio_dir / "11_ArmaniWhite_Stem_FourOnFloorKick_909.wav", sl, sr)

    # Stem 2: Live Slap Bass (Music Man StingRay / Avalon U5 Tone)
    sl, sr = [0.0]*n, [0.0]*n
    sixteenth_104 = b_dur_104 / 4.0
    for i in range(n):
        t = i / SAMPLE_RATE
        pos = t % sixteenth_104
        # Slap pop transient + fundamental (G1 = 49Hz)
        slap_thud = math.sin(2*math.pi*49.0*t) * math.exp(-pos * 20.0) * 0.7
        pop_click = math.sin(2*math.pi*2500.0*pos) * math.exp(-pos * 60.0) * 0.3
        sl[i] = slap_thud + pop_click
        sr[i] = slap_thud + pop_click
    write_wav(audio_dir / "11_ArmaniWhite_Stem_LiveSlapBass_StingRay.wav", sl, sr)

    # Stem 3: Staccato Horns Fanfare (Trumpets & Tenor Sax Riff)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        horn_pos = t % (b_dur_104/2)
        horn_note = [392.00, 466.16, 587.33, 783.99][int(t / (b_dur_104/2)) % 4]
        horn = (math.sin(2*math.pi*horn_note*t) + 0.6*math.sin(2*math.pi*horn_note*2*t)) * math.exp(-horn_pos * 25.0) * 0.45
        sl[i] = horn * 0.9
        sr[i] = horn * 0.95
    write_wav(audio_dir / "11_ArmaniWhite_Stem_StaccatoHornsFanfare.wav", sl, sr)

    # Stem 4: Catchy Whistle Lead
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        w_note = [783.99, 880.00, 987.77, 1174.66][int(t / (b_dur_104/2)) % 4]
        whistle = math.sin(2*math.pi*w_note*t) * 0.35 * (0.8 + 0.2*math.sin(2*math.pi*6.0*t))  # Vibrato
        sl[i] = whistle * 0.8
        sr[i] = whistle * 0.9
    write_wav(audio_dir / "11_ArmaniWhite_Stem_CatchyWhistleLead.wav", sl, sr)

    # -------------------------------------------------------------
    # TRACK 12: OUTRO: JAMAICA (76 BPM, G Major)
    # -------------------------------------------------------------
    # Stem 1: One-Drop Drums (Kick + Cross-Stick Snare on Beat 3)
    sl, sr = [0.0]*n, [0.0]*n
    b_dur_76 = 60.0 / 76.0
    bar_dur_76 = b_dur_76 * 4.0
    for i in range(n):
        t = i / SAMPLE_RATE
        bar_pos = t % bar_dur_76
        # Beat 3 occurs at t = 2 * b_dur_76
        beat3_time = 2.0 * b_dur_76
        is_beat3 = 0.0 <= (bar_pos - beat3_time) < 0.35
        kick_snare = 0.0
        if is_beat3:
            dt = bar_pos - beat3_time
            k_hit = math.sin(2*math.pi*50.0*dt) * math.exp(-dt * 15.0) * 0.8
            stick_hit = (random.random()*2-1) * math.exp(-dt * 30.0) * 0.5
            kick_snare = k_hit + stick_hit
        # Shakers / Hats on upbeats
        hat_pos = (t % b_dur_76)
        hat = (random.random()*2-1) * math.exp(-(hat_pos - b_dur_76/2)*20.0)*0.2 if hat_pos >= b_dur_76/2 else 0.0
        sl[i] = kick_snare + hat
        sr[i] = kick_snare + hat
    write_wav(audio_dir / "12_Jamaica_Stem_OneDropKickSnare_Beat3.wav", sl, sr)

    # Stem 2: Fender P-Bass Flatwounds (Deep Warm Roots Tone)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        # Deep round G1 fundamental (49 Hz)
        bass = math.sin(2*math.pi*49.0*t) * 0.7 * (1.0 + 0.2*math.sin(2*math.pi*2.0*t))
        sl[i] = bass
        sr[i] = bass
    write_wav(audio_dir / "12_Jamaica_Stem_FenderPBass_Flatwounds.wav", sl, sr)

    # Stem 3: Hammond B3 Organ Bubble Chops (Leslie Speaker)
    sl, sr = [0.0]*n, [0.0]*n
    bubble_rate = b_dur_76 / 4.0
    for i in range(n):
        t = i / SAMPLE_RATE
        pos = t % bubble_rate
        organ = (math.sin(2*math.pi*392.00*t) + 0.7*math.sin(2*math.pi*493.88*t) + 0.5*math.sin(2*math.pi*587.33*t)) * math.exp(-pos * 20.0) * 0.35
        # Leslie rotary panning modulation (4 Hz)
        sl[i] = organ * (0.5 + 0.5*math.sin(2*math.pi*4.0*t))
        sr[i] = organ * (0.5 + 0.5*math.cos(2*math.pi*4.0*t))
    write_wav(audio_dir / "12_Jamaica_Stem_HammondB3Organ_Bubble.wav", sl, sr)

    # Stem 4: Stratocaster Chop Skank & Steelpan Accents
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        upbeat_pos = (t % b_dur_76) - (b_dur_76 / 2.0)
        skank = 0.0
        if 0 <= upbeat_pos < 0.12:
            skank = (math.sin(2*math.pi*587.33*t) + math.sin(2*math.pi*783.99*t)) * math.exp(-upbeat_pos * 40.0) * 0.4
        # Steelpan bell ring
        steelpan = math.sin(2*math.pi*987.77*t) * math.exp(-(t % (b_dur_76*2))*8.0) * 0.2
        sl[i] = skank * 0.4 + steelpan * 0.8
        sr[i] = skank * 0.9 + steelpan * 0.3
    write_wav(audio_dir / "12_Jamaica_Stem_StratSkankGuitar_Steelpan.wav", sl, sr)

    print(f"All 8 Act IV audio stems successfully rendered in {audio_dir}!")

if __name__ == "__main__":
    render_act_4()
