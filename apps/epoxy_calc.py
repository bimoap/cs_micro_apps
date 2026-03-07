import streamlit as st
import pandas as pd
import plotly.express as px

# Callback function to reset the input fields
def reset_values():
    st.session_state.total_amount = 100.0
    st.session_state.part_amount = 100.0

def calculate_ratios():
    # Using standard emoji to ensure compatibility with all Streamlit versions
    st.set_page_config(page_title="Epoxy Ratio Calculator", page_icon=":material/blender:")
    
    # Initialize session state variables if they don't exist yet
    if "total_amount" not in st.session_state:
        st.session_state.total_amount = 100.0
    if "part_amount" not in st.session_state:
        st.session_state.part_amount = 100.0

    # Removed the 'icon=' parameter here to prevent the version crash
    st.title("🧪 Epoxy Mix Calculator")
    
    # Layout for instructions and the reset button
    col_text, col_btn = st.columns([4, 1])
    with col_text:
        st.write("Select the epoxy type and your calculation method.")
    with col_btn:
        st.button("🔄 Reset Inputs", on_click=reset_values)

    # 1. Define the Epoxy Data
    epoxy_data = {
        "Normal Araldite F": {
            "Part A, Araldite F": 100,
            "Part B, HY 905 Aradur": 90,
            "Part C, Plasticizer DY040": 20,
            "Part D, Accelerator DY061": 0.0044
        },
        "ADR ADH Epoxy": {
            "Part A, ADR270": 4,
            "Part B, ADH25": 1
        },
        "High Temp EL160": {
            "Part A, Resin": 100,
            "Part B, Hardener": 35
        },
        "24 hour epoxy": {
            "Part A, Araldite F": 2,
            "Part B, Hardener Aradur 2964": 1
        },
        "Araldite Kit K106 (by weight)": {
            "Part A": 100,
            "Part B": 80
        }
    }

    # 2. User Inputs: Mix Selection & Mode
    option = st.selectbox("Choose Epoxy Mix:", list(epoxy_data.keys()))
    selected_mix = epoxy_data[option]
    
    calc_mode = st.radio(
        "How do you want to calculate the mix?",
        ["By Total Amount", "By a Specific Part"]
    )

    st.divider()

    # 3. Input & Calculation Logic
    results = {}
    total_parts_ratio = sum(selected_mix.values())
    calculated_total = 0.0
    valid_input = False

    if calc_mode == "By Total Amount":
        total_amount = st.number_input("Total desired amount:", min_value=0.0, step=10.0, key="total_amount")
        
        if total_amount > 0:
            valid_input = True
            multiplier = total_amount / total_parts_ratio
            calculated_total = total_amount
            
            for part, ratio in selected_mix.items():
                results[part] = ratio * multiplier

    elif calc_mode == "By a Specific Part":
        col1, col2 = st.columns(2)
        with col1:
            part_choice = st.selectbox("Which part do you have?", list(selected_mix.keys()))
        with col2:
            part_amount = st.number_input(f"Amount of {part_choice}:", min_value=0.0, step=10.0, key="part_amount")
        
        if part_amount > 0:
            valid_input = True
            part_ratio = selected_mix[part_choice]
            multiplier = part_amount / part_ratio
            calculated_total = total_parts_ratio * multiplier
            
            for part, ratio in selected_mix.items():
                results[part] = ratio * multiplier

    # 4. Display Results
    if valid_input:
        st.subheader(f"Results for {option}")
        st.info(f"Calculated Total: **{calculated_total:.4f}**")

        # Top metric row
        cols = st.columns(len(selected_mix))
        for i, (part_name, amount) in enumerate(results.items()):
            precision = 4 if "Accelerator" in part_name else 2
            with cols[i % len(cols)]:
                st.metric(label=part_name, value=f"{amount:.{precision}f}")

        st.divider()

        # Bottom row: Table and Chart side-by-side
        col_table, col_chart = st.columns([1, 1.5])
        
        with col_table:
            st.write("### Detailed Breakdown")
            breakdown = {part: f"{amount:.4f}" for part, amount in results.items()}
            st.table(breakdown.items())
            
        with col_chart:
            # Create a dataframe for the chart
            df = pd.DataFrame({
                "Part": list(results.keys()),
                "Amount": list(results.values())
            })
            
            # Generate a donut chart
            fig = px.pie(
                df, 
                names="Part", 
                values="Amount", 
                hole=0.4,
                title=f"Mix Proportions"
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.warning("Please enter an amount greater than 0 to see the breakdown.")

if __name__ == "__main__":
    calculate_ratios()
