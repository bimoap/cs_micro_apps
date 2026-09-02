import streamlit as st

def calculate_resistance(voltage: float, current: float) -> float:
    """Calculates resistance given voltage and current."""
    return voltage / current

def calculate_core_temperature(t_start: float, r_start: float, r_final: float) -> float:
    """Calculates the core temperature of an electromagnet coil using the original 0.00393 constant."""
    temperature_rise = (r_final - r_start) / (0.00393 * r_start)
    return t_start + temperature_rise

# Set up the web page layout and title
st.set_page_config(page_title="Core Temperature Calculator", layout="centered")
st.title("Core Temperature Calculator")
st.markdown("Enter your current and voltage measurements below to calculate resistance and core temperature.")

# Display the original formula being used for reference
with st.expander("View Original Calculation Formula"):
    st.latex(r"T_{core} = T_{start} + \frac{R_{final} - R_{start}}{0.00393 \cdot R_{start}}")

st.divider()

# Create a form for the inputs
with st.form("calc_form"):
    # Row 1: Current
    current = st.number_input("Current (A)", value=240.0, step=1.0, format="%.2f")
        
    # Row 2: Voltages
    col1, col2 = st.columns(2)
    with col1:
        v_start = st.number_input("Start Voltage (V)", value=10.00, step=0.01, format="%.2f")
    with col2:
        v_final = st.number_input("Finish Voltage (V)", value=12.00, step=0.01, format="%.2f")
        
    # Row 3: Start Temperature
    t_start = st.number_input("Start Temp (°C)", value=20.0, step=0.5, format="%.1f")
        
    # The submit button triggers the calculation
    submitted = st.form_submit_button("Calculate Core Temperature")

# Handle the calculation and display the results outside the form
if submitted:
    if current <= 0:
        st.error("Current must be greater than zero to calculate resistance.")
    else:
        # Calculate resistances
        r_start = calculate_resistance(v_start, current)
        r_final = calculate_resistance(v_final, current)
        
        # Calculate temperatures
        final_temp = calculate_core_temperature(t_start, r_start, r_final)
        temp_rise = final_temp - t_start
        
        st.success("Calculation complete!")
        
        # Display the calculated resistances to 6 decimal places
        st.markdown("### Calculated Resistances")
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.metric(label="Start Resistance", value=f"{r_start:.6f} Ω")
        with res_col2:
            st.metric(label="Finish Resistance", value=f"{r_final:.6f} Ω")
            
        st.divider()
        
        # Display the final temperature result
        st.markdown("### Core Temperature")
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
    Coil Shop Technician and NT Production Engineer
</div>
""", unsafe_allow_html=True)
