import streamlit as st

# Define your pages
app_1 = st.Page("apps/coil_calculator.py", title="Coil Calculator", icon="🖩")
app_2 = st.Page("apps/magnetic_field_sim.py", title="Magnetic Field Sim", icon="🖩")

# Group them into a navigation menu
pg = st.navigation([app_1, app_2])

# Set global page config (optional, but recommended)
st.set_page_config(page_title="My Engineering Suite", page_icon="⚙️")

# Run the selected page
pg.run()
