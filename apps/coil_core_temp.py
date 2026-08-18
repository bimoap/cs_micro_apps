import streamlit as st

def calculate_core_temperature(t_start: float, r_start: float, r_final: float) -> float:
    """Calculates the core temperature of an electromagnet coil using the 254.5 constant."""
    temperature_rise = ((r_final - r_start) / r_start) * 254.5
    return t_start + temperature_rise

# Set up the web page layout and title
st.set_page_config(page_title="Coil Temperature Calculator", layout="centered")
st.title("Coil Core Temperature Calculator")
st.markdown("Enter your measurements below to calculate the internal core temperature of the coil.")

st.divider()

# Create a form so the app doesn't recalculate on every single keystroke
with st.form("calc_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        t_start = st.number_input("Start Temp (°C)", value=20.0, step=0.5, format="%.1f")
    with col2:
        r_start = st.number_input("Start Resistance (Ω)", value=1.000000, step=0.000001, format="%.6f")
    with col3:
        r_final = st.number_input("Final Resistance (Ω)", value=1.200000, step=0.000001, format="%.6f")
        
    # The submit button triggers the calculation
    submitted = st.form_submit_button("Calculate Core Temperature")

# Handle the calculation and display the results outside the form
if submitted:
    if r_start <= 0:
        st.error("Start resistance must be greater than zero.")
    else:
        # Perform calculation
        final_temp = calculate_core_temperature(t_start, r_start, r_final)
        temp_rise = final_temp - t_start
        
        st.success("Calculation complete!")
        
        # Display the result using Streamlit's built-in metric widget
        st.metric(
            label="Calculated Core Temperature", 
            value=f"{final_temp:.2f} °C", 
            delta=f"{temp_rise:.2f} °C (Temperature Rise)",
            delta_color="off" # Keeps the delta text gray instead of red/green
        )

# Signature Section
st.markdown("""
---
<div style="text-align: center; color: gray; font-size: 0.9em;">
    App developed & maintained by:<br>
    <strong>Bimo Adhi Prastya</strong><br>
    Coil Shop Production Staff
</div>
""", unsafe_allow_html=True)
