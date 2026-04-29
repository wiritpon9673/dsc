import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import matplotlib
matplotlib.rcParams['font.family'] = ['DejaVu Sans']

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="คำนวณฐานรากเสาเข็มเยื้องศูนย์",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Sarabun', sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #c0392b 0%, #e74c3c 50%, #c0392b 100%);
        padding: 28px 36px;
        border-radius: 16px;
        margin-bottom: 24px;
        text-align: center;
        box-shadow: 0 6px 20px rgba(192,57,43,0.35);
    }
    .main-header h1 {
        color: white;
        font-size: 1.9rem;
        font-weight: 700;
        margin: 0 0 6px 0;
        text-shadow: 1px 2px 4px rgba(0,0,0,0.3);
    }
    .main-header p {
        color: rgba(255,255,255,0.92);
        font-size: 1.0rem;
        margin: 0;
    }

    .section-header {
        background: linear-gradient(90deg, #27ae60, #2ecc71);
        color: white;
        padding: 10px 20px;
        border-radius: 10px;
        font-size: 1.05rem;
        font-weight: 600;
        margin: 18px 0 12px 0;
        box-shadow: 0 3px 8px rgba(39,174,96,0.25);
    }
    .section-header-orange {
        background: linear-gradient(90deg, #e67e22, #f39c12);
        color: white;
        padding: 10px 20px;
        border-radius: 10px;
        font-size: 1.05rem;
        font-weight: 600;
        margin: 18px 0 12px 0;
        box-shadow: 0 3px 8px rgba(230,126,34,0.25);
    }
    .section-header-pink {
        background: linear-gradient(90deg, #8e44ad, #9b59b6);
        color: white;
        padding: 10px 20px;
        border-radius: 10px;
        font-size: 1.05rem;
        font-weight: 600;
        margin: 18px 0 12px 0;
        box-shadow: 0 3px 8px rgba(142,68,173,0.25);
    }

    .info-box {
        background: #eafaf1;
        border-left: 5px solid #27ae60;
        padding: 14px 18px;
        border-radius: 8px;
        margin: 10px 0;
        font-size: 0.92rem;
    }
    .warning-box {
        background: #fef9e7;
        border-left: 5px solid #f39c12;
        padding: 14px 18px;
        border-radius: 8px;
        margin: 10px 0;
        font-size: 0.92rem;
    }
    .danger-box {
        background: #fdedec;
        border-left: 5px solid #e74c3c;
        padding: 14px 18px;
        border-radius: 8px;
        margin: 10px 0;
        font-size: 0.92rem;
    }
    .formula-box {
        background: linear-gradient(135deg, #f0f4ff, #e8f0fe);
        border: 2px solid #4a90d9;
        padding: 16px 20px;
        border-radius: 12px;
        margin: 12px 0;
        text-align: center;
        font-size: 1.05rem;
        font-weight: 600;
        color: #1a3a5c;
        box-shadow: 0 2px 8px rgba(74,144,217,0.15);
    }
    .result-card {
        background: linear-gradient(135deg, #fdfefe, #f2f3f4);
        border: 1.5px solid #bdc3c7;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 8px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    }
    .result-ok {
        background: linear-gradient(135deg, #eafaf1, #d5f5e3);
        border: 2px solid #27ae60;
        border-radius: 12px;
        padding: 14px 20px;
        margin: 8px 0;
        font-weight: 600;
        color: #1e8449;
    }
    .result-fail {
        background: linear-gradient(135deg, #fdedec, #fadbd8);
        border: 2px solid #e74c3c;
        border-radius: 12px;
        padding: 14px 20px;
        margin: 8px 0;
        font-weight: 600;
        color: #922b21;
    }
    .centroid-box {
        background: linear-gradient(135deg, #fff3e0, #ffe0b2);
        border: 2px solid #e67e22;
        border-radius: 12px;
        padding: 14px 20px;
        margin: 8px 0;
        text-align: center;
    }
    .step-badge {
        display: inline-block;
        background: #27ae60;
        color: white;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        line-height: 30px;
        text-align: center;
        font-weight: 700;
        font-size: 1rem;
        margin-right: 8px;
    }
    .ref-box {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 10px 16px;
        font-size: 0.82rem;
        color: #555;
        margin-top: 8px;
    }
    div[data-testid="stNumberInput"] label {
        font-size: 0.93rem;
    }
    .stDataFrame { font-size: 0.9rem; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="main-header">
    <h1>🏗️ โปรแกรมคำนวณฐานรากเสาเข็มเยื้องศูนย์</h1>
    <p>Pile Foundation Eccentricity Calculator | อ้างอิง มยผ.1106-64 | Bakhoum (1992)</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR – MODE & TOLERANCE
# ============================================================
with st.sidebar:
    st.markdown("### ⚙️ ตั้งค่าการคำนวณ")
    st.markdown("---")

    calc_mode = st.radio(
        "**รูปแบบการเยื้องศูนย์**",
        ["แบบสมมาตร (≤ 2 ต้น)", "แบบไม่สมมาตร (> 2 ต้น)"],
        help="เลือกตามจำนวนเสาเข็มและลักษณะการเยื้อง"
    )

    st.markdown("---")
    st.markdown("### 📐 ข้อกำหนด มยผ.1106-64")
    tol_1_2 = st.number_input("เยื้องศูนย์สูงสุด (1-2 ต้น) [mm]", value=50, min_value=1)
    tol_3up = st.number_input("เยื้องศูนย์สูงสุด (≥3 ต้น) [mm]", value=75, min_value=1)

    st.markdown("---")
    st.markdown("### ℹ️ เกี่ยวกับโปรแกรม")
    st.markdown("""
    <div class="ref-box">
    บรรยายโดย รศ.ดร.อิทธิพล มีผล<br>
    ภาควิชาครุศาสตร์โยธา<br>
    มจพ. (KMUTNB)<br><br>
    อ้างอิง: มยผ.1106-64, Bakhoum (1992)
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def check_eccentricity_tolerance(ex_mm, ey_mm, n_piles, tol_1_2, tol_3up):
    e = np.sqrt(ex_mm**2 + ey_mm**2)
    limit = tol_1_2 if n_piles <= 2 else tol_3up
    return e, limit, e <= limit

def compute_centroid(pile_data):
    """pile_data: list of (ex, ey) in cm"""
    n = len(pile_data)
    X_bar = sum(p[0] for p in pile_data) / n
    Y_bar = sum(p[1] for p in pile_data) / n
    return X_bar, Y_bar

def compute_new_coords(pile_data, X_bar, Y_bar):
    """new x,y relative to new centroid"""
    return [(p[0] - X_bar, p[1] - Y_bar) for p in pile_data]

def symmetric_pile_reaction(Q, Mx, My, new_coords):
    """สำหรับเสาเข็ม ≤ 2 ต้น (แบบสมมาตร)"""
    n = len(new_coords)
    sum_x2 = sum(c[0]**2 for c in new_coords)
    sum_y2 = sum(c[1]**2 for c in new_coords)
    reactions = []
    for x, y in new_coords:
        Pi = (Q/n) + (My*x/sum_x2 if sum_x2 != 0 else 0) + (Mx*y/sum_y2 if sum_y2 != 0 else 0)
        reactions.append(Pi)
    return reactions, sum_x2, sum_y2

def asymmetric_pile_reaction(Q, Mx, My, new_coords):
    """สำหรับเสาเข็ม > 2 ต้น (Bakhoum 1992)"""
    n = len(new_coords)
    xs = [c[0] for c in new_coords]
    ys = [c[1] for c in new_coords]
    sum_x2 = sum(xi**2 for xi in xs)
    sum_y2 = sum(yi**2 for yi in ys)
    sum_xy = sum(xs[i]*ys[i] for i in range(n))

    denom = sum_x2 * sum_y2 - sum_xy**2
    if abs(denom) < 1e-10:
        # fallback to symmetric formula
        return symmetric_pile_reaction(Q, Mx, My, new_coords)[0], sum_x2, sum_y2, sum_xy

    m = (My * sum_y2 - Mx * sum_xy) / denom
    nv = (Mx * sum_x2 - My * sum_xy) / denom

    reactions = []
    for x, y in new_coords:
        Pi = (Q/n) + m*x + nv*y
        reactions.append(Pi)
    return reactions, sum_x2, sum_y2, sum_xy

# ============================================================
# TAB LAYOUT
# ============================================================
tab1, tab2, tab3 = st.tabs(["📊 คำนวณแรงในเสาเข็ม", "📐 ตรวจสอบข้อกำหนด", "📖 สูตรและทฤษฎี"])

# ============================================================
# TAB 1: MAIN CALCULATION
# ============================================================
with tab1:
    col_input, col_result = st.columns([1, 1.05], gap="large")

    # -------- INPUT COLUMN --------
    with col_input:
        st.markdown('<div class="section-header">① ข้อมูลฐานราก</div>', unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            Q = st.number_input("แรงกระทำ Q (ตัน)", value=150.0, min_value=0.1, step=5.0, format="%.2f")
            pile_cap = st.number_input("กำลังรับน้ำหนักปลอดภัย (ตัน/ต้น)", value=40.0, min_value=1.0, step=1.0)
        with col_b:
            n_piles = st.number_input("จำนวนเสาเข็ม (ต้น)", value=4, min_value=2, max_value=12, step=1)
            pile_size = st.number_input("ขนาดเสาเข็ม Dp (cm)", value=30.0, min_value=10.0, step=5.0)

        st.markdown('<div class="section-header">② ระยะเยื้องศูนย์ของเสาเข็มแต่ละต้น</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box">
        📌 ป้อนระยะเยื้องศูนย์จากตำแหน่งเดิม (ก่อนเยื้อง) ของเสาเข็มแต่ละต้น<br>
        โดยกำหนดให้จุดกึ่งกลางกลุ่มเสาเข็มเดิมอยู่ที่ (0, 0)<br>
        <b>ex</b> = ระยะในแนว X (cm), <b>ey</b> = ระยะในแนว Y (cm)
        </div>
        """, unsafe_allow_html=True)

        # Default positions based on common pile arrangements
        def default_positions(n, s=75):
            """Return default pile positions for n piles with spacing s cm"""
            hs = s/2
            if n == 2:
                return [(-hs, 0), (hs, 0)]
            elif n == 3:
                return [(-hs, -s*0.29), (hs, -s*0.29), (0, s*0.58)]
            elif n == 4:
                return [(-hs, -hs), (hs, -hs), (-hs, hs), (hs, hs)]
            elif n == 5:
                return [(-hs, -hs), (hs, -hs), (-hs, hs), (hs, hs), (0, 0)]
            elif n == 6:
                return [(-s, -hs), (0, -hs), (s, -hs), (-s, hs), (0, hs), (s, hs)]
            else:
                # generic grid
                cols = int(np.ceil(np.sqrt(n)))
                rows = int(np.ceil(n / cols))
                positions = []
                for r in range(rows):
                    for c in range(cols):
                        if len(positions) < n:
                            positions.append(((c - (cols-1)/2)*s, (r - (rows-1)/2)*s))
                return positions

        defaults = default_positions(int(n_piles))

        pile_original = []  # original (design) positions in cm
        pile_eccentric = []  # actual (after eccentricity) positions in cm

        # Detect mode for number of piles
        is_symmetric = ("สมมาตร" in calc_mode) or (int(n_piles) <= 2)

        st.markdown("**ตำแหน่งเสาเข็ม (ก่อนเยื้องศูนย์) และระยะเยื้อง:**")

        df_input_data = []
        for i in range(int(n_piles)):
            st.markdown(f"**เสาเข็มต้นที่ {i+1}**")
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                ox = defaults[i][0] if i < len(defaults) else 0.0
                orig_x = st.number_input(f"ตำแหน่ง X เดิม (cm)", value=float(ox), key=f"ox_{i}", format="%.1f", label_visibility="visible")
            with c2:
                oy = defaults[i][1] if i < len(defaults) else 0.0
                orig_y = st.number_input(f"ตำแหน่ง Y เดิม (cm)", value=float(oy), key=f"oy_{i}", format="%.1f", label_visibility="visible")
            with c3:
                ecc_x = st.number_input(f"เยื้อง ΔX (cm)", value=0.0, key=f"ex_{i}", format="%.1f",
                                         help="ระยะเยื้องในแนว X จากตำแหน่งเดิม (+/-)")
            with c4:
                ecc_y = st.number_input(f"เยื้อง ΔY (cm)", value=(5.0 if i == 0 else 0.0), key=f"ey_{i}", format="%.1f",
                                         help="ระยะเยื้องในแนว Y จากตำแหน่งเดิม (+/-)")

            actual_x = orig_x + ecc_x
            actual_y = orig_y + ecc_y
            pile_original.append((orig_x, orig_y))
            pile_eccentric.append((actual_x, actual_y))
            df_input_data.append({
                "ต้นที่": i+1,
                "X เดิม (cm)": orig_x, "Y เดิม (cm)": orig_y,
                "ΔX (cm)": ecc_x, "ΔY (cm)": ecc_y,
                "X จริง (cm)": actual_x, "Y จริง (cm)": actual_y,
                "เยื้องรวม (mm)": round(np.sqrt(ecc_x**2 + ecc_y**2)*10, 1)
            })

        df_input = pd.DataFrame(df_input_data)

    # -------- RESULT COLUMN --------
    with col_result:
        st.markdown('<div class="section-header-orange">③ ผลการคำนวณ</div>', unsafe_allow_html=True)

        # Step 1: Find new centroid
        X_bar, Y_bar = compute_centroid(pile_eccentric)

        st.markdown(f"""
        <div class="centroid-box">
        <b>จุด Centroid ใหม่ของกลุ่มเสาเข็ม</b><br><br>
        <span style="font-size:1.3rem; color:#c0392b; font-weight:700;">
        X̄ = {X_bar:.3f} cm &nbsp;|&nbsp; Ȳ = {Y_bar:.3f} cm
        </span>
        </div>
        """, unsafe_allow_html=True)

        # Step 2: Compute moments
        Mx = Q * Y_bar   # ton-cm
        My = Q * X_bar   # ton-cm

        col_mx, col_my = st.columns(2)
        with col_mx:
            st.markdown(f"""
            <div class="result-card" style="text-align:center;">
            <b>โมเมนต์ M<sub>x</sub></b><br>
            <span style="font-size:1.2rem; color:#8e44ad; font-weight:700;">
            {Mx:.2f} ตัน-cm<br>= {Mx/100:.4f} ตัน-m
            </span>
            </div>
            """, unsafe_allow_html=True)
        with col_my:
            st.markdown(f"""
            <div class="result-card" style="text-align:center;">
            <b>โมเมนต์ M<sub>y</sub></b><br>
            <span style="font-size:1.2rem; color:#8e44ad; font-weight:700;">
            {My:.2f} ตัน-cm<br>= {My/100:.4f} ตัน-m
            </span>
            </div>
            """, unsafe_allow_html=True)

        # Step 3: New pile coordinates
        new_coords = compute_new_coords(pile_eccentric, X_bar, Y_bar)

        # Step 4: Pile reactions
        if is_symmetric or int(n_piles) <= 2:
            reactions, sum_x2, sum_y2 = symmetric_pile_reaction(Q, Mx, My, new_coords)
            sum_xy = sum(c[0]*c[1] for c in new_coords)
        else:
            result = asymmetric_pile_reaction(Q, Mx, My, new_coords)
            if len(result) == 4:
                reactions, sum_x2, sum_y2, sum_xy = result
            else:
                reactions, sum_x2, sum_y2 = result
                sum_xy = sum(c[0]*c[1] for c in new_coords)

        # Display reaction table
        st.markdown('<div class="section-header-pink">④ แรงปฏิกิริยาในเสาเข็มแต่ละต้น</div>', unsafe_allow_html=True)

        table_rows = []
        for i, (Pi, (xi, yi)) in enumerate(zip(reactions, new_coords)):
            status = "✅ OK" if Pi <= pile_cap else "❌ เกิน"
            table_rows.append({
                "ต้นที่": i+1,
                "x (cm)": round(xi, 3),
                "y (cm)": round(yi, 3),
                "x² (cm²)": round(xi**2, 3),
                "y² (cm²)": round(yi**2, 3),
                "Pi (ตัน)": round(Pi, 3),
                "ตรวจสอบ": status
            })

        df_result = pd.DataFrame(table_rows)

        # Color the Pi column
        def highlight_pi(val):
            if isinstance(val, str):
                return "color: green; font-weight: bold" if "✅" in val else "color: red; font-weight: bold"
            return ""

        st.dataframe(
            df_result.style.applymap(highlight_pi, subset=["ตรวจสอบ"]),
            use_container_width=True, hide_index=True
        )

        # Summary
        P_max = max(reactions)
        P_min = min(reactions)
        P_avg = sum(reactions) / len(reactions)
        all_ok = all(Pi <= pile_cap for Pi in reactions)

        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            st.metric("P สูงสุด (ตัน)", f"{P_max:.2f}", delta=f"{P_max - pile_cap:.2f} vs ปลอดภัย")
        with col_s2:
            st.metric("P ต่ำสุด (ตัน)", f"{P_min:.2f}")
        with col_s3:
            st.metric("ΣPi (ตัน)", f"{sum(reactions):.2f}", delta=f"vs Q={Q:.1f}")

        if all_ok:
            st.markdown(f"""
            <div class="result-ok">
            ✅ ผ่าน — เสาเข็มทุกต้นรับแรงไม่เกินกำลังรับน้ำหนักปลอดภัย {pile_cap:.1f} ตัน/ต้น
            </div>
            """, unsafe_allow_html=True)
        else:
            failed = [i+1 for i, Pi in enumerate(reactions) if Pi > pile_cap]
            st.markdown(f"""
            <div class="result-fail">
            ❌ ไม่ผ่าน — เสาเข็มต้นที่ {failed} รับแรงเกินกำลังรับน้ำหนักปลอดภัย {pile_cap:.1f} ตัน/ต้น
            </div>
            """, unsafe_allow_html=True)

        # -------- DIAGRAM --------
        st.markdown('<div class="section-header">⑤ ผังตำแหน่งเสาเข็ม</div>', unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(6, 5))
        ax.set_aspect('equal')
        ax.set_facecolor('#f8f9fa')
        fig.patch.set_facecolor('#ffffff')
        ax.grid(True, linestyle='--', alpha=0.4, color='#cccccc')
        ax.set_title("ผังตำแหน่งเสาเข็ม (ก่อน/หลังเยื้องศูนย์)", fontsize=10, fontweight='bold', pad=10)

        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#e67e22', '#e91e63']

        for i, ((ox, oy), (ax2, ay)) in enumerate(zip(pile_original, pile_eccentric)):
            c = colors[i % len(colors)]
            # original position (hollow)
            circle_orig = plt.Circle((ox, oy), 4, fill=False, edgecolor=c, linewidth=1.5, linestyle='--', alpha=0.6)
            ax.add_patch(circle_orig)
            # actual position (filled)
            circle_act = plt.Circle((ax2, ay), 4, fill=True, facecolor=c, edgecolor='white', linewidth=1.5, alpha=0.85, zorder=3)
            ax.add_patch(circle_act)
            # Arrow from original to actual
            if abs(ox - ax2) > 0.1 or abs(oy - ay) > 0.1:
                ax.annotate('', xy=(ax2, ay), xytext=(ox, oy),
                            arrowprops=dict(arrowstyle='->', color=c, lw=1.5))
            ax.text(ax2 + 5, ay + 5, f"P{i+1}\n{reactions[i]:.1f}t", fontsize=7.5,
                    color=c, fontweight='bold', zorder=4)

        # Plot centroids
        orig_cent_x = sum(p[0] for p in pile_original) / len(pile_original)
        orig_cent_y = sum(p[1] for p in pile_original) / len(pile_original)
        ax.plot(orig_cent_x, orig_cent_y, 'k+', markersize=12, markeredgewidth=2, zorder=5, label=f"Centroid เดิม (0,0)")
        ax.plot(X_bar, Y_bar, 'r*', markersize=14, zorder=5, label=f"Centroid ใหม่ ({X_bar:.2f},{Y_bar:.2f})")

        # Axes
        ax.axhline(0, color='gray', linewidth=0.8, alpha=0.5)
        ax.axvline(0, color='gray', linewidth=0.8, alpha=0.5)
        ax.set_xlabel("X (cm)", fontsize=9)
        ax.set_ylabel("Y (cm)", fontsize=9)

        legend_patches = [
            mpatches.Patch(color='none', label='○ ตำแหน่งเดิม (เส้นประ)'),
            mpatches.Patch(color='#555', label='● ตำแหน่งจริง (เยื้องแล้ว)'),
        ]
        ax.legend(handles=legend_patches + ax.get_lines()[-2:], fontsize=7.5, loc='lower right')

        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        # Summary table
        st.markdown("**สรุปค่าที่ใช้ในสมการ**")
        summary_data = {
            "ค่า": ["Σx²", "Σy²", "Σxy", "Mx (ตัน-cm)", "My (ตัน-cm)", "X̄ (cm)", "Ȳ (cm)"],
            "ผลลัพธ์": [f"{sum_x2:.3f}", f"{sum_y2:.3f}", f"{sum_xy:.3f}",
                        f"{Mx:.3f}", f"{My:.3f}", f"{X_bar:.3f}", f"{Y_bar:.3f}"]
        }
        st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)

# ============================================================
# TAB 2: TOLERANCE CHECK
# ============================================================
with tab2:
    st.markdown('<div class="section-header">ตรวจสอบการเยื้องศูนย์ตาม มยผ.1106-64</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="info-box">
    📌 <b>ข้อกำหนด มยผ.1106-64</b><br>
    • เสาเข็ม 1-2 ต้น: ยอมให้เยื้องศูนย์ไม่เกิน <b>{tol_1_2} มม.</b><br>
    • เสาเข็ม ≥ 3 ต้น: ยอมให้เยื้องศูนย์ไม่เกิน <b>{tol_3up} มม.</b><br>
    • วัดที่ระดับตัดหัวเสาเข็ม | ความเอียงไม่เกิน 1:100
    </div>
    """, unsafe_allow_html=True)

    tol_rows = []
    for row in df_input.to_dict('records'):
        i = row["ต้นที่"] - 1
        e_mm = row["เยื้องรวม (mm)"]
        limit = tol_1_2 if int(n_piles) <= 2 else tol_3up
        pass_fail = "✅ ผ่าน" if e_mm <= limit else "❌ ไม่ผ่าน"
        tol_rows.append({
            "เสาเข็มต้นที่": row["ต้นที่"],
            "ΔX (cm)": row["ΔX (cm)"],
            "ΔY (cm)": row["ΔY (cm)"],
            "เยื้องรวม (mm)": e_mm,
            f"เกณฑ์ (mm)": limit,
            "ผล": pass_fail
        })

    df_tol = pd.DataFrame(tol_rows)

    def color_result(val):
        if "✅" in str(val):
            return "color: green; font-weight: bold"
        elif "❌" in str(val):
            return "color: red; font-weight: bold"
        return ""

    st.dataframe(
        df_tol.style.applymap(color_result, subset=["ผล"]),
        use_container_width=True, hide_index=True
    )

    all_tol_ok = all("✅" in r["ผล"] for r in tol_rows)
    if all_tol_ok:
        st.markdown(f"""
        <div class="result-ok">
        ✅ เสาเข็มทุกต้นมีระยะเยื้องศูนย์อยู่ในเกณฑ์ที่ยอมรับได้ตาม มยผ.1106-64
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-fail">
        ❌ มีเสาเข็มบางต้นเยื้องศูนย์เกินเกณฑ์ที่กำหนด ควรตรวจสอบและแก้ไข
        </div>
        """, unsafe_allow_html=True)

    # Eccentricity bar chart
    st.markdown("**กราฟแสดงระยะเยื้องศูนย์ของเสาเข็มแต่ละต้น**")
    fig2, ax2 = plt.subplots(figsize=(8, 3.5))
    pile_labels = [f"P{r['เสาเข็มต้นที่']}" for r in tol_rows]
    eccs = [r["เยื้องรวม (mm)"] for r in tol_rows]
    limit = tol_1_2 if int(n_piles) <= 2 else tol_3up
    bar_colors = ['#27ae60' if e <= limit else '#e74c3c' for e in eccs]
    bars = ax2.bar(pile_labels, eccs, color=bar_colors, edgecolor='white', linewidth=1.2, zorder=3)
    ax2.axhline(limit, color='#e74c3c', linestyle='--', linewidth=2, label=f"เกณฑ์ {limit} mm", zorder=4)
    ax2.set_ylabel("ระยะเยื้องศูนย์ (mm)", fontsize=9)
    ax2.set_title("ระยะเยื้องศูนย์ของเสาเข็มแต่ละต้น", fontsize=10, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(axis='y', alpha=0.4)
    ax2.set_facecolor('#f8f9fa')
    for bar, val in zip(bars, eccs):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, f"{val:.1f}", ha='center', va='bottom', fontsize=8.5, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close()

# ============================================================
# TAB 3: THEORY
# ============================================================
with tab3:
    st.markdown('<div class="section-header">สูตรและทฤษฎีที่ใช้ในโปรแกรม</div>', unsafe_allow_html=True)

    st.markdown("### 📌 ขั้นตอนการคำนวณ")

    st.markdown("""
    <div class="result-card">
    <b><span class="step-badge" style="background:#27ae60;color:white;border-radius:50%;padding:3px 10px;">1</span>
    หาจุด Centroid ใหม่ของกลุ่มเสาเข็ม (หลังเยื้องศูนย์)</b><br><br>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="formula-box">
    X̄ = (Σ eₓᵢ) / n &nbsp;&nbsp;&nbsp;&nbsp; Ȳ = (Σ eᵧᵢ) / n
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="result-card">
    <b><span style="background:#27ae60;color:white;border-radius:50%;padding:3px 10px;">2</span>
    คำนวณโมเมนต์ที่เกิดจากการเยื้องศูนย์</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="formula-box">
    Mₓ = Q × Ȳ &nbsp;&nbsp;&nbsp;&nbsp; Mᵧ = Q × X̄
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="result-card">
    <b><span style="background:#27ae60;color:white;border-radius:50%;padding:3px 10px;">3</span>
    หาพิกัดเสาเข็มใหม่จาก Centroid ใหม่</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="formula-box">
    xᵢ = eₓᵢ − X̄ &nbsp;&nbsp;&nbsp;&nbsp; yᵢ = eᵧᵢ − Ȳ
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    col_f1, col_f2 = st.columns(2)

    with col_f1:
        st.markdown("#### 🔹 แบบสมมาตร (≤ 2 ต้น)")
        st.markdown("""
        <div class="formula-box" style="font-size:0.95rem;">
        Pᵢ = (Q/n) + (Mᵧ·xᵢ / Σx²) + (Mₓ·yᵢ / Σy²)
        </div>
        """, unsafe_allow_html=True)

    with col_f2:
        st.markdown("#### 🔸 แบบไม่สมมาตร (> 2 ต้น) — Bakhoum (1992)")
        st.markdown("""
        <div class="formula-box" style="font-size:0.95rem;">
        Pᵢ = (Q/n) ± (m·xᵢ) ± (n·yᵢ)
        <br><br>
        m = (Mᵧ·Σy² − Mₓ·Σxy) / (Σx²·Σy² − (Σxy)²)
        <br>
        n = (Mₓ·Σx² − Mᵧ·Σxy) / (Σx²·Σy² − (Σxy)²)
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📐 ข้อกำหนด มยผ.1106-64")
    st.markdown(f"""
    <div class="warning-box">
    <b>ที่ระดับตัดหัวเสาเข็ม:</b><br>
    • เสาเข็ม 1 ต้น และ 2 ต้น: ยอมให้เยื้องศูนย์ไม่เกิน <b>50 มม.</b><br>
    • เสาเข็มตั้งแต่ 3 ต้นขึ้นไป: ยอมให้เยื้องศูนย์ไม่เกิน <b>75 มม.</b><br>
    • ความเอียงของเสาเข็มต้องไม่เกิน <b>1:100</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📦 ระยะห่างระหว่างเสาเข็ม")
    st.markdown("""
    <div class="info-box">
    S ≥ 3 เท่า ของขนาดเสาเข็มที่เลือกใช้ (Dp)<br>
    <b>ขนาดฐานราก:</b> ขอบนอก = 1–1.5 Dp จากขอบเสาเข็ม
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📊 น้ำหนักบรรทุกของเสาเข็ม")
    st.markdown("""
    <div class="info-box">
    • แรงต้านทานผิว (Friction Resistance): ประมาณ <b>90%</b> ของน้ำหนักบรรทุกทั้งหมด<br>
    • แรงต้านทานปลาย (End/Point Bearing): ประมาณ <b>10%</b> ของน้ำหนักบรรทุกทั้งหมด
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div class="ref-box">
    <b>อ้างอิง:</b><br>
    • Bakhoum, M.M. (1992). Pile Group Analysis<br>
    • มาตรฐานงานวิศวกรรมฐานราก มยผ.1106-64<br>
    • บรรยายโดย รศ.ดร.อิทธิพล มีผล, ภาควิชาครุศาสตร์โยธา, มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ
    </div>
    """, unsafe_allow_html=True)
