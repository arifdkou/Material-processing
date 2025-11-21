import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
#   MATERIAL PROCESS LABORATORY – WEEK 9
#   Topic: Welding and Joining of Metals
#   Language: English
#   Format: Streamlit Interactive Lecture Note
# ---------------------------------------------------------

st.set_page_config(
    page_title="Material Process Lab – Week 9: Welding and Joining",
    layout="centered"
)

st.title("Material Process Laboratory – Week 9")
st.subheader("Welding and Joining of Metals")

st.markdown(
    """
This interactive lecture note is prepared for **Week 9** of the Material Process Laboratory course.  
Topic: **Welding and Joining of Metals**

Use the **sidebar** to navigate between:

- **Learning Outcomes & Theory**
- **Heat Input Simulation**
- **Weld Thermal Profile (Simple Model)**
- **Solved Examples**
- **Quiz**
- **Summary**
    """
)

# Sidebar navigation
section = st.sidebar.selectbox(
    "Go to section",
    [
        "Learning Outcomes & Theory",
        "Heat Input Simulation",
        "Weld Thermal Profile",
        "Solved Examples",
        "Quiz",
        "Summary"
    ]
)

# ---------------------------------------------------------
# 1) LEARNING OUTCOMES & THEORY
# ---------------------------------------------------------
if section == "Learning Outcomes & Theory":
    st.header("1. Learning Outcomes")

    st.markdown(
        """
After completing this week, students will be able to:

1. **Define** the basic principles of welding and fusion joining of metals.
2. **Classify** different welding processes (arc welding, resistance welding, etc.).
3. **Calculate** heat input in arc welding using process parameters.
4. **Explain** how heat input and cooling rate affect microstructure and mechanical properties.
5. **Interpret** simple weld thermal cycles and heat-affected zone (HAZ) behavior.
        """
    )

    st.header("2. Introduction to Welding")

    st.markdown(
        """
Welding is a permanent joining process in which two or more parts are **fused together** by:

- **Heating** (with or without pressure),
- Often with **filler material**.

Common welding processes:

- **Shielded Metal Arc Welding (SMAW)**
- **Gas Metal Arc Welding (GMAW / MIG)**
- **Gas Tungsten Arc Welding (GTAW / TIG)**
- **Submerged Arc Welding (SAW)**
- **Resistance Spot Welding (RSW)**

Welding produces three important regions:

1. **Fusion Zone (FZ):** Fully melted and resolidified metal.
2. **Heat-Affected Zone (HAZ):** Not melted but heated enough to change microstructure.
3. **Base Metal (BM):** Unaffected parent material.
        """
    )

    st.header("3. Heat Input in Arc Welding")

    st.markdown("The **heat input per unit length** in arc welding can be approximated by:")

    st.latex(
        r"""
Q = \eta \, \frac{V I}{v}
"""
    )

    st.markdown(
        r"""
where:

- \(Q\): heat input per unit length (J/mm or kJ/mm),
- \(\eta\): process efficiency (typically 0.6–0.9),
- \(V\): arc voltage (V),
- \(I\): welding current (A),
- \(v\): travel speed (mm/s or m/s).
        """
    )

    st.markdown(
        """
Higher heat input generally leads to:

- **Wider HAZ**
- **Coarser grains**
- **Lower cooling rate**
- Potentially **lower strength** and **toughness**, but better fusion.

Lower heat input:

- **Narrower HAZ**
- **Finer grains**
- **Higher cooling rate**
- Risk of **hard and brittle microstructures** (especially in steels).
        """
    )

    st.header("4. Cooling Rate and Microstructure")

    st.markdown(
        """
The **cooling rate** near the weld has a strong influence on microstructure:

- In **low-alloy steels**:
  - Slow cooling → ferrite + pearlite (tough, not very hard).
  - Fast cooling → bainite or martensite (harder, possibly brittle).

A simple (conceptual) relation is:

- High heat input → low cooling rate.
- Low heat input → high cooling rate.

In this app, we will use a **simple model** to visualize the thermal profile near the weld.
        """
    )


# ---------------------------------------------------------
# 2) HEAT INPUT SIMULATION
# ---------------------------------------------------------
elif section == "Heat Input Simulation":
    st.header("Heat Input Simulation for Arc Welding")

    st.markdown(
        """
Use the controls below to explore how **voltage**, **current**, **travel speed**, and **efficiency**
affect the **heat input per unit length**.

We use the relation:

"""
    )
    st.latex(r"Q = \eta \, \frac{V I}{v}")
    st.markdown("Here we will calculate **Q in kJ/mm**.")

    st.subheader("Input Parameters")

    col1, col2 = st.columns(2)

    with col1:
        V = st.slider("Arc Voltage V (volts)", min_value=10, max_value=40, value=24, step=1)
        I = st.slider("Welding Current I (amps)", min_value=50, max_value=350, value=180, step=10)
        eta = st.slider("Process Efficiency η", min_value=0.50, max_value=0.95, value=0.80, step=0.01)

    with col2:
        travel_speed_mm_s = st.slider(
            "Travel Speed v (mm/s)", min_value=2.0, max_value=20.0, value=6.0, step=0.5
        )
        plate_thickness_mm = st.slider(
            "Plate Thickness (mm)", min_value=3, max_value=30, value=10, step=1
        )

    # Heat input calculation
    # Q_kJ_per_mm = η * V * I / (1000 * v_mm_s)
    Q_kJ_per_mm = eta * V * I / (1000.0 * travel_speed_mm_s)

    st.subheader("Results")

    st.write(f"**Heat input per unit length Q:** `{Q_kJ_per_mm:.4f} kJ/mm`")
    st.write(f"Plate thickness: `{plate_thickness_mm} mm`")

    # Simple qualitative interpretation
    if Q_kJ_per_mm < 0.5:
        level = "LOW"
        comment = "Narrow weld bead, high cooling rate, possible hard microstructures in steels."
    elif Q_kJ_per_mm < 1.5:
        level = "MODERATE"
        comment = "Balanced heat input. Usually acceptable HAZ width and cooling rate."
    else:
        level = "HIGH"
        comment = "Wide HAZ, coarse grains, low cooling rate. Risk of softening or distortion."

    st.markdown(
        f"""
**Qualitative Interpretation:**

- Heat input level: **{level}**
- Comment: {comment}
        """
    )

    st.info(
        "Students can change the parameters and observe how heat input changes. "
        "You can also compare the effect of doubling welding speed or current."
    )


# ---------------------------------------------------------
# 3) SIMPLE WELD THERMAL PROFILE
# ---------------------------------------------------------
elif section == "Weld Thermal Profile":
    st.header("Simple Weld Thermal Profile (Conceptual Model)")

    st.markdown(
        """
To understand how temperature varies with **distance from the weld centerline**, we can use a very simple
**Gaussian-like temperature distribution** (not a rigorous Rosenthal solution, but good for visualization):

"""
    )
    st.latex(
        r"""
T(x) = T_0 + \Delta T \, \exp\!\left( -\left( \frac{x}{w} \right)^2 \right)
"""
    )
    st.markdown(
        """
where:

- \(T_0\): base metal temperature (°C),
- \(\Delta T\): peak temperature rise at the weld centerline,
- \(w\): characteristic width of the weld thermal field (mm),
- \(x\): distance from weld centerline (mm).

We will link \(\Delta T\) to the **heat input**.
        """
    )

    st.subheader("Input Parameters")

    T0 = st.slider("Base Metal Temperature T₀ (°C)", min_value=20, max_value=100, value=25, step=5)
    Q_kJ_per_mm_input = st.slider(
        "Assumed Heat Input Q (kJ/mm)", min_value=0.2, max_value=3.0, value=1.0, step=0.1
    )
    w = st.slider("Thermal Width Parameter w (mm)", min_value=3.0, max_value=30.0, value=10.0, step=1.0)

    # Relate deltaT to Q: very simple proportional model
    # For Q = 1 kJ/mm, let ΔT ≈ 1000°C (just a conceptual scale)
    delta_T = 1000.0 * (Q_kJ_per_mm_input / 1.0)

    x = np.linspace(-40, 40, 400)
    T = T0 + delta_T * np.exp(-(x / w) ** 2)

    fig, ax = plt.subplots()
    ax.plot(x, T)
    ax.set_xlabel("Distance from Weld Centerline x (mm)")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Conceptual Weld Thermal Profile")
    ax.grid(True)

    st.pyplot(fig)

    st.markdown(
        """
**Interpretation:**

- Near \(x = 0\), temperature is highest (fusion zone).
- For intermediate distances, temperature may exceed critical transformation ranges (HAZ).
- Far from the weld, temperature is close to \(T_0\) (unaffected base metal).

This simple model helps students visualize how **heat input (Q)** and **thermal width (w)** affect
the temperature field and thus the **HAZ width**.
        """
    )


# ---------------------------------------------------------
# 4) SOLVED EXAMPLES
# ---------------------------------------------------------
elif section == "Solved Examples":
    st.header("Solved Examples – Welding and Joining")

    example = st.selectbox(
        "Select example",
        [
            "Example 1 – Heat Input Calculation",
            "Example 2 – Effect of Travel Speed",
            "Example 3 – Estimating Cooling Time",
            "Example 4 – HAZ Width Comparison",
            "Example 5 – Process Selection"
        ]
    )

    if example == "Example 1 – Heat Input Calculation":
        st.subheader("Example 1 – Heat Input in GMAW")

        st.markdown(
            """
**Problem:**  
Gas Metal Arc Welding (GMAW) is used on a steel plate with:

- Voltage \(V = 26\ \text{V}\)
- Current \(I = 220\ \text{A}\)
- Travel speed \(v = 5\ \text{mm/s}\)
- Process efficiency \(\eta = 0.8\)

Compute the **heat input per unit length** \(Q\) in kJ/mm.

**Solution:**

We use:
"""
        )
        st.latex(r"Q = \eta \, \frac{V I}{v}")
        st.markdown(
            r"""
Substitute the values (with \(v\) in mm/s):

\[
Q = 0.8 \times \frac{26 \times 220}{5}
\]

\[
26 \times 220 = 5720
\]

\[
\frac{5720}{5} = 1144
\]

\[
Q = 0.8 \times 1144 = 915.2\ \text{J/mm}
\]

Convert to kJ/mm:

\[
Q = 0.9152\ \text{kJ/mm}
\]

**Answer:** \(Q \approx 0.92\ \text{kJ/mm}\).
            """
        )

    elif example == "Example 2 – Effect of Travel Speed":
        st.subheader("Example 2 – Effect of Travel Speed on Heat Input")

        st.markdown(
            """
**Problem:**  
Consider the same welding parameters as Example 1, but we compare two travel speeds:

- Case A: \(v_A = 5\ \text{mm/s}\)
- Case B: \(v_B = 10\ \text{mm/s}\)

Use:

- \(V = 26\ \text{V}\),
- \(I = 220\ \text{A}\),
- \(\eta = 0.8\).

Compute \(Q_A\) and \(Q_B\) and comment on the result.

**Solution:**

Heat input:

\[
Q = \eta \, \frac{V I}{v}
\]

For Case A:

\[
Q_A = 0.8 \frac{26 \times 220}{5}
      = 915.2\ \text{J/mm}
      = 0.915\ \text{kJ/mm}
\]

For Case B:

\[
Q_B = 0.8 \frac{26 \times 220}{10}
      = 457.6\ \text{J/mm}
      = 0.458\ \text{kJ/mm}
\]

**Interpretation:**

- Doubling the travel speed **halves the heat input** per unit length.
- Lower heat input produces a **narrower HAZ** and **higher cooling rate**.
            """
        )

    elif example == "Example 3 – Estimating Cooling Time":
        st.subheader("Example 3 – Simple Cooling Time Estimate")

        st.markdown(
            """
**Problem:**  
A small weld region can be approximated as a lumped body with:

- Initial temperature \(T_i = 900^\circ\text{C}\),
- Ambient temperature \(T_f = 25^\circ\text{C}\),
- Time constant \(τ = 15\ \text{s}\).

Estimate the time to cool to \(T = 300^\circ\text{C}\) using:

\[
\frac{T - T_f}{T_i - T_f} = e^{-t/τ}
\]

**Solution:**

Compute the temperature ratio:

\[
\frac{T - T_f}{T_i - T_f}
= \frac{300 - 25}{900 - 25}
= \frac{275}{875}
= 0.314
\]

Then:

\[
0.314 = e^{-t/15}
\]

Take natural logarithm:

\[
-t/15 = \ln(0.314) \Rightarrow t = -15 \ln(0.314)
\]

\[
\ln(0.314) \approx -1.158
\]

\[
t = -15 \times (-1.158) \approx 17.4\ \text{s}
\]

**Answer:** Cooling to \(300^\circ\text{C}\) takes about **17 s**.
            """
        )

    elif example == "Example 4 – HAZ Width Comparison":
        st.subheader("Example 4 – HAZ Width and Heat Input")

        st.markdown(
            """
**Problem:**  
Two welding procedures are used on the same steel plate:

- Procedure 1: \(Q_1 = 0.5\ \text{kJ/mm}\)
- Procedure 2: \(Q_2 = 1.0\ \text{kJ/mm}\)

Assume the **HAZ width is proportional to the square root of the heat input**:

\[
\text{HAZ width} \propto \sqrt{Q}
\]

If Procedure 1 gives a HAZ width of **4 mm**, estimate the HAZ width for Procedure 2.

**Solution:**

Let:

\[
\frac{\text{HAZ}_2}{\text{HAZ}_1} = \sqrt{\frac{Q_2}{Q_1}}
\]

\[
\frac{\text{HAZ}_2}{4} = \sqrt{\frac{1.0}{0.5}} = \sqrt{2} \approx 1.414
\]

\[
\text{HAZ}_2 = 4 \times 1.414 \approx 5.66\ \text{mm}
\]

**Answer:** HAZ width for Procedure 2 is about **5.7 mm**.
            """
        )

    elif example == "Example 5 – Process Selection":
        st.subheader("Example 5 – Process Selection for Thin Sheet")

        st.markdown(
            """
**Problem:**  
You need to weld **1.5 mm thick stainless steel sheet** for a high-quality application with
minimum distortion and good control of heat input.

Which process would you prefer and why?

Options:

1. Submerged Arc Welding (SAW) at high current  
2. Gas Metal Arc Welding (GMAW) with spray transfer  
3. Gas Tungsten Arc Welding (GTAW / TIG)  

**Solution / Discussion:**

- SAW typically uses **very high heat input** and is more suitable for **thick sections**.
- GMAW with spray transfer may also have **relatively high heat input** and less precise arc.
- GTAW (TIG) provides:
  - Excellent **arc stability**,
  - Precise **heat input control**,
  - Very **clean welds**.

**Answer:**  
**GTAW / TIG** is the most suitable choice for **thin stainless sheet** with good control and quality.
            """
        )


# ---------------------------------------------------------
# 5) QUIZ
# ---------------------------------------------------------
elif section == "Quiz":
    st.header("Quick Quiz – Week 9: Welding and Joining")

    st.markdown("Answer the questions and check your understanding.")

    # Question 1
    st.subheader("Question 1")
    st.markdown(
        """
If you **increase travel speed** while keeping voltage and current constant, what happens to heat input per unit length?

Choose the best answer.
        """
    )
    q1 = st.radio(
        "Heat input trend:",
        [
            "Heat input increases.",
            "Heat input decreases.",
            "Heat input stays the same.",
            "Heat input first increases then decreases."
        ],
        index=1
    )

    if q1:
        if q1 == "Heat input decreases.":
            st.success("Correct. Q = η V I / v, so increasing v reduces Q.")
        else:
            st.error("Not correct. Recall Q = η V I / v; increasing v lowers Q.")

    # Question 2
    st.subheader("Question 2")
    st.markdown(
        """
Which region in a weldment experiences temperatures high enough to **change microstructure** but **does not melt**?
        """
    )
    q2 = st.radio(
        "Select region:",
        [
            "Fusion Zone (FZ)",
            "Heat-Affected Zone (HAZ)",
            "Base Metal (BM)",
            "Filler Metal Only"
        ],
        index=1
    )

    if q2:
        if q2 == "Heat-Affected Zone (HAZ)":
            st.success("Correct. HAZ is not melted but its microstructure is altered by heat.")
        else:
            st.error("Incorrect. The correct answer is Heat-Affected Zone (HAZ).")

    # Question 3
    st.subheader("Question 3")
    st.markdown(
        """
Which process generally gives **best control of heat input** and is suitable for **high-quality thin sheet welding**?
        """
    )
    q3 = st.radio(
        "Select process:",
        [
            "Shielded Metal Arc Welding (SMAW)",
            "Gas Tungsten Arc Welding (GTAW / TIG)",
            "Submerged Arc Welding (SAW)",
            "Resistance Spot Welding (RSW)"
        ],
        index=1
    )

    if q3:
        if q3 == "Gas Tungsten Arc Welding (GTAW / TIG)":
            st.success("Correct. GTAW/TIG has excellent heat control and is ideal for thin, high-quality welds.")
        else:
            st.error("Not the best choice. GTAW/TIG is usually preferred for precise low-heat-input welding.")


# ---------------------------------------------------------
# 6) SUMMARY
# ---------------------------------------------------------
elif section == "Summary":
    st.header("Summary – Week 9: Welding and Joining of Metals")

    st.markdown(
        """
**Key Points:**

- Welding is a **permanent joining process** involving fusion of metals.
- Major regions: **Fusion Zone**, **Heat-Affected Zone (HAZ)**, and **Base Metal**.
- **Heat input** in arc welding is approximated by:

"""
    )
    st.latex(r"Q = \eta \, \frac{V I}{v}")
    st.markdown(
        """
- Heat input strongly affects:
  - **Cooling rate**
  - **HAZ width**
  - **Microstructure** (ferrite, pearlite, bainite, martensite)
  - **Mechanical properties** (hardness, toughness).

- A **simple Gaussian model** can be used to visualize temperature distribution around the weld.
- For **thin, high-quality welds**, processes like **GTAW/TIG** offer precise heat control.

Students are encouraged to:

- Experiment with different parameters in the **simulation**,
- Sketch thermal cycles and HAZ regions,
- Connect **heat input** and **cooling rate** to **metallurgical transformations**.
        """
    )

    st.info(
        "You can extend this app by adding your own examples, more realistic thermal models, "
        "or links to experimental data from the laboratory."
    )
