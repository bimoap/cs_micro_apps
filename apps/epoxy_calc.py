import streamlit as st

def calculate_ratios():
    st.set_page_config(page_title="Epoxy Ratio Calculator", page_icon="🧪")
    
    st.title(":material/blender: Epoxy Mix Calculator")
    st.write("Select the epoxy type and target total weight to get the required parts.")

    # 1. Define the Epoxy Data
    # Values represent the relative parts by weight
    epoxy_data = {
        "Normal Araldite F": {
            "Part A (Araldite F)": 100,
            "Part B (HY 905 Aradur)": 90,
            "Part C (Plasticizer DY040)": 20,
            "Part D (Accelerator DY061)": 0.0044
        },
        "ADR ADH Epoxy": {
            "Part A (ADR270)": 4,
            "Part B (ADH25)": 1
        },
        "High Temp EL160": {
            "Part A (Resin)": 100,
            "Part B (Hardener)": 35
        },
        "24 Hour Epoxy": {
            "Part A (Araldite F)": 2,
            "Part B (Hardener Aradur 2964)": 1
        }
    }

    # 2. User Inputs
    option = st.selectbox("Choose Epoxy Mix:", list(epoxy_data.keys()))
    total_amount = st.number_input("Total desired amount (grams):", min_value=0.0, value=100.0, step=10.0)

    # 3. Calculation Logic
    if total_amount > 0:
        selected_mix = epoxy_data[option]
        total_parts = sum(selected_mix.values())
        
        st.divider()
        st.subheader(f"Results for {option}")
        st.info(f"Target Total: **{total_amount} g**")

        # Create columns for a clean layout
        cols = st.columns(len(selected_mix))
        
        for i, (part_name, ratio) in enumerate(selected_mix.items()):
            # Calculate weight: (Part Ratio / Total Ratios) * Total Weight
            weight = (ratio / total_parts) * total_amount
            
            with cols[i % len(cols)]:
                # Use 4 decimal places for the Accelerator, 2 for others
                precision = 4 if "Accelerator" in part_name else 2
                st.metric(label=part_name, value=f"{weight:.{precision}f} g")

        # Table View for high precision verification
        st.write("### Detailed Breakdown")
        breakdown = {part: f"{(r/total_parts)*total_amount:.4f} g" for part, r in selected_mix.items()}
        st.table(breakdown.items())
    else:
        st.warning("Please enter a total amount greater than 0.")

if __name__ == "__main__":
    calculate_ratios()
