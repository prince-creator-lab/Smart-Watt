import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="SmartWatt", page_icon="🔋")
st.title("🔋 SmartWatt - Home Energy Advisor (Interactive)")
st.markdown("Fill in your appliance usage to get energy insights and savings tips!")

# Initialize session state
if 'appliance_data' not in st.session_state:
    st.session_state.appliance_data = []

# Form to input new appliance
with st.form("appliance_form"):
    appliance = st.text_input("Appliance Name", value="Air Conditioner")
    wattage = st.number_input("Wattage (W)", min_value=10, value=1500)
    usage_hours = st.number_input("Usage Hours per Day", min_value=0.0, value=6.0)
    days_used = st.number_input("Days Used per Month", min_value=1, value=25)
    add_btn = st.form_submit_button("Add Appliance")

if add_btn:
    kwh = round((wattage * usage_hours * days_used) / 1000, 2)
    st.session_state.appliance_data.append({
        "Appliance": appliance,
        "Wattage (W)": wattage,
        "UsageHoursPerDay": usage_hours,
        "DaysUsedPerMonth": days_used,
        "MonthlyUsage_kWh": kwh
    })
    st.success(f"✅ Added: {appliance} ({kwh} kWh/month)")

# Convert to DataFrame
df = pd.DataFrame(st.session_state.appliance_data)

# Display table and analysis
if not df.empty:
    st.subheader("📊 Appliance Usage Summary")
    st.dataframe(df)

    total_kwh = df["MonthlyUsage_kWh"].sum()
    st.success(f"⚡ Total Estimated Monthly Usage: **{total_kwh:.2f} kWh**")

    # Pie chart
    st.subheader("📈 Energy Usage Breakdown")
    fig, ax = plt.subplots()
    ax.pie(df["MonthlyUsage_kWh"], labels=df["Appliance"], autopct="%1.1f%%", startangle=140)
    ax.axis("equal")
    st.pyplot(fig)

    # Recommendations
    st.subheader("💡 Smart Recommendations")
    for row in df.itertuples():
        if row.MonthlyUsage_kWh > total_kwh * 0.25:
            st.warning(f"🔌 **{row.Appliance}** uses a lot of power. Consider reducing usage or replacing it.")
        elif row._2 > 1000 and row.UsageHoursPerDay > 1:
            st.info(f"⚠️ **{row.Appliance}** is high wattage. Try using it during non-peak hours.")
        elif "bulb" in row.Appliance.lower():
            st.info(f"💡 Use LED for **{row.Appliance}** to save energy.")
        elif "ac" in row.Appliance.lower():
            st.info(f"❄️ Keep your **{row.Appliance}** at 26°C and clean filters for efficiency.")

    if total_kwh > 400:
        st.error("⚠️ High energy usage detected! Try energy audits or solar alternatives.")
    else:
        st.success("✅ Your energy usage is efficient! 🌿")
else:
    st.info("Add at least one appliance above to begin analysis.")
