import numpy as np
import streamlit as st

def apply_mueller_matrix(M, S_in):
    """
    Apply Mueller matrix M to input Stokes vector S_in.
    Returns the output Stokes vector.
    """
    S_out = np.dot(M, S_in)
    return S_out

st.title("Mueller Matrix Calculator")

st.markdown("""
Enter your **Mueller matrix** (4×4) and **Stokes vector** (length 4) to see how light polarization changes.
""")

st.sidebar.header("Input Mueller Matrix")
M_elements = []
for i in range(4):
    row = st.sidebar.text_input(f"Row {i+1} (4 numbers, comma-separated)", value="1.0, 0.0, 0.0, 0.0" if i == 0 else "0.0, 1.0, 0.0, 0.0")
    M_elements.extend([float(x.strip()) for x in row.split(",")])

st.sidebar.header("Input Stokes Vector")
S_input_str = st.sidebar.text_input("Stokes Vector (I, Q, U, V)", value="1.0, 0.0, 0.0, 0.0")
S_elements = [float(x.strip()) for x in S_input_str.split(",")]

# Reshape and calculate
try:
    M = np.array(M_elements).reshape((4, 4))
    S_in = np.array(S_elements)
    S_out = apply_mueller_matrix(M, S_in)

    st.subheader("Results")
    st.write("**Input Stokes Vector:**", S_in)
    st.write("**Output Stokes Vector:**", S_out)

except Exception as e:
    st.error(f"Error: {e}")
