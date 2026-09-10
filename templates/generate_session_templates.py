#!/usr/bin/env python3
"""
generate_session_templates.py
Generates DAW project session template definitions and an index manifest for Project 35: Willy Nelson.
"""

import json
import os
from pathlib import Path

def generate():
    base_dir = Path(__file__).resolve().parent
    master_json_path = base_dir / "tempo_map_master.json"
    
    with open(master_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    output_dir = base_dir / "sessions"
    output_dir.mkdir(exist_ok=True)
    
    manifest_lines = [
        "# DAW SESSION TEMPLATES & MASTER TEMPO MAP",
        "",
        f"**Project:** {data['project_title']} ({data['subtitle']})",
        f"**Sample Rate:** {data['sample_rate_hz']} Hz | **Bit Depth:** {data['bit_depth']}-bit | **Target Pre-Mix Headroom:** {data['headroom_target_db']} dB",
        "",
        "---",
        ""
    ]
    
    for t in data["tracks"]:
        t_num = t["track_number"]
        t_title = t["title"]
        t_bpm = t["bpm"]
        t_key = t["key"]
        t_act = t["act"]
        
        # Build individual DAW template text file
        template_filename = f"Track_{t_num}_{t_title.replace(' ', '_').replace('(', '').replace(')', '').replace('{', '').replace('}', '').replace('<', '').replace('>', '').replace('$', 'S')}.txt"
        template_file_path = output_dir / template_filename
        
        with open(template_file_path, "w", encoding="utf-8") as tf:
            tf.write(f"PROJECT: {data['project_title']}\n")
            tf.write(f"TRACK {t_num}: {t_title}\n")
            tf.write(f"ACT: {t_act}\n")
            tf.write(f"BPM: {t_bpm} | KEY: {t_key} | TIME SIG: {t['time_signature']}\n")
            tf.write(f"SAMPLE RATE: {data['sample_rate_hz']} Hz | BIT DEPTH: {data['bit_depth']}-bit\n")
            tf.write(f"TARGET HEADROOM: {data['headroom_target_db']} dB True Peak\n")
            tf.write(f"TRANSITION OUT: {t['transition_out']}\n\n")
            tf.write("ARRANGEMENT MARKERS:\n")
            for m in t["arrangement_markers"]:
                tf.write(f"  - Bar {m['bar']:02d} [{m['time']}]: {m['name']}\n")
            tf.write("\nSTEM CHANNELS & BUS ROUTING:\n")
            for idx, ch in enumerate(t["stem_channels"], 1):
                tf.write(f"  Channel {idx:02d}: {ch} -> Master Bus\n")
                
        # Append to Master Manifest
        manifest_lines.append(f"## Track {t_num}: {t_title}")
        manifest_lines.append(f"* **Act:** {t_act}")
        manifest_lines.append(f"* **Tempo / Grid:** {t_bpm} BPM | **Key:** {t_key} | **Meter:** {t['time_signature']}")
        manifest_lines.append(f"* **Transition Hook:** {t['transition_out']}")
        manifest_lines.append("* **Arrangement Markers:**")
        for m in t["arrangement_markers"]:
            manifest_lines.append(f"  - Bar {m['bar']:02d} ({m['time']}): {m['name']}")
        manifest_lines.append("* **Stem Channel Stacking:**")
        for idx, ch in enumerate(t["stem_channels"], 1):
            manifest_lines.append(f"  - Ch {idx:02d}: `{ch}`")
        manifest_lines.append("")
        manifest_lines.append("---")
        manifest_lines.append("")

    manifest_path = base_dir / "TEMPLATES_INDEX.md"
    with open(manifest_path, "w", encoding="utf-8") as mf:
        mf.write("\n".join(manifest_lines))
        
    print(f"Successfully generated 12 DAW session templates in {output_dir}")
    print(f"Generated Master Templates Index in {manifest_path}")

if __name__ == "__main__":
    generate()
