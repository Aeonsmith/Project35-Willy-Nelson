#!/usr/bin/env python3
"""
generate_scratch_vocal_demos.py
Synthesizes 24-bit / 48 kHz guide cadence audio demo stems for Project 35: Willy Nelson.
"""

import math
import struct
import wave
from pathlib import Path

SAMPLE_RATE = 48000

TRACKS = [
    ("01_Resentful", 130, 3.0),
    ("02_Savage_Gasp", 128, 3.0),
    ("03_Chris_Brown_King", 135, 3.0),
    ("04_Clejan_11_Mirror", 132, 2.5),
    ("05_A_Rob_PS5", 90, 3.0),
    ("06_Token_Methane_Gas", 150, 2.5),
    ("07_Mac_Lethal_Heartbreak_Days", 86, 3.0),
    ("08_MJ", 124, 3.0),
    ("09_Messi", 140, 2.5),
    ("10_Dont_Play_Golf", 126, 3.0),
    ("11_Armani_White", 104, 2.5),
    ("12_Outro_Jamaica", 76, 3.5),
]

def synthesize_cadence_guide(filepath: Path, bpm: float, duration_sec: float):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    n_frames = int(SAMPLE_RATE * duration_sec)
    beat_interval = 60.0 / bpm
    
    samples_l = [0.0] * n_frames
    samples_r = [0.0] * n_frames
    
    # Generate cadence rhythmic speech pulses on subdivisions
    for i in range(n_frames):
        t = i / SAMPLE_RATE
        beat_phase = (t % beat_interval) / beat_interval
        
        # Quarter-note click
        click = 0.0
        if beat_phase < 0.05:
            dt = beat_phase * beat_interval
            click = math.sin(2 * math.pi * 1200.0 * dt) * math.exp(-dt * 80.0) * 0.4
            
        # Syllable rhythmic cadence formant pulse (220Hz / 440Hz / 880Hz)
        sixteenth_phase = ((t * 4) % beat_interval) / beat_interval
        vocal_pulse = 0.0
        if sixteenth_phase < 0.15:
            dt = sixteenth_phase * (beat_interval / 4)
            formant = (math.sin(2*math.pi*220*dt) + 0.5*math.sin(2*math.pi*440*dt) + 0.3*math.sin(2*math.pi*880*dt))
            vocal_pulse = formant * math.exp(-dt * 20.0) * 0.35
            
        samples_l[i] = click * 0.5 + vocal_pulse * 0.8
        samples_r[i] = click * 0.5 + vocal_pulse * 0.8
        
    # Write 24-bit WAV
    with wave.open(str(filepath), 'wb') as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(3)
        wav_file.setframerate(SAMPLE_RATE)
        
        raw_bytes = bytearray()
        for i in range(n_frames):
            sl = int(max(min(samples_l[i], 1.0), -1.0) * 8388607.0)
            sr = int(max(min(samples_r[i], 1.0), -1.0) * 8388607.0)
            raw_bytes.extend(sl.to_bytes(3, byteorder='little', signed=True))
            raw_bytes.extend(sr.to_bytes(3, byteorder='little', signed=True))
            
        wav_file.writeframes(raw_bytes)

def generate_all():
    base_dir = Path(__file__).resolve().parent
    demos_dir = base_dir / "scratch_demos"
    demos_dir.mkdir(parents=True, exist_ok=True)
    
    print("Generating 24-bit / 48 kHz scratch vocal cadence demo stems...")
    for name, bpm, dur in TRACKS:
        file_path = demos_dir / f"Demo_Cadence_{name}.wav"
        synthesize_cadence_guide(file_path, bpm, dur)
        print(f"  ✓ {file_path.name} ({bpm} BPM)")
        
    print(f"All 12 scratch vocal cadence demos generated in {demos_dir}!")

if __name__ == "__main__":
    generate_all()
