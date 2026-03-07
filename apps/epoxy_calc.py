import streamlit as st

def calculate_ratios():
    st.set_page_config(page_title="Epoxy Ratio Calculator", page_icon="🧪")
    
    st.title("🧪 Epoxy Mix Calculator")
    st.write("Select the epoxy type and your calculation method.")

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
        total_amount = st.number_input("Total desired amount:", min_value=0.0, value=100.0, step=10.0)
        if total_amount > 0:
            valid_input = True
            # Find the multiplier based on the total target
            multiplier = total_amount / total_parts_ratio
            calculated_total = total_amount
            
            for part, ratio in selected_mix.items():
                results[part] = ratio * multiplier

    elif calc_mode == "By a Specific Part":
        col1, col2 = st.columns(2)
        with col1:
            part_choice = st.selectbox("Which part do you have?", list(selected_mix.keys()))
        with col2:
            part_amount = st.number_input(f"Amount of {part_choice}:", min_value=0.0, value=100.0, step=10.0)
        
        if part_amount > 0:
            valid_input = True
            # Find the multiplier based on the chosen part's base ratio
            part_ratio = selected_mix[part_choice]
            multiplier = part_amount / part_ratio
            calculated_total = total_parts_ratio * multiplier
            
            for part, ratio in selected_mix.items():
                results[part] = ratio * multiplier

    # 4. Display Results
    if valid_input:
        st.subheader(f"Results for {option}")
        st.info(f"Calculated Total: **{calculated_total:.4f}**")

        # Create dynamic columns based on the number of parts
        cols = st.columns(len(selected_mix))
        
        for i, (part_name, amount) in enumerate(results.items()):
            # Keep higher precision for the accelerator due to the tiny ratio
            precision = 4 if "Accelerator" in part_name else 2
            with cols[i % len(cols)]:
                st.metric(label=part_name, value=f"{amount:.{precision}f}")

        st.write("### Detailed Breakdown")
        breakdown = {part: f"{amount:.4f}" for part, amount in results.items()}
        st.table(breakdown.items())
        
    else:
        st.warning("Please enter an amount greater than 0 to see the breakdown.")

if __name__ == "__main__":
    calculate_ratios()
