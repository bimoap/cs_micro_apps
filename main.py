import streamlit as st

# Set global page config (optional, but recommended)
# Note: set_page_config must be the first Streamlit command used
st.set_page_config(page_title="C/S micro apps", page_icon="⚙️")

# Define your pages
app_1 = st.Page("apps/cs_resistance_calc.py", title="Coil Resistance Calculator", icon=":material/calculate:")
app_2 = st.Page("apps/mid_winding_check.py", title="Pre & Mid Winding Checker", icon=":material/calculate:")
app_3 = st.Page("apps/coil_core_temp.py", title="Coil Core Temperature", icon=":material/calculate:")
app_4 = st.Page("apps/epoxy_calc.py", title="Epoxy Calculator", icon=":material/calculate:")

# Group them into a navigation menu
pg = st.navigation([app_1, app_2, app_3, app_4])

# Add the signature to the bottom of the sidebar
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **App developed & maintained by:**  
    Bimo Adhi Prastya  
    Coil Shop Technician & NT Production Engineer
    """
)

# Run the selected page
pg.run()
