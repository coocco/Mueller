import numpy as np
import streamlit as st

def apply_mueller_matrix(M, S_in):
    S_out = np.dot(M, S_in)
    return S_out

def degree_of_polarization(S):
    I, Q, U, V = S
    dop = np.sqrt(Q**2 + U**2 + V**2) / I if I != 0 else 0
    return dop

st.title("Mueller Matrix Calculator")

st.markdown("""
Enter your **Mueller matrix** (4×4) and **Stokes vector** (length 4) to see how light polarization changes.
""")

st.sidebar.header("Quick Presets")
if st.sidebar.button("Horizontal Polarizer + Unpolarized Light"):
    st.session_state.M_default = [
        [0.5, 0.5, 0, 0],
        [0.5, 0.5, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    st.session_state.S_default = [1.0, 0.0, 0.0, 0.0]

# Initialize defaults if not set
if "M_default" not in st.session_state:
    st.session_state.M_default = [[1.0, 0.0, 0.0, 0.0],
                                  [0.0, 1.0, 0.0, 0.0],
                                  [0.0, 0.0, 1.0, 0.0],
                                  [0.0, 0.0, 0.0, 1.0]]
if "S_default" not in st.session_state:
    st.session_state.S_default = [1.0, 0.0, 0.0, 0.0]

st.sidebar.header("Input Mueller Matrix")
M_elements = []
for i in range(4):
    default_row = ", ".join([str(x) for x in st.session_state.M_default[i]])
    row = st.sidebar.text_input(f"Row {i+1} (4 numbers, comma-separated)", value=default_row, key=f"row_{i}")
    M_elements.extend([float(x.strip()) for x in row.replace(" ", "").split(",")])

st.sidebar.header("Input Stokes Vector")
def_s = ", ".join([str(x) for x in st.session_state.S_default])
S_input_str = st.sidebar.text_input("Stokes Vector (I, Q, U, V)", value=def_s)
S_elements = [float(x.strip()) for x in S_input_str.replace(" ", "").split(",")]

try:
    if len(M_elements) != 16:
        st.error("Mueller matrix must have 16 elements (4 rows of 4 numbers).")
    else:
        M = np.array(M_elements).reshape((4, 4))
        S_in = np.array(S_elements)
        S_out = apply_mueller_matrix(M, S_in)

        st.subheader("Results")
        st.write("**Input Stokes Vector:**", S_in)
        st.write("**Output Stokes Vector:**", S_out)

        dop = degree_of_polarization(S_out)
        st.write(f"**Degree of Polarization:** {dop:.3f}")

        if dop > 0.99:
            st.success("Fully polarized light")
        elif dop > 0.01:
            st.info("Partially polarized light")
        else:
            st.warning("Unpolarized light")

except Exception as e:
    st.error(f"Error: {e}")

