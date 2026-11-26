import json
from app import CPUS, GPUS

with open("games.json", "r", encoding="utf-8") as f:
    games = json.load(f)

required_keys = {
    "genre", "release", "storage_gb", "ssd_required",
    "min_cpu", "min_gpu", "min_ram", "min_vram",
    "rec_cpu", "rec_gpu", "rec_ram", "rec_vram",
    "base_fps", "cpu_weight"
}

errors = 0
for title, info in games.items():
    missing = required_keys - set(info.keys())
    if missing:
        print(f"[MISSING KEYS] {title}: {missing}")
        errors += 1
    for cpu_field in ("min_cpu", "rec_cpu"):
        if info.get(cpu_field) not in CPUS:
            print(f"[UNKNOWN CPU] {title} -> {cpu_field}: '{info.get(cpu_field)}'")
            errors += 1
    for gpu_field in ("min_gpu", "rec_gpu"):
        if info.get(gpu_field) not in GPUS:
            print(f"[UNKNOWN GPU] {title} -> {gpu_field}: '{info.get(gpu_field)}'")
            errors += 1

print(f"Checked {len(games)} games. Found {errors} issue(s).")