import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Week 8 – Material Processing Laboratory")
st.markdown("### Heat Transfer, Cooling Curves, and Solidification of Metals")

# ============================================================
# 1. LEARNING OUTCOMES
# ============================================================
st.header("1. Learning Outcomes")

st.markdown("""
After completing this module, students will be able to:

1. Explain heat transfer mechanisms in metal processing (conduction, convection, radiation).
2. Interpret cooling curves during solidification of pure metals and alloys.
3. Simulate cooling behavior using Python.
4. Analyze effects of thermal conductivity, density, and heat capacity.
5. Solve industrial solidification problems (casting, melt processing).
""")

# ============================================================
# 2. THEORY
# ============================================================
st.header("2. Theory of Heat Transfer in Metal Processing")

# Subsection 2.1
st.subheader("2.1 Fourier’s Law of Heat Conduction")

st.latex(r"""
q = -k A \frac{dT}{dx}
""")

st.markdown("""
- \(q\): heat transfer rate (W)  
- \(k\): thermal conductivity (W/m·K)  
- \(A\): cross-sectional area  
- Metals have **high thermal conductivity**, enabling fast heat flow.
""")

# Subsection 2.2
st.subheader("2.2 Newton’s Law of Cooling")

st.latex(r"""
q = h A (T_s - T_\infty)
""")

st.markdown("""
- \(h\): convective heat transfer coefficient  
- \(T_s\): surface temperature  
- \(T_\infty\): ambient temperature  
""")

# Subsection 2.3
st.subheader("2.3 Cooling Curve of Pure Metals")

st.markdown("Pure metals have a clear **thermal arrest plateau** during solidification.")

st.latex(r"""
T = T_\text{melt} = \text{constant during solidification}
""")

st.markdown("""
During phase change, temperature remains constant because **latent heat** is released.
""")

# Subsection 2.4
st.subheader("2.4 Solidification Time – Chvorinov’s Rule")

st.latex(r"""
t_s = C_m \left( \frac{V}{A} \right)^n
""")

st.markdown("""
- \( t_s \): solidification time  
- \( V/A \): volume-to-surface-area ratio  
- \( n \approx 2 \) for most castings  
- Large castings solidify more slowly.
""")

# ============================================================
# 3. INTERACTIVE SIMULATION
# ============================================================
st.header("3. Interactive Simulation: Cooling Curve of a Metal")

st.markdown("Use the sliders to change physical parameters and observe the cooling behavior.")

T_initial = st.slider("Initial Temperature (°C)", 200, 1200, 900)
T_melt = st.slider("Melting Temperature (°C)", 400, 1200, 660)
k = st.slider("Thermal Conductivity k (W/m·K)", 10.0, 300.0, 205.0)
rho = st.slider("Density ρ (kg/m³)", 1000, 9000, 2700)
Cp = st.slider("Heat Capacity Cp (J/kg·K)", 200, 1200, 900)
h = st.slider("Convective Coefficient h (W/m²K)", 5.0, 200.0, 50.0)

# Time axis
t = np.linspace(0, 600, 600)
T_env = 25.0

# Simple Newtonian cooling model
T = T_env + (T_initial - T_env) * np.exp(-h * t / (rho * Cp))

# Artificial solidification plateau
plateau_start = int(200)
plateau_end = int(350)
if plateau_end <= len(T):
    T[plateau_start:plateau_end] = T_melt

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(t, T, linewidth=2)
ax.axhline(T_melt, linestyle='--')
ax.set_xlabel("Time (s)")
ax.set_ylabel("Temperature (°C)")
ax.set_title("Cooling Curve with Solidification Plateau")
st.pyplot(fig)

# ============================================================
# 4. SOLVED EXAMPLES
# ============================================================
st.header("4. Solved Examples")

# Example 1
st.subheader("Example 1 – Heat Conduction in Aluminum Plate")
st.markdown("""
A 10 cm thick Al plate has surfaces at 200°C and 30°C.  
Compute heat flux.
""")
st.latex(r"""
q = -k \frac{dT}{dx}
""")
st.latex(r"""
q = -205 \frac{200 - 30}{0.10} = -348500\ \text{W/m}^2
""")

# Example 2
st.subheader("Example 2 – Cooling Rate of Molten Metal")
st.markdown("""A molten aluminum sample cools from 900°C to 25°C with \(h = 40\ \text{W/m}^2\text{K}\).""")
st.latex(r"""
T(t) = T_\infty + (T_0 - T_\infty)e^{-ht/(\rho C_p)}
""")

# Example 3
st.subheader("Example 3 – Chvorinov’s Rule")
st.markdown("""
A casting has V/A = 0.5.  
Find solidification time if V/A doubles.
""")
st.latex(r"""
t_s \propto \left(\frac{V}{A}\right)^2
""")
st.latex(r"""
\frac{t_2}{t_1} = \left(\frac{1.0}{0.5}\right)^2 = 4
""")

# Example 4
st.subheader("Example 4 – Latent Heat Release")
st.markdown("""
Aluminum latent heat: 397 kJ/kg.  
Mass = 2 kg.  
Find the total heat released during solidification.
""")
st.latex(r"""
Q = m L = 2 \times 397 = 794\ \text{kJ}
""")

# Example 5
st.subheader("Example 5 – Cooling Curve Interpretation")
st.markdown("""
A pure metal shows a flat line at 660°C for 120 s.  
This means **latent heat** is being released during solidification and the material is undergoing a phase change from liquid to solid.
""")

# ============================================================
# 5. QUIZ
# ============================================================
st.header("5. Quiz")

q1 = st.radio("1) Temperature remains constant during:", 
              ["Conduction", "Convection", "Radiation", "Solidification of pure metals"])
if q1 == "Solidification of pure metals":
    st.success("Correct!")
else:
    st.error("Incorrect.")

q2 = st.radio("2) Which law describes conduction?", 
              ["Newton’s law", "Fourier’s law", "Hooke’s law"])
if q2 == "Fourier’s law":
    st.success("Correct!")
else:
    st.error("Try again.")

q3 = st.radio("3) In Chvorinov’s rule, solidification time increases with:", 
              ["Surface area", "Volume/Area ratio", "Ambient temperature"])
if q3 == "Volume/Area ratio":
    st.success("Correct!")
else:
    st.error("Incorrect.")

# ============================================================
# 6. SUMMARY
# ============================================================
st.header("6. Summary of Week 8")

st.markdown("""
- Metals cool rapidly due to high thermal conductivity.  
- Cooling curves show phase change behavior and thermal arrest plateaus.  
- Solidification time depends heavily on the volume-to-surface-area ratio (V/A).  
- Latent heat causes a temperature plateau during the phase change.  
- Casting quality is strongly influenced by heat flow and cooling rate.  
""")
