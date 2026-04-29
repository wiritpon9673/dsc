import streamlit as st
import math
 
# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Eccentric Footing | Terzaghi",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed",
)
 
# ─── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap');
 
*, *::before, *::after { box-sizing: border-box; }
 
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background: #f0f4f8 !important;
    font-family: 'IBM Plex Sans Thai', sans-serif !important;
}
[data-testid="stHeader"]  { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
 
/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #1a365d 0%, #2b6cb0 60%, #3182ce 100%);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    color: #fff;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: '';
    position: absolute;
    right: -40px; top: -40px;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: rgba(255,255,255,0.06);
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.18);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 20px;
    padding: 3px 12px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    margin-bottom: 0.8rem;
}
.hero h1 {
    font-size: 1.9rem;
    font-weight: 700;
    margin: 0 0 0.3rem;
    line-height: 1.2;
}
.hero p { margin: 0; font-size: 0.9rem; opacity: 0.8; font-weight: 300; }
 
/* ── Card Title ── */
.card-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #2b6cb0;
    border-left: 3px solid #3182ce;
    padding-left: 10px;
    margin-bottom: 1.2rem;
}
 
/* ── Inputs ── */
[data-testid="stNumberInput"] label,
[data-testid="stSelectbox"] label {
    font-family: 'IBM Plex Sans Thai', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    color: #2d3748 !important;
}
[data-testid="stNumberInput"] input {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.92rem !important;
    border-radius: 8px !important;
    border: 1.5px solid #cbd5e0 !important;
    background: #f7fafc !important;
    color: #1a202c !important;
}
[data-testid="stNumberInput"] input:focus {
    border-color: #3182ce !important;
    box-shadow: 0 0 0 3px rgba(49,130,206,0.15) !important;
    background: #fff !important;
}
[data-testid="stSelectbox"] > div > div {
    border-radius: 8px !important;
    border: 1.5px solid #cbd5e0 !important;
    background: #f7fafc !important;
    font-family: 'IBM Plex Sans Thai', sans-serif !important;
    font-size: 0.88rem !important;
}
 
/* ── Tabs ── */
[data-baseweb="tab-list"] {
    background: #edf2f7 !important;
    border-radius: 10px !important;
    padding: 3px !important;
    gap: 3px !important;
    border: none !important;
}
[data-baseweb="tab"] {
    border-radius: 8px !important;
    font-family: 'IBM Plex Sans Thai', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    color: #718096 !important;
    padding: 0.4rem 1rem !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    background: #ffffff !important;
    color: #2b6cb0 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.12) !important;
}
 
/* ── Buttons ── */
[data-testid="stButton"] > button {
    width: 100% !important;
    border-radius: 10px !important;
    font-family: 'IBM Plex Sans Thai', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.6rem 1rem !important;
    transition: all 0.2s !important;
    border: none !important;
    letter-spacing: 0.02em !important;
}
[data-testid="stButton"]:nth-of-type(1) > button {
    background: linear-gradient(135deg, #2b6cb0, #3182ce) !important;
    color: #ffffff !important;
    box-shadow: 0 4px 12px rgba(49,130,206,0.4) !important;
}
[data-testid="stButton"]:nth-of-type(1) > button:hover {
    box-shadow: 0 6px 20px rgba(49,130,206,0.5) !important;
    transform: translateY(-1px) !important;
}
[data-testid="stButton"]:nth-of-type(2) > button {
    background: #edf2f7 !important;
    color: #4a5568 !important;
}
[data-testid="stButton"]:nth-of-type(2) > button:hover {
    background: #e2e8f0 !important;
    color: #2d3748 !important;
}
 
/* ── Result boxes ── */
.res-primary {
    background: linear-gradient(135deg, #1a365d, #2b6cb0);
    border-radius: 14px;
    padding: 1.8rem 2rem;
    text-align: center;
    color: #fff;
    margin-bottom: 1rem;
    box-shadow: 0 4px 20px rgba(43,108,176,0.35);
}
.res-primary .res-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    opacity: 0.75;
    margin-bottom: 0.4rem;
}
.res-primary .res-num {
    font-size: 3.2rem;
    font-weight: 700;
    line-height: 1;
    letter-spacing: -0.02em;
}
.res-primary .res-unit {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
    opacity: 0.7;
    margin-top: 0.3rem;
}
.res-secondary {
    background: #f0fff4;
    border: 2px solid #9ae6b4;
    border-radius: 14px;
    padding: 1.4rem 2rem;
    text-align: center;
    margin-bottom: 1rem;
}
.res-secondary .res-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #276749;
    margin-bottom: 0.4rem;
}
.res-secondary .res-num {
    font-size: 2.6rem;
    font-weight: 700;
    color: #276749;
    line-height: 1;
}
.res-secondary .res-unit {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    color: #38a169;
    margin-top: 0.3rem;
}
 
/* ── Data grid ── */
.dgrid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.6rem;
}
.ditem {
    background: #f7fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 0.65rem 0.9rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.dname {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    color: #718096;
}
.dval {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    font-weight: 600;
    color: #1a202c;
}
 
/* ── Alerts ── */
.alert-warn {
    background: #fffbeb;
    border: 1.5px solid #f6ad55;
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    color: #744210;
    font-size: 0.84rem;
    line-height: 1.5;
    margin-top: 0.75rem;
}
.alert-ok {
    background: #f0fff4;
    border: 1.5px solid #9ae6b4;
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    color: #276749;
    font-size: 0.84rem;
    line-height: 1.5;
    margin-top: 0.75rem;
}
.alert-err {
    background: #fff5f5;
    border: 1.5px solid #fc8181;
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    color: #742a2a;
    font-size: 0.84rem;
    line-height: 1.5;
    margin-bottom: 0.6rem;
}
.placeholder {
    background: #fff;
    border: 2px dashed #cbd5e0;
    border-radius: 14px;
    padding: 3rem 2rem;
    text-align: center;
    color: #a0aec0;
}
.placeholder .ph-icon { font-size: 2.5rem; margin-bottom: 0.75rem; }
.placeholder p { margin: 0; font-size: 0.9rem; }
.hdiv {
    height: 1px;
    background: linear-gradient(90deg, transparent, #cbd5e0, transparent);
    margin: 1.2rem 0;
}
 
/* ── Formula ── */
.fbox {
    background: #1a202c;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
    color: #90cdf4;
    line-height: 2.2;
}
.ftitle {
    color: #63b3ed;
    font-weight: 600;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.2rem;
    border-bottom: 1px solid #2d3748;
    padding-bottom: 0.3rem;
}
.fline { color: #e2e8f0; }
.fsub  { color: #68d391; }
 
.footer {
    text-align: center;
    padding: 1.5rem 0 0.5rem;
    color: #a0aec0;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.1em;
}
</style>
""", unsafe_allow_html=True)
 
 
# ─── Calculation Functions ───────────────────────────────────────────────────────
 
def terzaghi_factors(phi_deg: float):
    """Terzaghi (1943) bearing capacity factors Nc, Nq, Nγ"""
    phi = math.radians(phi_deg)
    if phi_deg == 0.0:
        return 5.14, 1.0, 0.0
    Nq = math.exp(math.pi * math.tan(phi)) * (math.tan(math.radians(45 + phi_deg / 2)) ** 2)
    Nc = (Nq - 1.0) / math.tan(phi)
    Ng = (Nq - 1.0) * math.tan(1.4 * phi)
    return Nc, Nq, Ng
 
 
def shape_factors(shape: str, B_eff: float, L_eff: float, phi_deg: float):
    """Shape factors sc, sq, sγ"""
    phi = math.radians(phi_deg)
    if shape == "square":
        return 1.3, 1.0, 0.8
    if shape == "circular":
        return 1.3, 1.0, 0.6
    # Rectangular — ratio = B'/L'
    ratio = B_eff / L_eff
    sc = 1.0 + 0.2 * ratio
    sq = 1.0 + ratio * math.tan(phi) if phi_deg > 0 else 1.0
    sg = max(1.0 - 0.4 * ratio, 0.6)
    return sc, sq, sg
 
 
def calculate(B, L, D, c, phi_deg, gamma, FS, eB, eL, shape):
    """Full Terzaghi eccentric footing calculation."""
    # Effective dimensions
    B_eff = B - 2.0 * eB
    L_eff = L - 2.0 * eL
    A_eff = B_eff * L_eff
 
    Nc, Nq, Ng = terzaghi_factors(phi_deg)
    sc, sq, sg = shape_factors(shape, B_eff, L_eff, phi_deg)
 
    q_over = gamma * D   # overburden pressure
 
    contrib_c = c * Nc * sc
    contrib_q = q_over * Nq * sq
    contrib_g = 0.5 * gamma * B_eff * Ng * sg
 
    q_ult = contrib_c + contrib_q + contrib_g
    q_all = q_ult / FS
 
    eB_ratio = eB / B
    eL_ratio = eL / L if L > 0 else 0.0
    kern_ok  = (eB_ratio <= 1.0 / 6.0) and (eL_ratio <= 1.0 / 6.0)
 
    shape_labels = {
        "rectangular": "สี่เหลี่ยมผืนผ้า",
        "square":      "สี่เหลี่ยมจัตุรัส",
        "circular":    "วงกลม",
    }
 
    return {
        "q_ult": q_ult, "q_all": q_all,
        "Nc": Nc, "Nq": Nq, "Ng": Ng,
        "sc": sc, "sq": sq, "sg": sg,
        "B_eff": B_eff, "L_eff": L_eff, "A_eff": A_eff,
        "q_over": q_over,
        "contrib_c": contrib_c, "contrib_q": contrib_q, "contrib_g": contrib_g,
        "eB_ratio": eB_ratio, "eL_ratio": eL_ratio,
        "kern_ok": kern_ok,
        "shape_label": shape_labels[shape],
    }
 
 
# ─── Session State Defaults ──────────────────────────────────────────────────────
DEFAULTS = dict(
    _B=2.0, _L=3.0, _D=1.5,
    _c=20.0, _phi=30.0, _gamma=18.0, _FS=3.0,
    _eB=0.20, _eL=0.10, _shape="rectangular",
)
 
def init_state():
    for k, v in DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v
    if "result" not in st.session_state:
        st.session_state["result"] = None
    if "errors" not in st.session_state:
        st.session_state["errors"] = []
 
def reset_state():
    for k, v in DEFAULTS.items():
        st.session_state[k] = v
    st.session_state["result"] = None
    st.session_state["errors"] = []
 
init_state()
 
 
# ─── Hero ────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">🏗️  GEOTECHNICAL · TERZAGHI (1943)</div>
    <h1>Eccentric Footing Calculator</h1>
    <p>คำนวณกำลังรับน้ำหนักฐานรากเยื้องศูนย์ &nbsp;·&nbsp;
       q<sub>ult</sub> และ q<sub>all</sub> (kPa) ด้วยสูตร Terzaghi + Meyerhof Effective Area</p>
</div>
""", unsafe_allow_html=True)
 
 
# ─── Layout ──────────────────────────────────────────────────────────────────────
left, right = st.columns([1.05, 1.0], gap="large")
 
 
# ══════════════════════════════════════════════════════
# LEFT — INPUTS
# ══════════════════════════════════════════════════════
with left:
    tab_geo, tab_soil = st.tabs(["📐  ฐานราก & เยื้องศูนย์", "🪨  คุณสมบัติดิน"])
 
    # ── Tab 1 : Geometry ─────────────────────────────
    with tab_geo:
        st.markdown('<div class="card-title">ขนาดและความลึกฐานราก</div>', unsafe_allow_html=True)
 
        c1, c2 = st.columns(2)
        with c1:
            st.number_input("ความกว้าง B (m)", min_value=0.10, max_value=50.0,
                            step=0.10, format="%.2f", key="_B")
        with c2:
            st.number_input("ความยาว L (m)", min_value=0.10, max_value=50.0,
                            step=0.10, format="%.2f", key="_L")
 
        st.number_input("ความลึกฐานราก D (m)", min_value=0.10, max_value=20.0,
                        step=0.10, format="%.2f", key="_D")
 
        st.selectbox(
            "รูปร่างฐานราก",
            options=["rectangular", "square", "circular"],
            format_func=lambda x: {
                "rectangular": "สี่เหลี่ยมผืนผ้า (Rectangular)",
                "square":      "สี่เหลี่ยมจัตุรัส (Square)",
                "circular":    "วงกลม (Circular)",
            }[x],
            key="_shape",
        )
 
        st.markdown('<div class="hdiv"></div>', unsafe_allow_html=True)
        st.markdown('<div class="card-title">ความเยื้องศูนย์ (Eccentricity)</div>',
                    unsafe_allow_html=True)
 
        max_eB = max(round(st.session_state["_B"] / 2.0 - 0.001, 3), 0.0)
        max_eL = max(round(st.session_state["_L"] / 2.0 - 0.001, 3), 0.0)
 
        e1, e2 = st.columns(2)
        with e1:
            st.number_input(
                f"eB ตามแนว B (m)  ≤ {max_eB:.3f}",
                min_value=0.0,
                max_value=max_eB,
                value=min(float(st.session_state["_eB"]), max_eB),
                step=0.01, format="%.3f", key="_eB",
            )
        with e2:
            st.number_input(
                f"eL ตามแนว L (m)  ≤ {max_eL:.3f}",
                min_value=0.0,
                max_value=max_eL,
                value=min(float(st.session_state["_eL"]), max_eL),
                step=0.01, format="%.3f", key="_eL",
            )
 
        st.markdown("""
        <div class="alert-ok" style="margin-top:0.5rem;font-size:0.78rem;">
            💡 <b>Meyerhof Effective Area:</b>&nbsp;
            B' = B − 2eB &nbsp;|&nbsp; L' = L − 2eL<br>
            คำนวณ q<sub>ult</sub> บนพื้นที่ประสิทธิผล A' = B' × L'
        </div>
        """, unsafe_allow_html=True)
 
    # ── Tab 2 : Soil ─────────────────────────────────
    with tab_soil:
        st.markdown('<div class="card-title">พารามิเตอร์ดินฐานราก</div>', unsafe_allow_html=True)
 
        st.number_input("แรงยึดเหนี่ยว  c  (kPa)",
                        min_value=0.0, max_value=500.0, step=1.0, format="%.1f", key="_c")
        st.number_input("มุมเสียดทานภายใน  φ  (°)",
                        min_value=0.0, max_value=45.0, step=0.5, format="%.1f", key="_phi")
        st.number_input("หน่วยน้ำหนักดิน  γ  (kN/m³)",
                        min_value=10.0, max_value=25.0, step=0.5, format="%.1f", key="_gamma")
        st.number_input("ค่าความปลอดภัย  FS",
                        min_value=1.0, max_value=10.0, step=0.5, format="%.1f", key="_FS")
 
        st.markdown("""
        <div class="alert-ok" style="margin-top:0.8rem;font-size:0.78rem;">
            📌 <b>ค่า FS แนะนำ:</b> งานทั่วไป = 3.0 &nbsp;|&nbsp; งานสำคัญ = 4.0–5.0<br>
            กรณี φ = 0 (ดินเหนียวอิ่มตัว) → ใช้ Nc = 5.14 โดยอัตโนมัติ
        </div>
        """, unsafe_allow_html=True)
 
    # ── Buttons ──────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    with b1:
        do_calc  = st.button("🔢  คำนวณ", key="btn_calc")
    with b2:
        do_clear = st.button("🗑️  ล้างค่า / Reset", key="btn_clear")
 
 
# ─── Handle Clear ────────────────────────────────────────────────────────────────
if do_clear:
    reset_state()
    st.rerun()
 
 
# ─── Handle Calculate ────────────────────────────────────────────────────────────
if do_calc:
    B_v     = float(st.session_state["_B"])
    L_v     = float(st.session_state["_L"])
    D_v     = float(st.session_state["_D"])
    eB_v    = float(st.session_state["_eB"])
    eL_v    = float(st.session_state["_eL"])
    c_v     = float(st.session_state["_c"])
    phi_v   = float(st.session_state["_phi"])
    gamma_v = float(st.session_state["_gamma"])
    FS_v    = float(st.session_state["_FS"])
    shape_v = st.session_state["_shape"]
 
    errs = []
    if eB_v >= B_v / 2.0:
        errs.append(f"eB = {eB_v:.3f} m ต้องน้อยกว่า B/2 = {B_v/2:.3f} m")
    if eL_v >= L_v / 2.0:
        errs.append(f"eL = {eL_v:.3f} m ต้องน้อยกว่า L/2 = {L_v/2:.3f} m")
    if c_v == 0.0 and phi_v == 0.0:
        errs.append("c และ φ เป็น 0 พร้อมกันไม่ได้ (ดินไม่มีความแข็งแรง)")
 
    if errs:
        st.session_state["errors"] = errs
        st.session_state["result"] = None
    else:
        st.session_state["errors"] = []
        st.session_state["result"] = calculate(
            B_v, L_v, D_v, c_v, phi_v, gamma_v, FS_v, eB_v, eL_v, shape_v
        )
        st.session_state["last_inp"] = dict(FS=FS_v)
 
 
# ══════════════════════════════════════════════════════
# RIGHT — RESULTS
# ══════════════════════════════════════════════════════
with right:
    st.markdown('<div class="card-title">ผลการคำนวณ</div>', unsafe_allow_html=True)
 
    errs   = st.session_state.get("errors", [])
    result = st.session_state.get("result", None)
 
    if errs:
        for e in errs:
            st.markdown(f'<div class="alert-err">⛔  {e}</div>', unsafe_allow_html=True)
 
    if result is None and not errs:
        st.markdown("""
        <div class="placeholder">
            <div class="ph-icon">🏗️</div>
            <p><b>ยังไม่มีผลการคำนวณ</b></p>
            <p style="font-size:0.82rem;margin-top:0.5rem;">
                กรอกข้อมูลด้านซ้าย แล้วกดปุ่ม <b>"คำนวณ"</b>
            </p>
        </div>
        """, unsafe_allow_html=True)
 
    if result:
        r   = result
        FS_ = st.session_state.get("last_inp", {}).get("FS", 3.0)
 
        # q_ult ─────────────────────────────────────
        st.markdown(f"""
        <div class="res-primary">
            <div class="res-label">กำลังรับน้ำหนักสูงสุด — Ultimate Bearing Capacity</div>
            <div class="res-num">{r['q_ult']:,.2f}</div>
            <div class="res-unit">q<sub>ult</sub> &nbsp; kPa</div>
        </div>
        """, unsafe_allow_html=True)
 
        # q_all ─────────────────────────────────────
        st.markdown(f"""
        <div class="res-secondary">
            <div class="res-label">กำลังรับน้ำหนักที่ยอมให้ — Allowable Bearing Capacity</div>
            <div class="res-num">{r['q_all']:,.2f}
                <span style="font-size:1.3rem;font-weight:400;"> kPa</span>
            </div>
            <div class="res-unit">q<sub>all</sub> = q<sub>ult</sub> / FS ({FS_:.1f})</div>
        </div>
        """, unsafe_allow_html=True)
 
        # Kern check ─────────────────────────────────
        if r['kern_ok']:
            st.markdown(f"""
            <div class="alert-ok">
                ✅ <b>แรงกระทำอยู่ภายใน Kern</b> — แรงกดเป็นบวกตลอดพื้นที่ฐานราก<br>
                eB/B = {r['eB_ratio']:.4f} ≤ 1/6 (0.1667) &nbsp;|&nbsp;
                eL/L = {r['eL_ratio']:.4f} ≤ 1/6 (0.1667)
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="alert-warn">
                ⚠️ <b>แรงกระทำอยู่นอก Kern!</b><br>
                eB/B = {r['eB_ratio']:.4f} &nbsp;|&nbsp; eL/L = {r['eL_ratio']:.4f}<br>
                แรงกดที่ขอบฐานรากอาจเป็นลบ — ควรขยายขนาดฐานรากหรือลด eccentricity
            </div>
            """, unsafe_allow_html=True)
 
        st.markdown("<br>", unsafe_allow_html=True)
 
        # Bearing Capacity Factors ───────────────────
        st.markdown('<div class="card-title">Bearing Capacity Factors (Terzaghi)</div>',
                    unsafe_allow_html=True)
        st.markdown(f"""
        <div class="dgrid">
            <div class="ditem">
                <span class="dname">Nc</span>
                <span class="dval">{r['Nc']:.4f}</span>
            </div>
            <div class="ditem">
                <span class="dname">Nq</span>
                <span class="dval">{r['Nq']:.4f}</span>
            </div>
            <div class="ditem">
                <span class="dname">N&#947;</span>
                <span class="dval">{r['Ng']:.4f}</span>
            </div>
            <div class="ditem">
                <span class="dname">q = &#947;&#183;D (kPa)</span>
                <span class="dval">{r['q_over']:.2f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
 
        st.markdown("<br>", unsafe_allow_html=True)
 
        # Effective Area & Shape Factors ─────────────
        st.markdown('<div class="card-title">Shape Factors & พื้นที่ประสิทธิผล</div>',
                    unsafe_allow_html=True)
        st.markdown(f"""
        <div class="dgrid">
            <div class="ditem">
                <span class="dname">รูปร่าง</span>
                <span class="dval">{r['shape_label']}</span>
            </div>
            <div class="ditem">
                <span class="dname">A' = B'&#215;L' (m&#178;)</span>
                <span class="dval">{r['A_eff']:.4f}</span>
            </div>
            <div class="ditem">
                <span class="dname">B' effective (m)</span>
                <span class="dval">{r['B_eff']:.4f}</span>
            </div>
            <div class="ditem">
                <span class="dname">L' effective (m)</span>
                <span class="dval">{r['L_eff']:.4f}</span>
            </div>
            <div class="ditem">
                <span class="dname">sc</span>
                <span class="dval">{r['sc']:.4f}</span>
            </div>
            <div class="ditem">
                <span class="dname">sq</span>
                <span class="dval">{r['sq']:.4f}</span>
            </div>
            <div class="ditem">
                <span class="dname">s&#947;</span>
                <span class="dval">{r['sg']:.4f}</span>
            </div>
            <div class="ditem">
                <span class="dname">eB/B &nbsp;|&nbsp; eL/L</span>
                <span class="dval">{r['eB_ratio']:.4f} | {r['eL_ratio']:.4f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
 
        st.markdown("<br>", unsafe_allow_html=True)
 
        # Term Breakdown ─────────────────────────────
        st.markdown('<div class="card-title">สัดส่วนองค์ประกอบ q_ult</div>',
                    unsafe_allow_html=True)
        total = r['q_ult'] if r['q_ult'] > 0 else 1.0
        pct_c = r['contrib_c'] / total * 100
        pct_q = r['contrib_q'] / total * 100
        pct_g = r['contrib_g'] / total * 100
        st.markdown(f"""
        <div class="dgrid">
            <div class="ditem" style="grid-column:1/-1;background:#ebf8ff;border-color:#bee3f8;">
                <span class="dname" style="color:#2c5282;">c&#183;Nc&#183;sc  (cohesion term)</span>
                <span class="dval" style="color:#2b6cb0;">
                    {r['contrib_c']:.2f} kPa &nbsp;({pct_c:.1f}%)
                </span>
            </div>
            <div class="ditem" style="grid-column:1/-1;background:#faf5ff;border-color:#d6bcfa;">
                <span class="dname" style="color:#44337a;">q&#183;Nq&#183;sq  (surcharge term)</span>
                <span class="dval" style="color:#6b46c1;">
                    {r['contrib_q']:.2f} kPa &nbsp;({pct_q:.1f}%)
                </span>
            </div>
            <div class="ditem" style="grid-column:1/-1;background:#f0fff4;border-color:#9ae6b4;">
                <span class="dname" style="color:#276749;">&#189;&#183;&#947;&#183;B'&#183;N&#947;&#183;s&#947;  (self-weight term)</span>
                <span class="dval" style="color:#276749;">
                    {r['contrib_g']:.2f} kPa &nbsp;({pct_g:.1f}%)
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
 
 
# ─── Formula Reference ───────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("📖  สูตรอ้างอิง — Terzaghi Bearing Capacity Formula"):
    st.markdown("""
    <div class="fbox">
        <div class="ftitle">1 · สูตรหลัก (General Equation)</div>
        <div class="fline">q_ult = c&#183;Nc&#183;sc  +  q&#183;Nq&#183;sq  +  0.5&#183;&#947;&#183;B'&#183;N&#947;&#183;s&#947;</div>
 
        <div class="ftitle">2 · Bearing Capacity Factors (Terzaghi 1943)</div>
        <div class="fline">Nq = exp(&#960;&#183;tan&#966;) &#183; tan&#178;(45 + &#966;/2)</div>
        <div class="fline">Nc = (Nq &#8722; 1) / tan&#966; &nbsp;&nbsp; [&#966;=0 &#8594; Nc = 5.14]</div>
        <div class="fline">N&#947; = (Nq &#8722; 1) &#183; tan(1.4&#966;) &nbsp;&nbsp; [Terzaghi approximation]</div>
 
        <div class="ftitle">3 · Shape Factors</div>
        <div class="fsub">Rectangular:  sc = 1 + 0.2(B'/L') &nbsp;|&nbsp; sq = 1 + (B'/L')&#183;tan&#966; &nbsp;|&nbsp; s&#947; = 1 &#8722; 0.4(B'/L') &#8805; 0.6</div>
        <div class="fsub">Square    :   sc = 1.3 &nbsp;|&nbsp; sq = 1.0 &nbsp;|&nbsp; s&#947; = 0.8</div>
        <div class="fsub">Circular  :   sc = 1.3 &nbsp;|&nbsp; sq = 1.0 &nbsp;|&nbsp; s&#947; = 0.6</div>
 
        <div class="ftitle">4 · Effective Area — Meyerhof</div>
        <div class="fline">B' = B &#8722; 2&#183;eB &nbsp;&nbsp;|&nbsp;&nbsp; L' = L &#8722; 2&#183;eL &nbsp;&nbsp;|&nbsp;&nbsp; A' = B'&#215;L'</div>
 
        <div class="ftitle">5 · Kern Condition</div>
        <div class="fline">eB/B &#8804; 1/6  และ  eL/L &#8804; 1/6 &#8594; แรงกดเป็นบวกทั่วฐานราก</div>
 
        <div class="ftitle">6 · Allowable Bearing Capacity</div>
        <div class="fline">q_all = q_ult / FS</div>
    </div>
    """, unsafe_allow_html=True)
 
 
# ─── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    ECCENTRIC FOOTING CALCULATOR &nbsp;&#183;&nbsp;
    TERZAGHI (1943) + MEYERHOF EFFECTIVE AREA &nbsp;&#183;&nbsp;
    FOR CIVIL ENGINEERING USE ONLY
</div>
""", unsafe_allow_html=True)
