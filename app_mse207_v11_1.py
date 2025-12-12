import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from math import erf, exp, log

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Week 11 – Phase Transformations (MSE207)",
    layout="wide"
)

st.title("Week 11 – Phase Transformations in Metals")
st.markdown("### Material Processing Laboratory – TTT, CCT, and Transformation Kinetics")

# =================================================
# 1. LEARNING OUTCOMES
# =================================================
st.header("1. Learning Outcomes")

st.markdown("""
After completing **Week 11**, students will be able to:

- Understand phase transformation kinetics in metals  
- Interpret **TTT** and **CCT** diagrams  
- Apply the **Avrami (JMAK) equation** for diffusion-controlled transformations  
- Estimate **martensite fraction** as a function of temperature  
- Predict final microstructure from cooling paths  
""")

# =================================================
# 2. THEORY & EQUATIONS
# =================================================
st.header("2. Theory and Governing Equations")

st.subheader("2.1 Thermodynamic Driving Force")
st.latex(r"\Delta G = G_{\text{final}} - G_{\text{initial}} < 0")
st.markdown("""
A phase transformation is thermodynamically possible if the Gibbs free energy decreases.
However, kinetics determines **how fast** the transformation occurs.
""")

st.subheader("2.2 Avrami (JMAK) Equation – Diffusion-Controlled Transformations")
st.latex(r"X(t) = 1 - \exp(-k t^n)")
st.markdown("""
- \(X(t)\): fraction transformed  
- \(k\): rate constant (temperature dependent)  
- \(n\): Avrami exponent (nucleation + growth mechanism)  
""")

st.subheader("2.3 Martensitic Transformation (Diffusionless)")
st.latex(r"f_M = 1 - \exp[-\alpha (M_s - T)]")
st.markdown("""
- \(M_s\): martensite start temperature  
- \(T\): current temperature  
Martensite formation depends mainly on **temperature** rather than time.
""")

# =================================================
# 3. SIMULATION 1 – AVRAMI TRANSFORMATION
# =================================================
st.header("3. Simulation 1 – Avrami Transformation Kinetics")

st.markdown("Fraction transformed as a function of time at constant temperature.")

col1, col2 = st.columns(2)
with col1:
    k = st.number_input("Rate constant k (s⁻ⁿ)", value=2.5e-4, format="%.2e")
    n = st.slider("Avrami exponent n", 1.0, 4.0, 2.0, 0.1)
with col2:
    t_max = st.slider("Maximum time (s)", 100, 5000, 2000)

t = np.linspace(0, t_max, 400)
X = 1 - np.exp(-k * t**n)

fig1, ax1 = plt.subplots()
ax1.plot(t, X, linewidth=2)
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Transformed Fraction X(t)")
ax1.set_title("Avrami Transformation Kinetics")
ax1.set_ylim(0, 1.05)
st.pyplot(fig1)

# =================================================
# 4. SIMULATION 2 – MARTENSITE FRACTION
# =================================================
st.header("4. Simulation 2 – Martensite Fraction vs Temperature")

st.markdown("Martensitic transformation below the martensite start temperature.")

col3, col4 = st.columns(2)
with col3:
    Ms = st.slider("Martensite start temperature Ms (°C)", 200, 450, 350)
    alpha = st.slider("Material constant α (1/°C)", 0.005, 0.03, 0.011, 0.001)
with col4:
    Tmin = st.slider("Minimum temperature (°C)", -50, 200, 0)

T = np.linspace(Tmin, Ms, 300)
fM = 1 - np.exp(-alpha * (Ms - T))

fig2, ax2 = plt.subplots()
ax2.plot(T, fM, linewidth=2)
ax2.set_xlabel("Temperature (°C)")
ax2.set_ylabel("Martensite Fraction")
ax2.set_title("Martensite Fraction vs Temperature")
ax2.set_ylim(0, 1.05)
st.pyplot(fig2)

# =================================================
# 5. SIMULATION 3 – SIMPLIFIED TTT + COOLING PATH
# =================================================
st.header("5. Simulation 3 – Simplified TTT Diagram and Cooling Curve")

st.markdown("""
A conceptual TTT diagram with a continuous cooling curve.
This helps visualize how the cooling path determines final microstructure.
""")

cooling_rate = st.slider("Cooling rate (°C/s)", 0.1, 50.0, 5.0)

# Conceptual "nose" curve
time_ttt = np.logspace(-1, 4, 450)
T_nose = 650 - 120 * np.exp(-((np.log10(time_ttt) - 1.2) ** 2) / (2 * (0.55 ** 2)))

# Cooling curve (start 900°C)
t_cool = np.linspace(0, 2000, 450)
T_cool = 900 - cooling_rate * t_cool

fig3, ax3 = plt.subplots()
ax3.semilogx(time_ttt, T_nose, label="TTT nose (conceptual)")
ax3.plot(t_cool, T_cool, linewidth=2, label="Cooling curve")
ax3.axhline(Ms, linestyle="--", label="Ms")
ax3.set_xlabel("Time (s) [log scale for TTT nose]")
ax3.set_ylabel("Temperature (°C)")
ax3.set_ylim(0, 950)
ax3.set_title("Simplified TTT Diagram with Cooling Path")
ax3.legend()
st.pyplot(fig3)

# Quick qualitative classification
# If cooling curve stays above the nose until it reaches Ms -> mostly martensite
# We'll check intersection approximately:
nose_interp = np.interp(np.clip(t_cool, time_ttt.min(), time_ttt.max()), time_ttt, T_nose)
intersects = np.any(T_cool <= nose_interp)

if not intersects:
    st.success("Cooling path avoids the TTT nose → microstructure tends to be mostly **Martensite**.")
else:
    st.warning("Cooling path intersects the TTT nose → microstructure tends to be **Pearlite/Bainite + Martensite**.")

# =================================================
# 6. WORKED EXAMPLES (3 DETAILED)
# =================================================
st.header("6. Worked Examples (Step-by-Step)")

# -------------------------
# Example 1: Avrami fraction
# -------------------------
st.subheader("Example 1 — Avrami Equation: Fraction Transformed at a Given Time")

st.markdown("""
A steel transforms isothermally at a fixed temperature. The Avrami parameters are:

- \(k = 2.5 \\times 10^{-4}\\ \\text{s}^{-n}\)
- \(n = 2\)

Find the transformed fraction after:

- \(t = 1200\\ \\text{s}\)
""")

st.markdown("**Solution**")

st.latex(r"X(t) = 1 - \exp(-k t^n)")
st.latex(r"k t^n = (2.5\times10^{-4})(1200)^2")
st.latex(r"(1200)^2 = 1.44\times 10^{6}")
st.latex(r"k t^n = 2.5\times10^{-4} \times 1.44\times10^{6} = 360")
st.latex(r"X = 1 - \exp(-360) \approx 1 - 0 \approx 1")

st.markdown(r"**Answer:**  \(\boxed{X \approx 1}\) (almost complete transformation).")

# -------------------------
# Example 2: Martensite fraction
# -------------------------
st.subheader("Example 2 — Martensite Fraction Below Ms")

st.markdown("""
For a steel:

- \(M_s = 350^\circ C\)
- \(\alpha = 0.011\ ^\circ C^{-1}\)

Find the martensite fraction at:

- \(T = 250^\circ C\)
""")

st.markdown("**Solution**")

st.latex(r"f_M = 1 - \exp[-\alpha (M_s - T)]")
st.latex(r"M_s - T = 350 - 250 = 100^\circ C")
st.latex(r"f_M = 1 - \exp[-0.011 \times 100] = 1 - \exp(-1.1)")
st.latex(r"\exp(-1.1) \approx 0.332")
st.latex(r"f_M \approx 1 - 0.332 = 0.668")

st.markdown(r"**Answer:**  \(\boxed{f_M \approx 0.67}\) (about 67% martensite).")

# -------------------------
# Example 3: Cooling path + Avrami estimate
# -------------------------
st.subheader("Example 3 — Cooling Path: Predicting Microstructure + Quantitative Estimate")

st.markdown("""
A steel is austenitized at \(900^\circ C\) and then cooled continuously.

Assume (simplified model):

- The cooling curve intersects the transformation region at \(T = 600^\circ C\).  
- Once it enters this region, the diffusion-controlled transformation follows Avrami kinetics:
  \[
  X(t) = 1 - \exp(-k t^n)
  \]
- Use \(k = 3.0 \times 10^{-4}\ \\text{s}^{-n}\), \(n = 2\).
- The material stays in the diffusion-transformation temperature range for \(t = 300\ \\text{s}\) before reaching \(M_s\).

Tasks:
1) Estimate the fraction transformed by diffusion \(X\).  
2) Predict the qualitative final microstructure if the remaining austenite transforms to martensite below \(M_s\).
""")

st.markdown("**Solution (1) – Diffusion-controlled fraction using Avrami**")
st.latex(r"X = 1 - \exp(-k t^n)")
st.latex(r"k t^n = (3.0\times10^{-4})(300)^2")
st.latex(r"(300)^2 = 9.0\times10^{4}")
st.latex(r"k t^n = 3.0\times10^{-4}\times 9.0\times10^{4} = 27")
st.latex(r"X = 1 - \exp(-27)")

st.markdown("Since \( \exp(-27) \approx 1.88\times10^{-12} \) is essentially zero:")
st.latex(r"X \approx 1")

st.markdown("**So nearly all austenite would transform by diffusion (pearlite/bainite) before reaching \(M_s\).**")

st.markdown("**Solution (2) – Microstructure**")
st.markdown("""
- If \(X \approx 1\), almost no austenite remains for martensite.
- Therefore the final microstructure is dominated by **diffusion products** (pearlite/bainite depending on temperature range).
""")

st.markdown(r"**Answer:**  \(\boxed{\text{Mostly Pearlite/Bainite (very little Martensite)}}\)")

# =================================================
# 7. KEY EQUATIONS SUMMARY
# =================================================
st.header("7. Key Equations – Week 11 Summary")

st.latex(r"\Delta G < 0")
st.latex(r"X(t) = 1 - \exp(-k t^n)")
st.latex(r"f_M = 1 - \exp[-\alpha (M_s - T)]")

# =================================================
# 8. QUIZ
# =================================================
st.header("8. Quick Quiz")

q1 = st.radio("1) Which equation models diffusion-controlled transformation kinetics?",
              ["Martensite equation", "Avrami (JMAK) equation", "Hooke's law"])
if q1 == "Avrami (JMAK) equation":
    st.success("Correct.")
elif q1 != "":
    st.error("Incorrect.")

q2 = st.radio("2) Martensite formation is mainly controlled by:",
              ["Time", "Temperature", "Grain size"])
if q2 == "Temperature":
    st.success("Correct.")
elif q2 != "":
    st.error("Incorrect.")

q3 = st.radio("3) In a TTT diagram, the 'nose' represents:",
              ["Maximum hardness", "Fastest transformation region", "Melting point"])
if q3 == "Fastest transformation region":
    st.success("Correct.")
elif q3 != "":
    st.error("Incorrect.")

# =================================================
# 9. SUMMARY
# =================================================
st.header("9. Final Remarks")

st.markdown("""
- **TTT diagrams** describe **isothermal** transformation behavior.
- **CCT diagrams** are more relevant to real processes with continuous cooling.
- The **Avrami equation** quantifies diffusion-controlled kinetics.
- Martensite is **diffusionless** and depends primarily on temperature below \(M_s\).
- Cooling path determines whether you get **pearlite**, **bainite**, **martensite**, or mixtures.
""")
