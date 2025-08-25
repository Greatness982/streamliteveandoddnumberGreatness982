import streamlit as st
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import pandas as pd

# ------------------ Streamlit Config ------------------
st.set_page_config(page_title="📱 Phone Number Tracker", page_icon="📍", layout="centered")
st.title("📱 Phone Number Tracker (Educational Demo)")

# ------------------ Session State for History ------------------
if "history" not in st.session_state:
    st.session_state.history = []  # store past lookups

# ------------------ Input ------------------
number = st.text_input("Enter a phone number with country code (e.g., +14155552671):")

if st.button("Track Number"):
    try:
        parsed_number = phonenumbers.parse(number, None)

        # --- Extract Info ---
        country = geocoder.description_for_number(parsed_number, "en")  # country / region
        sim_carrier = carrier.name_for_number(parsed_number, "en")
        tz = timezone.time_zones_for_number(parsed_number)
        region_code = phonenumbers.region_code_for_number(parsed_number)

        # 🏙️ Sometimes includes city/area (especially for landlines)
        possible_area = geocoder.description_for_number(parsed_number, "en")

        # Flag
        flag = f":flag-{region_code.lower()}:" if region_code else "🏳️"

        st.success("✅ Phone number parsed successfully!")
        st.write(f"{flag} **Country/Region:** {country or 'Unknown'}")
        st.write(f"🏙️ **Possible Area:** {possible_area or 'Not available'}")
        st.write(f"📡 **Carrier:** {sim_carrier or 'Unknown'}")
        st.write(f"⏰ **Timezone(s):** {', '.join(tz) if tz else 'Unknown'}")

        # Save to history
        st.session_state.history.append({
            "Number": number,
            "Country": country or "Unknown",
            "Area": possible_area or "Not available",
            "Carrier": sim_carrier or "Unknown",
            "Timezone": ", ".join(tz) if tz else "Unknown"
        })

    except Exception as e:
        st.error(f"❌ Error: {e}")

# ------------------ Show History ------------------
if st.session_state.history:
    st.subheader("📜 Phone Lookup History")
    df_history = pd.DataFrame(st.session_state.history)
    st.dataframe(df_history, use_container_width=True)
