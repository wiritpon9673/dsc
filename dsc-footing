"""
=============================================================
  โปรแกรมออกแบบฐานรากแผ่ (Isolated Footing Design)
  ตาม ACI 318 / วสท. (ฐานรากสี่เหลี่ยม รับแรงในแนวดิ่ง)
=============================================================
  Author  : Foundation Design Tool
  Standard: ACI 318-19 / วสท. 1012-58
=============================================================
"""

import math


# ─────────────────────────────────────────────
#  1. ข้อมูลนำเข้า (Input Parameters)
# ─────────────────────────────────────────────

class FootingInput:
    """เก็บข้อมูลนำเข้าสำหรับออกแบบฐานราก"""

    def __init__(
        self,
        P: float,          # แรงกระทำในแนวดิ่ง [kN]
        Mx: float,         # โมเมนต์รอบแกน X [kN·m]
        My: float,         # โมเมนต์รอบแกน Y [kN·m]
        bc: float,         # ความกว้างเสา [m]
        hc: float,         # ความยาวเสา [m]
        q_allow: float,    # กำลังรับน้ำหนักดินที่ยอมให้ [kN/m²]
        Df: float,         # ความลึกฝังฐานราก [m]
        gamma_soil: float, # น้ำหนักดิน [kN/m³]
        t: float,          # ความหนาฐานราก [m]
        fc: float,         # กำลังอัดคอนกรีต [MPa]
        fy: float,         # กำลังครากเหล็ก [MPa]
        cover: float,      # ระยะหุ้ม [m]
        bar_dia: float = 0.020,  # เส้นผ่าศูนย์กลางเหล็ก [m]
    ):
        self.P = P
        self.Mx = Mx
        self.My = My
        self.bc = bc
        self.hc = hc
        self.q_allow = q_allow
        self.Df = Df
        self.gamma_soil = gamma_soil
        self.t = t
        self.fc = fc
        self.fy = fy
        self.cover = cover
        self.bar_dia = bar_dia

        self.gamma_conc = 24.0   # kN/m³ (คอนกรีต)
        self.phi_flex = 0.90     # ค่า φ สำหรับดัด
        self.phi_shear = 0.75    # ค่า φ สำหรับแรงเฉือน


# ─────────────────────────────────────────────
#  2. ผลการออกแบบ (Output Results)
# ─────────────────────────────────────────────

class FootingResult:
    """เก็บผลลัพธ์การออกแบบ"""
    pass


# ─────────────────────────────────────────────
#  3. ฟังก์ชันหลัก
# ─────────────────────────────────────────────

def size_footing(inp: FootingInput) -> tuple[float, float]:
    """
    หาขนาดฐานราก B × L (m)
    โดยให้ความดันดินสูงสุดไม่เกิน q_allow
    """
    q_net = inp.q_allow - inp.gamma_soil * inp.Df  # net bearing capacity
    A_req = inp.P / q_net                           # พื้นที่เริ่มต้น

    if inp.Mx == 0 and inp.My == 0:
        # ไม่มีโมเมนต์ → ฐานรากสี่เหลี่ยมจัตุรัส
        side = math.ceil(math.sqrt(A_req) * 10) / 10  # ปัดขึ้น 0.1 m
        return side, side
    else:
        # มีโมเมนต์ → ขยายขนาดจนผ่าน
        B = L = math.ceil(math.sqrt(A_req) * 10) / 10 + 0.1
        for _ in range(50):
            A = B * L
            Wf = (inp.gamma_conc * A * inp.t
                  + inp.gamma_soil * A * (inp.Df - inp.t))
            Ptot = inp.P + Wf
            eL = inp.My / Ptot
            eB = inp.Mx / Ptot
            q_max = (Ptot / A) * (1 + 6 * eL / L + 6 * eB / B)
            if q_max > inp.q_allow:
                B += 0.1
                L += 0.1
            else:
                break
        return B, L


def calc_soil_pressure(inp: FootingInput, B: float, L: float):
    """คำนวณความดันดิน q_max, q_min [kN/m²]"""
    A = B * L
    Wf = (inp.gamma_conc * A * inp.t
          + inp.gamma_soil * A * (inp.Df - inp.t))
    Ptot = inp.P + Wf
    eL = inp.My / Ptot if Ptot != 0 else 0
    eB = inp.Mx / Ptot if Ptot != 0 else 0
    q_max = (Ptot / A) * (1 + 6 * eL / L + 6 * eB / B)
    q_min = (Ptot / A) * (1 - 6 * eL / L - 6 * eB / B)
    return q_max, q_min


def calc_effective_depth(inp: FootingInput) -> float:
    """คำนวณระยะประสิทธิผล d [m]"""
    return inp.t - inp.cover - inp.bar_dia / 2


def check_one_way_shear(inp: FootingInput, B: float, L: float,
                         qu: float, d: float) -> dict:
    """
    ตรวจสอบแรงเฉือนทางเดียว (One-Way Shear)
    หน้าตัดวิกฤตอยู่ห่างจากหน้าเสา d
    """
    # ทิศทาง L (cantilever จาก B)
    lv_L = (L - inp.hc) / 2 - d
    Vu_L = qu * B * max(lv_L, 0)
    phi_Vc_L = inp.phi_shear * (1/6) * math.sqrt(inp.fc) * 1000 * B * d  # kN

    # ทิศทาง B (cantilever จาก L)
    lv_B = (B - inp.bc) / 2 - d
    Vu_B = qu * L * max(lv_B, 0)
    phi_Vc_B = inp.phi_shear * (1/6) * math.sqrt(inp.fc) * 1000 * L * d  # kN

    return {
        "Vu_L":      Vu_L,
        "phiVc_L":   phi_Vc_L,
        "ok_L":      Vu_L <= phi_Vc_L,
        "Vu_B":      Vu_B,
        "phiVc_B":   phi_Vc_B,
        "ok_B":      Vu_B <= phi_Vc_B,
    }


def check_punching_shear(inp: FootingInput, B: float, L: float,
                          qu: float, d: float) -> dict:
    """
    ตรวจสอบแรงเจาะ (Two-Way / Punching Shear)
    เส้นรอบรูปวิกฤต bo อยู่ห่างจากหน้าเสา d/2
    """
    bo = 2 * ((inp.bc + d) + (inp.hc + d))
    A_punch = (inp.bc + d) * (inp.hc + d)
    Vu2 = qu * (B * L - A_punch)

    # กำลังต้านแรงเจาะ (ACI 318 §22.6.5)
    beta = inp.hc / inp.bc          # อัตราส่วนด้านยาว/ด้านสั้น
    alpha_s = 40                     # เสาภายใน = 40
    vc = min(
        0.083 * (2 + 4 / beta) * math.sqrt(inp.fc),
        0.083 * (alpha_s * d / bo + 2) * math.sqrt(inp.fc),
        0.333 * math.sqrt(inp.fc),
    )
    phi_Vc2 = inp.phi_shear * vc * 1000 * bo * d   # kN

    return {
        "bo":      bo,
        "Vu2":     Vu2,
        "phiVc2":  phi_Vc2,
        "ok":      Vu2 <= phi_Vc2,
    }


def calc_flexure(inp: FootingInput, B: float, L: float,
                  qu: float, d: float) -> dict:
    """
    คำนวณเหล็กเสริม (Flexural Reinforcement)
    หน้าตัดวิกฤตที่หน้าเสา
    """
    rho_min = max(0.0018, 1.4 / inp.fy)

    def steel_area(Mu_kNm: float, width: float) -> tuple[float, float, float]:
        """
        คืนค่า (As_req, As_min, As_use) [m²]
        Mu_kNm : โมเมนต์ [kN·m]
        width  : ความกว้างฐาน [m]
        d      : ระยะประสิทธิผล [m]
        → Rn = Mu / (φ · b · d²) [MPa]
        """
        # แปลงหน่วย: kN·m → N·mm, m → mm
        Mu_Nmm = Mu_kNm * 1e6          # N·mm
        b_mm   = width * 1000           # mm
        d_mm   = d * 1000               # mm
        Rn_MPa = Mu_Nmm / (inp.phi_flex * b_mm * d_mm ** 2)   # MPa
        disc = 1 - (2 * Rn_MPa) / (0.85 * inp.fc)
        if disc < 0:
            raise ValueError("หน้าตัดมีกำลังไม่พอ ต้องเพิ่มความหนาฐานราก")
        rho = (0.85 * inp.fc / inp.fy) * (1 - math.sqrt(disc))
        As_req  = rho * width * d          # m²
        As_min  = rho_min * width * d
        As_use  = max(As_req, As_min)
        return As_req, As_min, As_use

    # ทิศทาง B (cantilever = (B - bc)/2)
    lm_B = (B - inp.bc) / 2
    Mu_B = qu * L * lm_B ** 2 / 2
    AsB_req, AsB_min, AsB_use = steel_area(Mu_B, L)

    # ทิศทาง L (cantilever = (L - hc)/2)
    lm_L = (L - inp.hc) / 2
    Mu_L = qu * B * lm_L ** 2 / 2
    AsL_req, AsL_min, AsL_use = steel_area(Mu_L, B)

    return {
        "Mu_B":    Mu_B,
        "As_B":    AsB_req,
        "Asmin_B": AsB_min,
        "Asuse_B": AsB_use,
        "Mu_L":    Mu_L,
        "As_L":    AsL_req,
        "Asmin_L": AsL_min,
        "Asuse_L": AsL_use,
    }


# ─────────────────────────────────────────────
#  4. ฟังก์ชัน Design หลัก
# ─────────────────────────────────────────────

def design_footing(inp: FootingInput) -> None:
    """
    ออกแบบฐานรากแผ่แล้วพิมพ์ผลลัพธ์
    """
    sep = "=" * 60

    print(sep)
    print("  การออกแบบฐานรากแผ่ (Isolated Footing Design)")
    print(sep)

    # --- ขนาดฐานราก ---
    B, L = size_footing(inp)
    A = B * L
    print(f"\n{'[1] ขนาดฐานราก':}")
    print(f"    B = {B:.2f} m,  L = {L:.2f} m,  A = {A:.2f} m²")

    # --- ความดันดิน ---
    q_max, q_min = calc_soil_pressure(inp, B, L)
    status_q = "✓ ผ่าน" if q_max <= inp.q_allow else "✗ ไม่ผ่าน (ต้องขยายขนาด)"
    print(f"\n{'[2] ความดันดิน':}")
    print(f"    q_max = {q_max:.2f} kN/m²  (≤ {inp.q_allow} kN/m²)  {status_q}")
    print(f"    q_min = {q_min:.2f} kN/m²")

    # --- ความดันดินสำหรับออกแบบ (Factored) ---
    qu = (inp.P * 1.4) / A
    print(f"    qu (factored) = {qu:.2f} kN/m²")

    # --- ระยะประสิทธิผล ---
    d = calc_effective_depth(inp)
    print(f"\n{'[3] ระยะประสิทธิผล':}")
    print(f"    d = {d*100:.1f} cm  ({d*1000:.0f} mm)")

    # --- แรงเฉือนทางเดียว ---
    sh1 = check_one_way_shear(inp, B, L, qu, d)
    print(f"\n{'[4] แรงเฉือนทางเดียว (One-Way Shear)':}")
    print(f"    ทิศทาง L:  Vu = {sh1['Vu_L']:.2f} kN,  φVc = {sh1['phiVc_L']:.2f} kN"
          f"  {'✓' if sh1['ok_L'] else '✗'}")
    print(f"    ทิศทาง B:  Vu = {sh1['Vu_B']:.2f} kN,  φVc = {sh1['phiVc_B']:.2f} kN"
          f"  {'✓' if sh1['ok_B'] else '✗'}")

    # --- แรงเจาะ ---
    sh2 = check_punching_shear(inp, B, L, qu, d)
    print(f"\n{'[5] แรงเจาะ (Punching Shear)':}")
    print(f"    bo = {sh2['bo']:.3f} m")
    print(f"    Vu2 = {sh2['Vu2']:.2f} kN,  φVc2 = {sh2['phiVc2']:.2f} kN"
          f"  {'✓' if sh2['ok'] else '✗ (ต้องเพิ่มความหนา)'}")

    # --- เหล็กเสริม ---
    fl = calc_flexure(inp, B, L, qu, d)
    print(f"\n{'[6] เหล็กเสริม (Reinforcement)':}")
    print(f"    ทิศทาง B  →  Mu = {fl['Mu_B']:.2f} kN·m")
    print(f"               As_req = {fl['As_B']*10000:.2f} cm²,  "
          f"As_min = {fl['Asmin_B']*10000:.2f} cm²,  "
          f"As_use = {fl['Asuse_B']*10000:.2f} cm²")
    print(f"    ทิศทาง L  →  Mu = {fl['Mu_L']:.2f} kN·m")
    print(f"               As_req = {fl['As_L']*10000:.2f} cm²,  "
          f"As_min = {fl['Asmin_L']*10000:.2f} cm²,  "
          f"As_use = {fl['Asuse_L']*10000:.2f} cm²")

    # --- สรุป ---
    all_ok = (q_max <= inp.q_allow and sh1['ok_L'] and sh1['ok_B'] and sh2['ok'])
    print(f"\n{sep}")
    print(f"  สรุป: {'✓  การออกแบบผ่านทุกเงื่อนไข' if all_ok else '✗  บางเงื่อนไขไม่ผ่าน — ปรับขนาดหรือความหนา'}")
    print(sep)
    print(f"  ฐานราก {B:.2f} × {L:.2f} m  หนา {inp.t*100:.0f} cm")
    print(f"  f'c = {inp.fc} MPa,  fy = {inp.fy} MPa,  d = {d*100:.1f} cm")
    print(f"  เหล็กทิศ B : {fl['Asuse_B']*10000:.2f} cm²  |  เหล็กทิศ L : {fl['Asuse_L']*10000:.2f} cm²")
    print(sep)


# ─────────────────────────────────────────────
#  5. ตัวอย่างการใช้งาน
# ─────────────────────────────────────────────

if __name__ == "__main__":

    # ตัวอย่างที่ 1: ไม่มีโมเมนต์
    print("\n" + "━" * 60)
    print("  ตัวอย่างที่ 1 — แรงดิ่งอย่างเดียว")
    print("━" * 60)
    inp1 = FootingInput(
        P=800,          # kN
        Mx=0,
        My=0,
        bc=0.40,        # m
        hc=0.40,        # m
        q_allow=150,    # kN/m²
        Df=1.5,         # m
        gamma_soil=18,  # kN/m³
        t=0.50,         # m
        fc=24,          # MPa
        fy=390,         # MPa
        cover=0.075,    # m
    )
    design_footing(inp1)

    # ตัวอย่างที่ 2: มีโมเมนต์สองทิศทาง
    print("\n" + "━" * 60)
    print("  ตัวอย่างที่ 2 — แรงดิ่ง + โมเมนต์")
    print("━" * 60)
    inp2 = FootingInput(
        P=1200,
        Mx=80,
        My=60,
        bc=0.50,
        hc=0.50,
        q_allow=200,
        Df=1.8,
        gamma_soil=18,
        t=0.60,
        fc=28,
        fy=390,
        cover=0.075,
    )
    design_footing(inp2)
