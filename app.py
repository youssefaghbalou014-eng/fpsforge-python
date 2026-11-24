import streamlit as st
import pandas as pd

# ==========================================
# 1. PAGE CONFIG & CUSTOM DARK GAMING THEME
# ==========================================
st.set_page_config(
    page_title="FPSForge | PC Game Benchmark & Specs Checker",
    page_icon="🎮",
    layout="wide",
)

st.markdown(
    """
    <style>
    .metric-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }
    .metric-value {
        font-size: 28px;
        font-weight: 800;
        color: #58a6ff;
    }
    .metric-label {
        font-size: 13px;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# 2. HARDWARE & GAME DATABASES
# ==========================================
# Score = relative gaming performance index
CPUS = {
    "Intel Core i3-10100F (4C/8T)": {"score": 9500, "tier": "Entry"},
    "Intel Core i5-8400 (6C/6T)": {"score": 9200, "tier": "Entry"},
    "Intel Core i7-7700HQ (4C/8T Laptop)": {"score": 7600, "tier": "Legacy Laptop"},
    "Intel Core i5-10400F (6C/12T)": {"score": 12500, "tier": "Budget"},
    "Intel Core i5-12400F (6C/12T)": {"score": 19500, "tier": "Mid-Range"},
    "Intel Core i5-13600K (14C/20T)": {"score": 28500, "tier": "High-End"},
    "Intel Core i7-14700K (20C/28T)": {"score": 34000, "tier": "Enthusiast"},
    "AMD Ryzen 5 3600 (6C/12T)": {"score": 13200, "tier": "Budget"},
    "AMD Ryzen 5 5600X (6C/12T)": {"score": 18500, "tier": "Mid-Range"},
    "AMD Ryzen 7 5800X3D (8C/16T)": {"score": 27000, "tier": "High-End"},
    "AMD Ryzen 7 7800X3D (8C/16T)": {"score": 35500, "tier": "Enthusiast"},
}

GPUS = {
    "NVIDIA GTX 1050 (4GB Laptop/Desktop)": {"score": 3600, "vram": 4},
    "NVIDIA GTX 1050 Ti (4GB)": {"score": 4400, "vram": 4},
    "NVIDIA GTX 1060 (6GB)": {"score": 6800, "vram": 6},
    "NVIDIA GTX 1650 (4GB)": {"score": 5600, "vram": 4},
    "NVIDIA GTX 1660 Super (6GB)": {"score": 8900, "vram": 6},
    "NVIDIA RTX 2060 (6GB)": {"score": 10800, "vram": 6},
    "NVIDIA RTX 3050 (8GB)": {"score": 9600, "vram": 8},
    "NVIDIA RTX 3060 (12GB)": {"score": 14000, "vram": 12},
    "NVIDIA RTX 3070 (8GB)": {"score": 19500, "vram": 8},
    "NVIDIA RTX 4060 (8GB)": {"score": 16200, "vram": 8},
    "NVIDIA RTX 4070 Super (12GB)": {"score": 25500, "vram": 12},
    "NVIDIA RTX 4080 Super (16GB)": {"score": 33000, "vram": 16},
    "NVIDIA RTX 4090 (24GB)": {"score": 42000, "vram": 24},
    "AMD Radeon RX 580 (8GB)": {"score": 6500, "vram": 8},
    "AMD Radeon RX 6600 (8GB)": {"score": 13200, "vram": 8},
    "AMD Radeon RX 6700 XT (12GB)": {"score": 18200, "vram": 12},
    "AMD Radeon RX 7800 XT (16GB)": {"score": 23800, "vram": 16},
}

# Baseline FPS is calibrated for an RTX 3060 (score 14000) + i5-12400F at 1080p High Native
GAMES = {
    "Cyberpunk 2077": {
        "genre": "Action RPG / Open World",
        "release": 2020,
        "storage_gb": 70,
        "ssd_required": True,
        "min_cpu": "Intel Core i5-8400 (6C/6T)",
        "min_gpu": "NVIDIA GTX 1060 (6GB)",
        "min_ram": 12,
        "min_vram": 6,
        "rec_cpu": "Intel Core i5-12400F (6C/12T)",
        "rec_gpu": "NVIDIA RTX 3060 (12GB)",
        "rec_ram": 16,
        "rec_vram": 8,
        "base_fps": 64,
        "cpu_weight": 0.30,
    },
    "Black Myth: Wukong": {
        "genre": "Action RPG",
        "release": 2024,
        "storage_gb": 130,
        "ssd_required": True,
        "min_cpu": "Intel Core i5-8400 (6C/6T)",
        "min_gpu": "NVIDIA GTX 1060 (6GB)",
        "min_ram": 16,
        "min_vram": 6,
        "rec_cpu": "Intel Core i5-12400F (6C/12T)",
        "rec_gpu": "NVIDIA RTX 3060 (12GB)",
        "rec_ram": 16,
        "rec_vram": 8,
        "base_fps": 55,
        "cpu_weight": 0.20,
    },
    "Red Dead Redemption 2": {
        "genre": "Open World Action-Adventure",
        "release": 2019,
        "storage_gb": 150,
        "ssd_required": False,
        "min_cpu": "Intel Core i7-7700HQ (4C/8T Laptop)",
        "min_gpu": "NVIDIA GTX 1050 (4GB Laptop/Desktop)",
        "min_ram": 8,
        "min_vram": 2,
        "rec_cpu": "Intel Core i5-10400F (6C/12T)",
        "rec_gpu": "NVIDIA GTX 1060 (6GB)",
        "rec_ram": 12,
        "rec_vram": 6,
        "base_fps": 82,
        "cpu_weight": 0.25,
    },
    "God of War Ragnarök": {
        "genre": "Action-Adventure",
        "release": 2024,
        "storage_gb": 190,
        "ssd_required": True,
        "min_cpu": "Intel Core i5-8400 (6C/6T)",
        "min_gpu": "NVIDIA GTX 1060 (6GB)",
        "min_ram": 8,
        "min_vram": 6,
        "rec_cpu": "Intel Core i5-12400F (6C/12T)",
        "rec_gpu": "NVIDIA RTX 3060 (12GB)",
        "rec_ram": 16,
        "rec_vram": 8,
        "base_fps": 78,
        "cpu_weight": 0.22,
    },
    "Elden Ring": {
        "genre": "Soulslike Action RPG",
        "release": 2022,
        "storage_gb": 60,
        "ssd_required": False,
        "min_cpu": "Intel Core i5-8400 (6C/6T)",
        "min_gpu": "NVIDIA GTX 1060 (6GB)",
        "min_ram": 12,
        "min_vram": 3,
        "rec_cpu": "Intel Core i5-10400F (6C/12T)",
        "rec_gpu": "NVIDIA RTX 3060 (12GB)",
        "rec_ram": 16,
        "rec_vram": 6,
        "base_fps": 60,  # Engine-capped at 60 FPS natively
        "fps_cap": 60,
        "cpu_weight": 0.30,
    },
    "The Witcher 3: Wild Hunt (Next-Gen)": {
        "genre": "Open World RPG",
        "release": 2015,
        "storage_gb": 50,
        "ssd_required": False,
        "min_cpu": "Intel Core i7-7700HQ (4C/8T Laptop)",
        "min_gpu": "NVIDIA GTX 1050 (4GB Laptop/Desktop)",
        "min_ram": 8,
        "min_vram": 4,
        "rec_cpu": "Intel Core i5-10400F (6C/12T)",
        "rec_gpu": "NVIDIA RTX 3060 (12GB)",
        "rec_ram": 16,
        "rec_vram": 8,
        "base_fps": 85,
        "cpu_weight": 0.25,
    },
    "Marvel's Spider-Man Remastered": {
        "genre": "Open World Action",
        "release": 2022,
        "storage_gb": 75,
        "ssd_required": True,
        "min_cpu": "Intel Core i7-7700HQ (4C/8T Laptop)",
        "min_gpu": "NVIDIA GTX 1050 (4GB Laptop/Desktop)",
        "min_ram": 8,
        "min_vram": 4,
        "rec_cpu": "Intel Core i5-10400F (6C/12T)",
        "rec_gpu": "NVIDIA RTX 3060 (12GB)",
        "rec_ram": 16,
        "rec_vram": 6,
        "base_fps": 92,
        "cpu_weight": 0.32,
    },
    "Counter-Strike 2": {
        "genre": "Competitive Tactical FPS",
        "release": 2023,
        "storage_gb": 85,
        "ssd_required": True,
        "min_cpu": "Intel Core i7-7700HQ (4C/8T Laptop)",
        "min_gpu": "NVIDIA GTX 1050 (4GB Laptop/Desktop)",
        "min_ram": 8,
        "min_vram": 2,
        "rec_cpu": "Intel Core i5-12400F (6C/12T)",
        "rec_gpu": "NVIDIA RTX 3060 (12GB)",
        "rec_ram": 16,
        "rec_vram": 4,
        "base_fps": 215,
        "cpu_weight": 0.45,
    },
    "Valorant": {
        "genre": "Competitive Tactical FPS",
        "release": 2020,
        "storage_gb": 45,
        "ssd_required": False,
        "min_cpu": "Intel Core i7-7700HQ (4C/8T Laptop)",
        "min_gpu": "NVIDIA GTX 1050 (4GB Laptop/Desktop)",
        "min_ram": 4,
        "min_vram": 1,
        "rec_cpu": "Intel Core i5-10400F (6C/12T)",
        "rec_gpu": "NVIDIA GTX 1650 (4GB)",
        "rec_ram": 8,
        "rec_vram": 4,
        "base_fps": 320,
        "cpu_weight": 0.55,
    },
    "Grand Theft Auto V": {
        "genre": "Open World Action",
        "release": 2015,
        "storage_gb": 110,
        "ssd_required": False,
        "min_cpu": "Intel Core i7-7700HQ (4C/8T Laptop)",
        "min_gpu": "NVIDIA GTX 1050 (4GB Laptop/Desktop)",
        "min_ram": 8,
        "min_vram": 2,
        "rec_cpu": "Intel Core i5-8400 (6C/6T)",
        "rec_gpu": "NVIDIA GTX 1060 (6GB)",
        "rec_ram": 16,
        "rec_vram": 4,
        "base_fps": 135,
        "cpu_weight": 0.30,
    },
}

RES_MULTIPLIERS = {
    "720p (1280×720)": 1.32,
    "1080p (1920×1080)": 1.00,
    "1440p (2560×1440)": 0.72,
    "4K (3840×2160)": 0.44,
}

PRESET_MULTIPLIERS = {
    "Low": 1.38,
    "Medium": 1.16,
    "High": 1.00,
    "Ultra": 0.78,
}

UPSCALING_MULTIPLIERS = {
    "Native (Off)": 1.00,
    "DLSS / FSR Quality": 1.24,
    "DLSS / FSR Balanced": 1.38,
    "DLSS / FSR Performance": 1.55,
}


# ==========================================
# 3. BENCHMARK & FPS ENGINE
# ==========================================
def calculate_fps(cpu_name, gpu_name, ram_gb, game_name, resolution, preset, upscaling):
    cpu = CPUS[cpu_name]
    gpu = GPUS[gpu_name]
    game = GAMES[game_name]

    # Reference system: RTX 3060 (14000) + i5-12400F (19500)
    gpu_ratio = gpu["score"] / 14000.0
    cpu_ratio = cpu["score"] / 19500.0

    # Weighted blend depending on whether the game is CPU-bound or GPU-bound
    w_cpu = game["cpu_weight"]
    w_gpu = 1.0 - w_cpu
    effective_ratio = (gpu_ratio * w_gpu) + (cpu_ratio * w_cpu)

    # Apply resolution, preset, and upscaling modifiers
    res_mult = RES_MULTIPLIERS[resolution]
    preset_mult = PRESET_MULTIPLIERS[preset]
    upscale_mult = UPSCALING_MULTIPLIERS[upscaling]

    # At higher resolutions (1440p/4K), GPU matters more; at 720p/1080p, CPU bottleneck caps ceiling
    raw_fps = game["base_fps"] * effective_ratio * res_mult * preset_mult * upscale_mult

    # CPU ceiling cap (prevents a weak CPU from achieving 300 FPS even with an RTX 4090)
    cpu_ceiling = (cpu["score"] / 19500.0) * game["base_fps"] * 1.45
    raw_fps = min(raw_fps, cpu_ceiling)

    # Penalty if VRAM or RAM is severely below minimum
    if gpu["vram"] < game["min_vram"]:
        vram_deficit = game["min_vram"] - gpu["vram"]
        raw_fps *= max(0.55, 1.0 - (0.15 * vram_deficit))
    if ram_gb < game["min_ram"]:
        raw_fps *= 0.75

    # Engine FPS cap (e.g., Elden Ring 60 FPS cap)
    if "fps_cap" in game:
        raw_fps = min(raw_fps, game["fps_cap"])

    avg_fps = max(12, int(round(raw_fps)))
    one_percent_low = max(8, int(round(avg_fps * (0.68 if ram_gb < game["rec_ram"] else 0.76))))
    return avg_fps, one_percent_low


def find_optimal_settings(cpu_name, gpu_name, ram_gb, game_name):
    """Finds the best resolution & preset combination targeting >= 60 FPS (or >= 30 FPS fallback)."""
    preferred_combos = [
        ("1440p (2560×1440)", "Ultra", "Native (Off)"),
        ("1440p (2560×1440)", "High", "Native (Off)"),
        ("1440p (2560×1440)", "High", "DLSS / FSR Quality"),
        ("1080p (1920×1080)", "Ultra", "Native (Off)"),
        ("1080p (1920×1080)", "High", "Native (Off)"),
        ("1080p (1920×1080)", "High", "DLSS / FSR Quality"),
        ("1080p (1920×1080)", "Medium", "Native (Off)"),
        ("1080p (1920×1080)", "Medium", "DLSS / FSR Quality"),
        ("1080p (1920×1080)", "Low", "DLSS / FSR Quality"),
        ("720p (1280×720)", "Medium", "Native (Off)"),
        ("720p (1280×720)", "Low", "DLSS / FSR Performance"),
    ]

    # First pass: look for >= 60 FPS
    for res, preset, up in preferred_combos:
        fps, _ = calculate_fps(cpu_name, gpu_name, ram_gb, game_name, res, preset, up)
        if fps >= 60:
            return res, preset, up, fps

    # Second pass: look for playable >= 30 FPS
    for res, preset, up in preferred_combos:
        fps, _ = calculate_fps(cpu_name, gpu_name, ram_gb, game_name, res, preset, up)
        if fps >= 30:
            return res, preset, up, fps

    # Fallback: lowest possible settings
    res, preset, up = "720p (1280×720)", "Low", "DLSS / FSR Performance"
    fps, _ = calculate_fps(cpu_name, gpu_name, ram_gb, game_name, res, preset, up)
    return res, preset, up, fps


# ==========================================
# 4. SIDEBAR: PC HARDWARE & GAME SELECTOR
# ==========================================
st.title("🎮 FPSForge — PC Game Compatibility & FPS Calculator")
st.caption("Select your PC specs and a game to check minimum/recommended requirements, bottlenecks, and estimated FPS.")

with st.sidebar:
    st.header("🖥️ Your PC Specifications")

    # Quick Rig Presets
    rig_preset = st.selectbox(
        "Quick Load Sample Rig (Optional)",
        [
            "Custom Selection",
            "Gaming Laptop (i7-7700HQ + GTX 1050 4GB + 16GB)",
            "Mid-Range PC (i5-12400F + RTX 3060 + 16GB)",
            "High-End PC (Ryzen 7 7800X3D + RTX 4070 Super + 32GB)",
        ],
    )

    default_cpu = "Intel Core i5-12400F (6C/12T)"
    default_gpu = "NVIDIA RTX 3060 (12GB)"
    default_ram = 16

    if "Laptop" in rig_preset:
        default_cpu = "Intel Core i7-7700HQ (4C/8T Laptop)"
        default_gpu = "NVIDIA GTX 1050 (4GB Laptop/Desktop)"
        default_ram = 16
    elif "High-End" in rig_preset:
        default_cpu = "AMD Ryzen 7 7800X3D (8C/16T)"
        default_gpu = "NVIDIA RTX 4070 Super (12GB)"
        default_ram = 32

    cpu_list = list(CPUS.keys())
    gpu_list = list(GPUS.keys())

    selected_cpu = st.selectbox("Processor (CPU)", cpu_list, index=cpu_list.index(default_cpu))
    selected_gpu = st.selectbox("Graphics Card (GPU)", gpu_list, index=gpu_list.index(default_gpu))
    selected_ram = st.select_slider("System Memory (RAM)", options=[4, 8, 12, 16, 32, 64], value=default_ram)
    selected_storage = st.radio("Storage Drive Type", ["NVMe / SATA SSD", "HDD (Hard Drive)"], horizontal=True)

    st.divider()
    st.header("🎯 Target Game & Display")
    selected_game = st.selectbox("Choose Game", list(GAMES.keys()))
    selected_res = st.selectbox("Target Resolution", list(RES_MULTIPLIERS.keys()), index=1)
    selected_preset = st.select_slider("Graphics Quality Preset", options=["Low", "Medium", "High", "Ultra"], value="High")
    selected_upscaling = st.selectbox("Upscaling (DLSS / FSR / XeSS)", list(UPSCALING_MULTIPLIERS.keys()))


# ==========================================
# 5. COMPATIBILITY & BOTTLENECK ANALYSIS
# ==========================================
game_data = GAMES[selected_game]
user_cpu_score = CPUS[selected_cpu]["score"]
user_gpu_score = GPUS[selected_gpu]["score"]
user_vram = GPUS[selected_gpu]["vram"]

min_cpu_score = CPUS[game_data["min_cpu"]]["score"]
rec_cpu_score = CPUS[game_data["rec_cpu"]]["score"]
min_gpu_score = GPUS[game_data["min_gpu"]]["score"]
rec_gpu_score = GPUS[game_data["rec_gpu"]]["score"]

meets_min = (
    user_cpu_score >= min_cpu_score
    and user_gpu_score >= min_gpu_score
    and selected_ram >= game_data["min_ram"]
)
meets_rec = (
    user_cpu_score >= rec_cpu_score
    and user_gpu_score >= rec_gpu_score
    and selected_ram >= game_data["rec_ram"]
)

# Verdict Banner
if meets_rec:
    st.success(
        f"✅ **EXCELLENT MATCH — Recommended Specs Met!** Your rig can run **{selected_game}** smoothly at High/Ultra settings."
    )
elif meets_min:
    st.warning(
        f"⚠️ **PLAYABLE — Minimum Specs Met.** Your PC can run **{selected_game}**, though lowering graphics settings is recommended for stable FPS."
    )
else:
    st.error(
        f"❌ **BELOW MINIMUM SPECS.** One or more components fall short of **{selected_game}**'s official minimum requirements."
    )

# Warnings & Bottlenecks
warnings = []
if user_gpu_score < min_gpu_score:
    warnings.append(f"**GPU Bottleneck:** Your `{selected_gpu}` is weaker than the minimum `{game_data['min_gpu']}`.")
if user_cpu_score < min_cpu_score:
    warnings.append(f"**CPU Bottleneck:** Your `{selected_cpu}` is below the minimum `{game_data['min_cpu']}`.")
if user_vram < game_data["min_vram"]:
    warnings.append(f"**VRAM Limit:** Your GPU has **{user_vram}GB VRAM**, below the **{game_data['min_vram']}GB** minimum (expect texture stuttering on High/Ultra).")
if selected_ram < game_data["min_ram"]:
    warnings.append(f"**RAM Limit:** You have **{selected_ram}GB RAM**, below the **{game_data['min_ram']}GB** minimum.")
if game_data["ssd_required"] and "HDD" in selected_storage:
    warnings.append(f"**Storage Warning:** **{selected_game}** requires an **SSD**; playing on an HDD will cause long loading times and texture pop-in.")

if warnings:
    with st.expander("🔍 Bottleneck & Hardware Alerts", expanded=True):
        for w in warnings:
            st.markdown(f"- {w}")

# ==========================================
# 6. KEY METRICS & OPTIMAL SETTINGS CARD
# ==========================================
avg_fps, low_fps = calculate_fps(
    selected_cpu, selected_gpu, selected_ram, selected_game, selected_res, selected_preset, selected_upscaling
)
opt_res, opt_preset, opt_upscale, opt_fps = find_optimal_settings(
    selected_cpu, selected_gpu, selected_ram, selected_game
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">Estimated Avg FPS</div><div class="metric-value">{avg_fps} FPS</div></div>',
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">1% Low FPS</div><div class="metric-value">{low_fps} FPS</div></div>',
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">Best Sweet-Spot Settings</div><div class="metric-value" style="font-size:18px; padding-top:8px;">{opt_res.split()[0]} • {opt_preset}</div></div>',
        unsafe_allow_html=True,
    )
with col4:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">Sweet-Spot FPS</div><div class="metric-value">{opt_fps} FPS</div></div>',
        unsafe_allow_html=True,
    )

st.info(
    f"💡 **Recommended Optimal Setup for Your PC:** Run **{selected_game}** at **{opt_res}**, **{opt_preset} Preset**, with **{opt_upscale}** for **~{opt_fps} FPS**."
)

# ==========================================
# 7. FULL FPS MATRIX & SPECS COMPARISON
# ==========================================
tab1, tab2 = st.tabs(["📊 FPS Across All Resolutions & Presets", "📋 Official Minimum vs. Recommended Specs"])

with tab1:
    st.subheader(f"Estimated Average FPS Matrix ({selected_upscaling})")
    matrix_rows = []
    for res_label in RES_MULTIPLIERS.keys():
        row = {"Resolution": res_label}
        for preset_label in ["Low", "Medium", "High", "Ultra"]:
            f_avg, f_low = calculate_fps(
                selected_cpu, selected_gpu, selected_ram, selected_game, res_label, preset_label, selected_upscaling
            )
            row[preset_label] = f"{f_avg} FPS (1% Low: {f_low})"
        matrix_rows.append(row)

    df_fps = pd.DataFrame(matrix_rows)
    st.dataframe(df_fps, use_container_width=True, hide_index=True)

    # Bar chart for the currently selected resolution
    chart_data = pd.DataFrame(
        {
            "Graphics Preset": ["Low", "Medium", "High", "Ultra"],
            "Average FPS": [
                calculate_fps(selected_cpu, selected_gpu, selected_ram, selected_game, selected_res, p, selected_upscaling)[0]
                for p in ["Low", "Medium", "High", "Ultra"]
            ],
        }
    )
    st.bar_chart(chart_data.set_index("Graphics Preset"), height=260)

with tab2:
    st.subheader(f"{selected_game} — System Requirements Breakdown")
    specs_df = pd.DataFrame(
        [
            {
                "Component": "Processor (CPU)",
                "Your PC": selected_cpu,
                "Minimum Required": game_data["min_cpu"],
                "Recommended": game_data["rec_cpu"],
                "Status": "✅ Recommended" if user_cpu_score >= rec_cpu_score else ("⚠️ Minimum" if user_cpu_score >= min_cpu_score else "❌ Below Min"),
            },
            {
                "Component": "Graphics Card (GPU)",
                "Your PC": selected_gpu,
                "Minimum Required": game_data["min_gpu"],
                "Recommended": game_data["rec_gpu"],
                "Status": "✅ Recommended" if user_gpu_score >= rec_gpu_score else ("⚠️ Minimum" if user_gpu_score >= min_gpu_score else "❌ Below Min"),
            },
            {
                "Component": "VRAM",
                "Your PC": f"{user_vram} GB",
                "Minimum Required": f"{game_data['min_vram']} GB",
                "Recommended": f"{game_data['rec_vram']} GB",
                "Status": "✅ Recommended" if user_vram >= game_data["rec_vram"] else ("⚠️ Minimum" if user_vram >= game_data["min_vram"] else "❌ Below Min"),
            },
            {
                "Component": "System RAM",
                "Your PC": f"{selected_ram} GB",
                "Minimum Required": f"{game_data['min_ram']} GB",
                "Recommended": f"{game_data['rec_ram']} GB",
                "Status": "✅ Recommended" if selected_ram >= game_data["rec_ram"] else ("⚠️ Minimum" if selected_ram >= game_data["min_ram"] else "❌ Below Min"),
            },
            {
                "Component": "Storage Space",
                "Your PC": selected_storage,
                "Minimum Required": f"{game_data['storage_gb']} GB ({'SSD Req.' if game_data['ssd_required'] else 'HDD/SSD'})",
                "Recommended": f"{game_data['storage_gb']} GB NVMe SSD",
                "Status": "❌ SSD Needed" if (game_data["ssd_required"] and "HDD" in selected_storage) else "✅ Ready",
            },
        ]
    )
    st.dataframe(specs_df, use_container_width=True, hide_index=True)