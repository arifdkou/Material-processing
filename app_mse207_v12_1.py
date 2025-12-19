import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Week 12 – Precipitation Hardening (MSE207)", layout="wide")

st.title("Week 12 – Precipitation Hardening (Age Hardening)")
st.markdown("### Material Processing Laboratory – Kinetics, Coarsening, and Strengthening")

# -----------------------------
# THEORY
# -----------------------------
st.header("1. Theory (with equations)")

st.subheader("1.1 Precipitation kinetics (JMAK / Avrami)")
st.latex(r"X(t)=1-\exp\left[-(k\,t)^n\right]")
st.markdown("""
- **X(t)**: precipitated (transformed) fraction  
- **k**: rate constant (temperature dependent)  
- **n**: Avrami exponent (mechanism-dependent)  
""")

st.subheader("1.2 Arrhenius dependence of rate constant")
st.latex(r"k(T)=k_0\exp\left(-\frac{Q}{RT}\right)")
st.markdown("""
- **Q**: activation energy (J/mol)  
- **R = 8.314 J/(mol·K)**  
- **T**: absolute temperature (K)  
""")

st.subheader("1.3 Coarsening (Ostwald ripening, LSW)")
st.latex(r"\bar{r}^3-\bar{r}_0^3 = K t")
st.markdown("""
- **r̄**: average precipitate radius at time t  
- **K**: coarsening rate constant  
Coarsening typically causes **overaging** (strength decreases).
""")

st.subheader("1.4 Orowan strengthening (simplified)")
st.latex(r"\Delta \tau \approx \frac{G b}{\lambda}")
st.latex(r"\Delta \sigma \approx M\,\frac{G b}{\lambda}")
st.markdown("""
- **G**: shear modulus  
- **b**: Burgers vector  
- **λ**: obstacle spacing  
- **M**: Taylor factor  
Smaller spacing → higher strengthening.
""")

# -----------------------------
# SIMULATION 1: AVRAMI X(t)
# -----------------------------
st.header("2. Simulation 1 – Precipitated fraction X(t)")

c1, c2 = st.columns(2)
with c1:
    k = st.number_input("k (1/s)", value=2.0e-4, format="%.2e")
    n = st.slider("n (Avrami exponent)", 1.0, 4.0, 2.0, 0.1)
with c2:
    t_max = st.slider("t_max (s)", 100, 20000, 5000)

t = np.linspace(0, t_max, 600)
X = 1 - np.exp(-(k * t) ** n)

fig1, ax1 = plt.subplots()
ax1.plot(t, X, linewidth=2)
ax1.set_xlabel("Time t (s)")
ax1.set_ylabel("Precipitated fraction X(t)")
ax1.set_title("JMAK / Avrami kinetics")
ax1.set_ylim(0, 1.05)
st.pyplot(fig1)

# -----------------------------
# SIMULATION 2: COARSENING r(t)
# -----------------------------
st.header("3. Simulation 2 – Coarsening (r̄³ − r̄₀³ = Kt)")

c3, c4 = st.columns(2)
with c3:
    r0_nm = st.slider("Initial radius r̄₀ (nm)", 1.0, 100.0, 10.0, 1.0)
    K = st.number_input("Coarsening constant K (m^3/s)", value=2.0e-25, format="%.2e")
with c4:
    t2_max = st.slider("t_max for coarsening (s)", 10, 20000, 2000)

r0 = r0_nm * 1e-9
t2 = np.linspace(0, t2_max, 600)
r = np.cbrt(r0**3 + K * t2)

fig2, ax2 = plt.subplots()
ax2.plot(t2, r * 1e9, linewidth=2)
ax2.set_xlabel("Time t (s)")
ax2.set_ylabel("Average radius r̄ (nm)")
ax2.set_title("Coarsening: average precipitate radius vs time")
st.pyplot(fig2)

# -----------------------------
# SIMULATION 3: OROWAN STRENGTHENING
# -----------------------------
st.header("4. Simulation 3 – Orowan strengthening vs spacing")

c5, c6 = st.columns(2)
with c5:
    G_GPa = st.slider("Shear modulus G (GPa)", 5.0, 100.0, 26.0, 1.0)
    b_nm = st.slider("Burgers vector b (nm)", 0.15, 0.40, 0.286, 0.001)
with c6:
    M = st.slider("Taylor factor M", 2.0, 3.5, 3.0, 0.1)
    lam_min = st.slider("Min spacing λ_min (nm)", 10, 200, 20)
    lam_max = st.slider("Max spacing λ_max (nm)", 50, 1000, 300)

lam = np.linspace(lam_min, lam_max, 400) * 1e-9
G = G_GPa * 1e9
b = b_nm * 1e-9

d_tau = (G * b) / lam
d_sigma = M * d_tau

fig3, ax3 = plt.subplots()
ax3.plot(lam * 1e9, d_sigma / 1e6, linewidth=2)
ax3.set_xlabel("Spacing λ (nm)")
ax3.set_ylabel("Strength increment Δσ (MPa)")
ax3.set_title("Orowan strengthening (simplified)")
st.pyplot(fig3)

# -----------------------------
# WORKED EXAMPLES
# -----------------------------
st.header("5. Worked Examples (step-by-step)")

st.subheader("Example 1 – Avrami fraction")
st.latex(r"X(t)=1-\exp\left[-(k t)^n\right]")
st.markdown("Use: **k = 2.0×10⁻⁴ 1/s**, **n = 2**, **t = 1800 s**")
st.latex(r"kt=(2.0\times10^{-4})(1800)=0.36")
st.latex(r"(kt)^n=(0.36)^2=0.1296")
st.latex(r"X=1-e^{-0.1296}\approx 1-0.878=0.122")
st.markdown(r"✅ **Result:**  \(\boxed{X\approx 0.12}\)")

st.subheader("Example 2 – Coarsening time to reach a target radius")
st.latex(r"\bar{r}^3-\bar{r}_0^3=Kt \Rightarrow t=\frac{\bar{r}^3-\bar{r}_0^3}{K}")
st.markdown("Use: **r̄₀ = 10 nm**, **r̄ = 25 nm**, **K = 2.0×10⁻²⁵ m³/s**")
st.latex(r"t \approx 73\ \text{s}")
st.markdown(r"✅ **Result:**  \(\boxed{t\approx 73\ \text{s}}\)")

st.subheader("Example 3 – Orowan strengthening")
st.latex(r"\Delta\sigma \approx M\frac{Gb}{\lambda}")
st.markdown("Use: **G = 26 GPa**, **b = 0.286 nm**, **λ = 80 nm**, **M = 3**")
st.latex(r"\Delta\sigma \approx 2.8\times10^8\ \text{Pa}\approx 280\ \text{MPa}")
st.markdown(r"✅ **Result:**  \(\boxed{\Delta\sigma\approx 280\ \text{MPa}}\)")

# -----------------------------
# SUMMARY
# -----------------------------
st.header("6. Summary")
st.markdown("""
- Precipitation hardening increases strength by forming fine precipitates.
- Kinetics can be modeled by JMAK (Avrami): **X(t)**
- Long aging causes coarsening: **r̄³ − r̄₀³ = Kt**
- Strengthening often scales with inverse spacing: **Δσ ∝ 1/λ**
""")
