import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from math import erf

# -------------------------------------------
# PAGE CONFIG
# -------------------------------------------
st.set_page_config(
    page_title="Week 10 – Diffusion in Solids (MSE207)",
    layout="wide"
)

st.title("Week 10 – Diffusion in Solids")
st.markdown("### Material Processing Laboratory – Fick's Laws, Arrhenius Law, and Applications")

# ============================================================
# 1. LEARNING OUTCOMES
# ============================================================
st.header("1. Learning Outcomes")

st.markdown("""
After completing **Week 10**, students will be able to:

1. Explain the physical meaning of atomic diffusion in solids.
2. Use **Fick’s First Law** to compute steady-state diffusion flux.
3. Use **Fick’s Second Law** and the **error function solution** for non-steady-state diffusion.
4. Apply the **Arrhenius equation** to calculate the diffusion coefficient as a function of temperature.
5. Estimate diffusion distances and interpret heat treatment processes such as carburizing.
""")

# ============================================================
# 2. THEORY – WITH LATEX
# ============================================================
st.header("2. Theory of Diffusion in Solids")

st.subheader("2.1 Fick's First Law – Steady-State Diffusion")

st.markdown("""
In **steady state**, the concentration profile does not change with time:
""")
st.latex(r"""
\frac{\partial C}{\partial t} = 0
""")

st.markdown("""
Fick's First Law relates the diffusion flux \\(J\\) to the concentration gradient:
""")
st.latex(r"""
J = -D \frac{dC}{dx}
""")
st.markdown("""
- \\(J\\): diffusion flux (kg/m²·s or mol/m²·s)  
- \\(D\\): diffusion coefficient (m²/s)  
- \\(C\\): concentration  
- \\(x\\): position  

The negative sign indicates diffusion from **high** to **low** concentration.
""")

st.subheader("2.2 Fick's Second Law – Non-Steady-State Diffusion")

st.markdown("""
When the concentration changes with time, we use **Fick's Second Law**:
""")
st.latex(r"""
\frac{\partial C}{\partial t} = D \frac{\partial^2 C}{\partial x^2}
""")

st.markdown("""
This is the fundamental equation for **non-steady-state diffusion** in a solid.
It is used to model processes such as **carburizing**, **nitriding**, **sintering**, and **semiconductor doping**.
""")

st.subheader("2.3 Error Function Solution (Semi-Infinite Solid)")

st.markdown("""
For a semi-infinite solid with:

- Initial concentration: \\(C(x,0) = C_0\\)  
- Surface concentration held constant: \\(C(0,t) = C_s\\)  
- Far field: \\(C(\infty, t) = C_0\\)  

The solution of Fick's Second Law is:
""")

st.latex(r"""
C(x,t) = C_s - (C_s - C_0)\,\text{erf}\left( \frac{x}{2\sqrt{D t}} \right)
""")

st.markdown("Or in dimensionless form:")

st.latex(r"""
\frac{C(x,t) - C_0}{C_s - C_0}
= 1 - \text{erf}\left( \frac{x}{2\sqrt{D t}} \right)
""")

st.subheader("2.4 Arrhenius Law for Diffusion Coefficient")

st.markdown("""
The diffusion coefficient is **strongly temperature dependent** and follows an Arrhenius-type relation:
""")
st.latex(r"""
D = D_0 \exp\left(-\frac{Q}{R T}\right)
""")
st.markdown("""
- \\(D_0\\): pre-exponential factor (m²/s)  
- \\(Q\\): activation energy (J/mol)  
- \\(R = 8.314\\ \text{J/mol·K}\\): gas constant  
- \\(T\\): absolute temperature (K)  

Logarithmic form:
""")
st.latex(r"""
\ln D = \ln D_0 - \frac{Q}{R}\frac{1}{T}
""")

st.subheader("2.5 Diffusion Distance (Approximate)")

st.markdown("""
A useful engineering estimate of diffusion distance is:
""")
st.latex(r"""
x_{\text{avg}} \approx \sqrt{D t}
""")
st.markdown("""
This means that **penetration depth increases with the square root of time**.
""")

# ============================================================
# 3. SIMULATION 1 – ARRHENIUS DIFFUSION COEFFICIENT
# ============================================================
st.header("3. Simulation 1 – Arrhenius Law: D vs Temperature")

st.markdown("""
Use the sliders to change activation energy and pre-exponential factor, and see how the diffusion coefficient changes with temperature.
""")

colA, colB = st.columns(2)

with colA:
    D0_input = st.number_input("Pre-exponential factor D₀ (m²/s)", value=1e-5, format="%.2e")
    Q_input_kJ = st.slider("Activation energy Q (kJ/mol)", 50.0, 300.0, 150.0)
    Q_input = Q_input_kJ * 1000.0  # convert to J/mol

with colB:
    T_min = st.slider("Minimum Temperature (°C)", 300, 900, 500)
    T_max = st.slider("Maximum Temperature (°C)", 600, 1400, 1000)
    n_points = 200

R = 8.314
T_K = np.linspace(T_min + 273.15, T_max + 273.15, n_points)

# Compute D(T)
D_T = D0_input * np.exp(-Q_input / (R * T_K))

fig1, ax1 = plt.subplots(figsize=(7, 4))
ax1.semilogy(T_K, D_T)
ax1.set_xlabel("Temperature (K)")
ax1.set_ylabel("Diffusion Coefficient D (m²/s)")
ax1.set_title("Arrhenius Diffusion Coefficient vs Temperature")
st.pyplot(fig1)

st.markdown("""
You can see that diffusion coefficient increases **exponentially** with temperature.
Even a moderate increase in temperature can dramatically accelerate diffusion.
""")

# ============================================================
# 4. SIMULATION 2 – NON-STEADY-STATE DIFFUSION PROFILE
# ============================================================
st.header("4. Simulation 2 – Non-Steady-State Diffusion Profile (Error Function Solution)")

st.markdown("""
We now simulate the concentration profile \\(C(x,t)\\) in a semi-infinite solid using the error function solution of Fick's Second Law.
""")

col1, col2 = st.columns(2)

with col1:
    C0 = st.slider("Initial concentration C₀ (wt.%)", 0.0, 2.0, 0.2, 0.1)
    Cs = st.slider("Surface concentration Cₛ (wt.%)", 0.1, 2.0, 1.0, 0.1)
    D_ns = st.number_input("Diffusion coefficient D (m²/s)", value=1e-11, format="%.1e")

with col2:
    t_hours = st.slider("Diffusion time (hours)", 0.5, 10.0, 4.0, 0.5)
    t_ns = t_hours * 3600.0
    max_depth_mm = st.slider("Maximum depth (mm)", 0.2, 5.0, 2.0, 0.1)

# Depth axis (m)
x_m = np.linspace(0, max_depth_mm / 1000.0, 300)

# Error function solution: C(x,t) = Cs - (Cs - C0)*erf(x / (2 sqrt(D t)))
if D_ns > 0 and t_ns > 0:
    denom = 2.0 * np.sqrt(D_ns * t_ns)
    z = x_m / denom
    erf_vec = np.vectorize(erf)
    C_xt = Cs - (Cs - C0) * erf_vec(z)
else:
    C_xt = np.full_like(x_m, C0)

fig2, ax2 = plt.subplots(figsize=(7, 4))
ax2.plot(x_m * 1000.0, C_xt)
ax2.set_xlabel("Depth x (mm)")
ax2.set_ylabel("Concentration C (wt.%)")
ax2.set_title("Non-Steady-State Diffusion Profile")
st.pyplot(fig2)

st.markdown(f"""
For the selected parameters:

- Time: **{t_hours:.2f} h**  
- Max depth: **{max_depth_mm:.2f} mm**  
- Diffusion coefficient: **{D_ns:.1e} m²/s**

The surface concentration is fixed at **Cₛ = {Cs:.2f} wt.%**,  
and the initial bulk concentration is **C₀ = {C0:.2f} wt.%**.
""")

# ============================================================
# 5. SIMULATION 3 – DIFFUSION DISTANCE ESTIMATE
# ============================================================
st.header("5. Simulation 3 – Diffusion Distance Estimate x ≈ √(Dt)")

st.markdown("""
This module estimates the **average diffusion distance** using:
""")
st.latex(r"""
x_{\text{avg}} \approx \sqrt{D t}
""")

col3, col4 = st.columns(2)

with col3:
    D_est = st.number_input("Diffusion coefficient D (m²/s)", value=1e-12, format="%.1e", key="D_est")
    t_est_hours = st.slider("Time (hours)", 0.1, 50.0, 5.0, 0.1, key="t_est_h")
    t_est = t_est_hours * 3600.0

with col4:
    st.markdown("### Estimated Diffusion Distance")

if D_est > 0 and t_est > 0:
    x_avg_m = np.sqrt(D_est * t_est)
    x_avg_mm = x_avg_m * 1000.0
    st.latex(rf"x_{{avg}} = \sqrt{{D t}} = {x_avg_m:.3e}\ \text{{m}} \approx {x_avg_mm:.3f}\ \text{{mm}}")
else:
    st.warning("Please use positive values for D and t.")

st.markdown("""
This simple estimate is very useful when designing **heat treatment durations** and predicting how deep atoms can diffuse into the material.
""")

# ============================================================
# 6. WORKED EXAMPLES (DETAILED)
# ============================================================
st.header("6. Worked Examples")

# Example 1
st.subheader("Example 1 – Steady-State Diffusion Flux through a Plate")

st.markdown("""
A metal plate has a thickness of **L = 2 mm**.  
The concentration at the left surface is:

- \\(C_1 = 5\\ \\text{kg/m}^3\\)

and at the right surface:

- \\(C_2 = 1\\ \\text{kg/m}^3\\)

The diffusion coefficient is:

- \\(D = 2.0 \\times 10^{-10}\\ \\text{m}^2/\\text{s}\\)

(a) Calculate the diffusion flux \\(J\\).  
(b) If the plate area is **A = 0.01 m²**, find the total mass that diffuses through in **1 hour**.
""")

st.markdown("**Solution (a) – Flux calculation**")

st.latex(r"""
\frac{dC}{dx} \approx \frac{C_2 - C_1}{L}
= \frac{1 - 5}{0.002}
= -2000\ \text{kg/m}^4
""")

st.latex(r"""
J = -D \frac{dC}{dx}
= -(2.0 \times 10^{-10})(-2000)
= 4.0 \times 10^{-7}\ \text{kg}/(\text{m}^2\cdot\text{s})
""")

st.markdown("**Solution (b) – Total mass**")

st.latex(r"""
m = J A t
""")

st.latex(r"""
m = (4.0 \times 10^{-7})(0.01)(3600)
= 1.44 \times 10^{-5}\ \text{kg}
\approx 0.014\ \text{g}
""")

st.markdown("So, about **0.014 g** of material diffuses through the plate in 1 hour.")

# Example 2
st.subheader("Example 2 – Non-Steady-State Diffusion (Carburizing-like Case)")

st.markdown("""
A steel is carburized at high temperature.  
Initially, the carbon concentration everywhere in the steel is:

- \\(C_0 = 0.2\\ \\text{wt.% C}\\)

The surface concentration is suddenly raised and held at:

- \\(C_s = 1.0\\ \\text{wt.% C}\\)

The diffusion coefficient at the carburizing temperature is:

- \\(D = 1.0 \\times 10^{-11}\\ \\text{m}^2/\\text{s}\\)

The process time is:

- \\(t = 4\\ \\text{h} = 14400\\ \\text{s}\\)

Find the carbon concentration at **x = 0.5 mm** below the surface.
""")

st.markdown("**Solution**")

st.latex(r"""
C(x,t) = C_s - (C_s - C_0)\,\text{erf}\left( \frac{x}{2\sqrt{D t}} \right)
""")

st.markdown("Compute \\( \\sqrt{D t} \\):")

st.latex(r"""
D t = (1.0 \times 10^{-11})(14400) = 1.44 \times 10^{-7}\ \text{m}^2
""")

st.latex(r"""
\sqrt{D t} \approx 3.8 \times 10^{-4}\ \text{m}
""")

st.latex(r"""
2\sqrt{D t} \approx 7.6 \times 10^{-4}\ \text{m}
""")

st.markdown("Dimensionless variable:")

st.latex(r"""
z = \frac{x}{2\sqrt{D t}} = \frac{0.0005}{7.6 \times 10^{-4}} \approx 0.66
""")

st.markdown("Using \\( \\text{erf}(0.66) \\approx 0.63 \\):")

st.latex(r"""
C(x,t) = 1.0 - (1.0 - 0.2)\times 0.63
= 1.0 - 0.8 \times 0.63
= 1.0 - 0.504 = 0.496\ \text{wt.\% C}
""")

st.markdown("So, the carbon concentration at 0.5 mm is approximately **0.50 wt.% C**.")

# Example 3
st.subheader("Example 3 – Arrhenius Law: Q, D₀, and D at a New Temperature")

st.markdown("""
The diffusion coefficient of an element in a metal is measured at two temperatures:

- At \\( T_1 = 800^\circ C = 1073\\ K \\):  
  \\( D_1 = 2.0 \\times 10^{-13}\\ \\text{m}^2/\\text{s} \\)

- At \\( T_2 = 1000^\circ C = 1273\\ K \\):  
  \\( D_2 = 3.0 \\times 10^{-12}\\ \\text{m}^2/\\text{s} \\)

(a) Determine the activation energy \\(Q\\).  
(b) Determine the pre-exponential factor \\(D_0\\).  
(c) Estimate \\(D\\) at \\( T_3 = 900^\circ C = 1173\\ K \\).
""")

st.markdown("**Solution (a) – Activation energy Q**")

st.latex(r"""
\ln\left(\frac{D_2}{D_1}\right)
= -\frac{Q}{R}\left(\frac{1}{T_2} - \frac{1}{T_1}\right)
""")

st.latex(r"""
\frac{D_2}{D_1} = \frac{3.0 \times 10^{-12}}{2.0 \times 10^{-13}} = 15
""")

st.latex(r"""
\ln 15 \approx 2.71
""")

st.latex(r"""
\frac{1}{T_2} - \frac{1}{T_1}
\approx 7.86\times 10^{-4} - 9.32\times 10^{-4}
= -1.46\times 10^{-4}\ \text{K}^{-1}
""")

st.latex(r"""
2.71 = \frac{Q}{R}(1.46\times 10^{-4})
\Rightarrow \frac{Q}{R} \approx 1.86\times 10^{4}
""")

st.latex(r"""
Q = R \cdot \frac{Q}{R}
\approx 8.314 \times 1.86\times 10^{4}
\approx 1.5 \times 10^{5}\ \text{J/mol}
= 150\ \text{kJ/mol}
""")

st.markdown("**Solution (b) – Pre-exponential factor D₀**")

st.latex(r"""
D_1 = D_0 \exp\left(-\frac{Q}{R T_1}\right)
\Rightarrow D_0 = D_1 \exp\left(\frac{Q}{R T_1}\right)
""")

st.latex(r"""
\frac{Q}{R T_1} \approx 17.3
\Rightarrow \exp(17.3) \approx 3.3 \times 10^{7}
""")

st.latex(r"""
D_0 \approx (2.0\times 10^{-13})(3.3\times 10^{7})
\approx 6.6\times 10^{-6}\ \text{m}^2/\text{s}
""")

st.markdown("**Solution (c) – D at 900°C (1173 K)**")

st.latex(r"""
D_3 = D_0 \exp\left(-\frac{Q}{R T_3}\right)
""")

st.latex(r"""
\frac{Q}{R T_3} \approx 15.8
\Rightarrow \exp(-15.8) \approx 1.35\times 10^{-7}
""")

st.latex(r"""
D_3 \approx 6.6\times 10^{-6} \times 1.35\times 10^{-7}
\approx 8.9\times 10^{-13}\ \text{m}^2/\text{s}
""")

st.markdown("""
So at **900°C**, the diffusion coefficient is approximately  
\\( D(900^\circ C) \approx 9 \times 10^{-13}\ \text{m}^2/\text{s} \\).
""")

# ============================================================
# 7. KEY EQUATIONS
# ============================================================
st.header("7. Key Equations – Week 10")

st.latex(r"""
J = -D \frac{dC}{dx}
""")
st.latex(r"""
\frac{\partial C}{\partial t} = D \frac{\partial^2 C}{\partial x^2}
""")
st.latex(r"""
C(x,t) = C_s - (C_s - C_0)\,\text{erf}\left( \frac{x}{2\sqrt{Dt}} \right)
""")
st.latex(r"""
D = D_0 \exp\left(-\frac{Q}{RT}\right)
""")
st.latex(r"""
x_{\text{avg}} \approx \sqrt{D t}
""")

# ============================================================
# 8. QUIZ
# ============================================================
st.header("8. Quick Quiz – Check Your Understanding")

q1 = st.radio(
    "1) Which law describes non-steady-state diffusion?",
    [
        "Fick's First Law",
        "Fick's Second Law",
        "Hooke's Law"
    ]
)

if q1 == "Fick's Second Law":
    st.success("Correct – Fick's Second Law governs non-steady-state diffusion.")
elif q1 != "":
    st.error("Not correct. Non-steady behavior is described by Fick's Second Law.")

q2 = st.radio(
    "2) How does diffusion coefficient D depend on temperature in metals?",
    [
        "Linearly with T",
        "Inversely with T",
        "Exponentially with 1/T (Arrhenius behavior)"
    ]
)

if q2 == "Exponentially with 1/T (Arrhenius behavior)":
    st.success("Correct – D follows an Arrhenius-type exponential dependence.")
elif q2 != "":
    st.error("Not correct. D follows an Arrhenius-type exponential dependence on 1/T.")

q3 = st.radio(
    "3) The approximate diffusion distance after time t is proportional to:",
    [
        "t",
        "√t",
        "1/t"
    ]
)

if q3 == "√t":
    st.success("Correct – diffusion distance grows with the square root of time.")
elif q3 != "":
    st.error("Not correct. It scales with the square root of time (√t).")

# ============================================================
# 9. SUMMARY
# ============================================================
st.header("9. Summary – Week 10 Conclusions")

st.markdown("""
- Diffusion in solids is driven by **concentration gradients** and is thermally activated.  
- **Fick's First Law** describes steady-state flux under constant gradients.  
- **Fick's Second Law** and the **error function solution** describe non-steady diffusion in semi-infinite solids.  
- The diffusion coefficient **increases exponentially** with temperature (Arrhenius behavior).  
- Diffusion depth grows roughly as **√(Dt)**, which is crucial for designing **heat treatments** (carburizing, nitriding, doping, etc.).
""")
