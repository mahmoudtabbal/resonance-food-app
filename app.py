
import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_excel("Unified_Food_Compatibility_Table_With_Resonance.xlsx")
    return df

st.set_page_config(page_title="Resonance Dowsing Food Log", layout="wide")
st.title("🔮 Resonance Compatibility Testing App")

if "index" not in st.session_state:
    st.session_state.index = 0

if "data" not in st.session_state:
    st.session_state.data = load_data()

df = st.session_state.data
current = df.iloc[st.session_state.index]
st.subheader(f"Food Item: {current['Item']}")

st.markdown(f"**Category:** {current['Category']} | **Super Category:** {current['Super Category']}")
st.markdown(f"**Dosha:** {current['Dosha Compatibility']} | **Metabolic Type:** {current['Metabolic Typing Compatibility']} | **Glandular Type:** {current['Glandular Compatibility']}")

resonance = st.selectbox("Select Resonance Compatibility", ["", "Compatible", "Incompatible", "Limited", "Neutral"])

if st.button("Save and Next"):
    st.session_state.data.at[st.session_state.index, "Resonance Compatibility"] = resonance
    if st.session_state.index < len(st.session_state.data) - 1:
        st.session_state.index += 1
    else:
        st.success("✅ All items processed!")

with st.expander("📥 Export Filtered Table"):
    dosha = st.selectbox("Filter by Dosha", ["All", "Vata", "Pitta", "Kapha", "Tridoshic"])
    resonance_filter = st.selectbox("Filter by Resonance", ["All", "Compatible", "Incompatible", "Limited", "Neutral"])

    filtered = st.session_state.data.copy()
    if dosha != "All":
        filtered = filtered[filtered["Dosha Compatibility"].str.contains(dosha, na=False)]
    if resonance_filter != "All":
        filtered = filtered[filtered["Resonance Compatibility"] == resonance_filter]

    st.dataframe(filtered)
    st.download_button("Download Filtered Table", data=filtered.to_csv(index=False), file_name="Filtered_Resonant_Foods.csv")
