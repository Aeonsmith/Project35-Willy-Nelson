#!/usr/bin/env python3
"""
synthesize_foley_assets.py
Procedurally synthesizes 24-bit / 48 kHz WAV reference audio assets for Project 35: Willy Nelson.
"""

import math
import random
import struct
import wave
from pathlib import Path

SAMPLE_RATE = 48000

def write_wav_24bit(filepath: Path, samples_l: list, samples_r: list):
    """Writes stereo 24-bit PCM WAV file."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    n_frames = len(samples_l)
    
    # Normalize to -6 dBFS max peak (~0.5 amplitude)
    max_val = max(max(abs(s) for s in samples_l), max(abs(s) for s in samples_r), 1e-6)
    target_peak = 0.50
    gain = target_peak / max_val if max_val > 0 else 1.0
    
    with wave.open(str(filepath), 'wb') as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(3)  # 24-bit
        wav_file.setframerate(SAMPLE_RATE)
        
        raw_bytes = bytearray()
        for i in range(n_frames):
            sl = int(max(min(samples_l[i] * gain, 1.0), -1.0) * 8388607.0)
            sr = int(max(min(samples_r[i] * gain, 1.0), -1.0) * 8388607.0)
            
            # Pack 24-bit little endian
            raw_bytes.extend(sl.to_bytes(3, byteorder='little', signed=True))
            raw_bytes.extend(sr.to_bytes(3, byteorder='little', signed=True))
            
        wav_file.writeframes(raw_bytes)

def generate_all():
    base_dir = Path(__file__).resolve().parent
    assets_dir = base_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    
    print("Synthesizing 24-bit / 48 kHz reference foley assets...")

    # 1. PS5_Startup_SubDrop (3.0 seconds)
    dur = 3.0
    n = int(SAMPLE_RATE * dur)
    sl, sr = [0.0]*n, [0.0]*n
    # 3-tone chime (523Hz C5, 659Hz E5, 784Hz G5)
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 2.0)
        chime = (0.3*math.sin(2*math.pi*523.25*t) + 0.3*math.sin(2*math.pi*659.25*t) + 0.4*math.sin(2*math.pi*783.99*t)) * env
        # Sub-drop at 1.0s
        sub = 0.0
        if t >= 0.8:
            t_sub = t - 0.8
            freq = max(35.0, 110.0 - 45.0 * t_sub)
            sub_env = math.exp(-t_sub * 1.5)
            sub = 0.8 * math.sin(2 * math.pi * freq * t_sub) * sub_env
        sl[i] = chime * 0.7 + sub
        sr[i] = chime * 0.8 + sub
    write_wav_24bit(assets_dir / "PS5_Startup_SubDrop.wav", sl, sr)

    # 2. Car_Trunk_Slam_Footsteps (2.5 seconds)
    dur = 2.5
    n = int(SAMPLE_RATE * dur)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        # Footsteps (gravel noise pulses at t=0.2, 0.6, 1.0)
        foot = 0.0
        for f_time in [0.2, 0.6, 1.0]:
            if 0 <= t - f_time < 0.15:
                dt = t - f_time
                noise = (random.random() * 2.0 - 1.0) * math.exp(-dt * 30.0)
                foot += noise * 0.3
        # Heavy trunk latch slam at t=1.4
        slam = 0.0
        if t >= 1.4:
            dt = t - 1.4
            thud = math.sin(2*math.pi*55.0*dt) * math.exp(-dt * 15.0)
            metal = (random.random() * 2.0 - 1.0) * math.exp(-dt * 40.0)
            slam = (thud * 0.7 + metal * 0.3)
        sl[i] = foot * 0.8 + slam
        sr[i] = foot * 0.6 + slam
    write_wav_24bit(assets_dir / "Car_Trunk_Slam_Footsteps.wav", sl, sr)

    # 3. Methane_Gas_Valve_Hiss (3.0 seconds)
    dur = 3.0
    n = int(SAMPLE_RATE * dur)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        noise_l = (random.random() * 2.0 - 1.0)
        noise_r = (random.random() * 2.0 - 1.0)
        env = (1.0 - math.exp(-t * 5.0)) * math.exp(-t * 0.5)
        # Resonant metallic whistle / alarm pulse
        whistle = 0.2 * math.sin(2 * math.pi * (1800.0 + 300.0 * math.sin(2*math.pi*2.0*t)) * t)
        sl[i] = (noise_l * 0.5 + whistle) * env
        sr[i] = (noise_r * 0.5 + whistle) * env
    write_wav_24bit(assets_dir / "Methane_Gas_Valve_Hiss.wav", sl, sr)

    # 4. Subsonic_Implosion_Detonation (3.5 seconds)
    dur = 3.5
    n = int(SAMPLE_RATE * dur)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        if t < 1.0:
            # Vacuum suction (rising pitch)
            env = t / 1.0
            freq = 40.0 + 120.0 * (t ** 2)
            val = math.sin(2 * math.pi * freq * t) * env * 0.4
            sl[i] = val
            sr[i] = val
        else:
            # Detonation & sub-decay
            dt = t - 1.0
            env = math.exp(-dt * 1.8)
            sub = math.sin(2 * math.pi * 38.0 * dt) * env * 0.8
            crack = (random.random() * 2.0 - 1.0) * math.exp(-dt * 25.0) * 0.5
            sl[i] = sub + crack
            sr[i] = sub + crack
    write_wav_24bit(assets_dir / "Subsonic_Implosion_Detonation.wav", sl, sr)

    # 5. Subterranean_Rain_Decay (4.0 seconds)
    dur = 4.0
    n = int(SAMPLE_RATE * dur)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        rain_l = (random.random() * 2.0 - 1.0) * 0.3
        rain_r = (random.random() * 2.0 - 1.0) * 0.3
        # Distant low rumble
        rumble = 0.2 * math.sin(2 * math.pi * 42.0 * t) * (1.0 + 0.5 * math.sin(2 * math.pi * 0.3 * t))
        sl[i] = rain_l + rumble
        sr[i] = rain_r + rumble
    write_wav_24bit(assets_dir / "Subterranean_Rain_Decay.wav", sl, sr)

    # 6. Hardwood_Sneaker_Squeaks_Arena (3.0 seconds)
    dur = 3.0
    n = int(SAMPLE_RATE * dur)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        # Arena low crowd drone
        crowd_l = (random.random() * 2.0 - 1.0) * 0.15
        crowd_r = (random.random() * 2.0 - 1.0) * 0.15
        # Sneaker squeaks at t=0.5, 1.2, 1.8
        squeak = 0.0
        for sq_t in [0.5, 1.2, 1.8]:
            if 0 <= t - sq_t < 0.12:
                dt = t - sq_t
                freq = 2400.0 + 800.0 * math.sin(2*math.pi*40.0*dt)
                squeak += math.sin(2 * math.pi * freq * dt) * math.exp(-dt * 25.0) * 0.5
        sl[i] = crowd_l + squeak * 0.9
        sr[i] = crowd_r + squeak * 0.6
    write_wav_24bit(assets_dir / "Hardwood_Sneaker_Squeaks_Arena.wav", sl, sr)

    # 7. Referee_Whistle_Echo (2.5 seconds)
    dur = 2.5
    n = int(SAMPLE_RATE * dur)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        # Whistle blast at 0.0s (2800Hz + 3100Hz dual tone)
        whistle = 0.0
        if t < 0.4:
            whistle = (math.sin(2*math.pi*2800*t) + math.sin(2*math.pi*3120*t)) * 0.4
        # Ping-pong echo repeats at 0.7s (L), 1.2s (R), 1.7s (L)
        echo_l = 0.0
        echo_r = 0.0
        if 0.7 <= t < 1.0:
            dt = t - 0.7
            echo_l = (math.sin(2*math.pi*2800*dt) + math.sin(2*math.pi*3120*dt)) * 0.2 * math.exp(-dt*5)
        if 1.2 <= t < 1.5:
            dt = t - 1.2
            echo_r = (math.sin(2*math.pi*2800*dt) + math.sin(2*math.pi*3120*dt)) * 0.1 * math.exp(-dt*5)
        sl[i] = whistle + echo_l
        sr[i] = whistle * 0.5 + echo_r
    write_wav_24bit(assets_dir / "Referee_Whistle_Echo.wav", sl, sr)

    # 8. Golf_Club_Titanium_Crack (1.5 seconds)
    dur = 1.5
    n = int(SAMPLE_RATE * dur)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        if t < 0.08:
            # Impact transient
            crack = (random.random() * 2.0 - 1.0) * math.exp(-t * 80.0) * 0.9
            ping = math.sin(2 * math.pi * 4200.0 * t) * math.exp(-t * 50.0) * 0.4
            sl[i] = crack + ping
            sr[i] = crack + ping
        else:
            sl[i] = 0.0
            sr[i] = 0.0
    write_wav_24bit(assets_dir / "Golf_Club_Titanium_Crack.wav", sl, sr)

    # 9. Twin_Jet_Turbine_Sweep (3.5 seconds)
    dur = 3.5
    n = int(SAMPLE_RATE * dur)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        env = (t / 3.5) ** 1.5
        noise = (random.random() * 2.0 - 1.0) * 0.4
        whine = 0.3 * math.sin(2 * math.pi * (400.0 + 3500.0 * (t / 3.5)) * t)
        sl[i] = (noise + whine) * env
        sr[i] = (noise + whine) * env * (0.8 + 0.2 * math.sin(2*math.pi*1.5*t))
    write_wav_24bit(assets_dir / "Twin_Jet_Turbine_Sweep.wav", sl, sr)

    # 10. Tire_Squeal_Parallel_Parking (2.5 seconds)
    dur = 2.5
    n = int(SAMPLE_RATE * dur)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        if t < 1.8:
            env = math.sin(math.pi * (t / 1.8))
            freq = 1100.0 + 300.0 * math.sin(2 * math.pi * 15.0 * t)
            screech = math.sin(2 * math.pi * freq * t) * 0.4 + (random.random()*2-1)*0.2
            pan_l = math.cos(math.pi * 0.5 * (t / 1.8))
            pan_r = math.sin(math.pi * 0.5 * (t / 1.8))
            sl[i] = screech * env * pan_l
            sr[i] = screech * env * pan_r
    write_wav_24bit(assets_dir / "Tire_Squeal_Parallel_Parking.wav", sl, sr)

    # 11. Tape_Stop_Deceleration (2.5 seconds)
    dur = 2.5
    n = int(SAMPLE_RATE * dur)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        speed = max(0.0, 1.0 - (t / 2.5) ** 1.8)
        freq = 440.0 * speed
        tone = math.sin(2 * math.pi * freq * t) * 0.3 * speed
        friction = (random.random() * 2 - 1) * 0.15 * (1.0 - speed)
        sl[i] = tone + friction
        sr[i] = tone + friction
    write_wav_24bit(assets_dir / "Tape_Stop_Deceleration.wav", sl, sr)

    # 12. Caribbean_Ocean_Surf_Dub_Siren (4.5 seconds)
    dur = 4.5
    n = int(SAMPLE_RATE * dur)
    sl, sr = [0.0]*n, [0.0]*n
    for i in range(n):
        t = i / SAMPLE_RATE
        # Ocean surf swell (low-passed noise)
        wave_env = math.sin(math.pi * (t / 4.5)) ** 2
        surf_l = (random.random() * 2.0 - 1.0) * 0.3 * wave_env
        surf_r = (random.random() * 2.0 - 1.0) * 0.3 * wave_env
        # Dub siren sweep pulses
        siren = 0.0
        if 1.0 <= t < 3.5:
            dt = t - 1.0
            s_freq = 600.0 + 400.0 * math.sin(2 * math.pi * 3.5 * dt)
            siren = math.sin(2 * math.pi * s_freq * dt) * 0.25 * math.exp(-dt * 0.4)
        sl[i] = surf_l + siren
        sr[i] = surf_r + siren * 0.8
    write_wav_24bit(assets_dir / "Caribbean_Ocean_Surf_Dub_Siren.wav", sl, sr)

    print(f"All 12 foley & sample sound design assets created successfully in {assets_dir}!")

if __name__ == "__main__":
    generate_all()
