import streamlit as st
import math
import pandas as pd

# Page configuration
st.set_page_config(page_title="Bio-Space Bone | NASA Space Apps", layout="wide")

st.title("🚀 Bio-Space Bone: Post-Mission Bone Rehabilitation & Mineral Safety System")
st.markdown("An algorithmic simulation model for tracking Bone Mineral Density (BMD) recovery and preventing renal stones after lunar missions.")

# Sidebar inputs
st.sidebar.header("⚙️ Daily Protocol Settings")
goat_milk = st.sidebar.slider("Goat Milk (cups/day)", 0, 5, 1)
dates = st.sidebar.slider("Dates (pieces/day)", 0, 15, 5)
supp_ca = st.sidebar.number_input("Calcium Citrate Supplement (mg)", 0, 2000, 600, step=100)
exercise_hours = st.sidebar.slider("Daily Rehabilitation & Resistance Exercise (hours)", 0.0, 3.0, 2.0, step=0.5)

# Mineral calculations
food_ca = (goat_milk * 330) + (dates * 6)
total_ca = food_ca + supp_ca
SAFE_LIMIT = 2000

# Safety metrics display
col1, col2, col3 = st.columns(3)
col1.metric("Total Daily Calcium", f"{total_ca} mg", delta=f"{total_ca - SAFE_LIMIT} mg vs Upper Limit", delta_color="inverse")
col2.metric("Post-Lunar BMD (Month 0)", "85.0%", "-15% Lunar Loss")
col3.metric("Earth Baseline Target", "100.0%", "Healthy Control")

if total_ca > SAFE_LIMIT:
    st.error(f"⚠️ Medical Alert: Total daily calcium ({total_ca} mg) exceeds the safe threshold ({SAFE_LIMIT} mg)! High risk of kidney stone formation (hypercalciuria).")
    rate = 0.40
    max_rec = 0.94
else:
    st.success("✅ Mineral balance is optimal and safe for kidneys, supporting maximum bone remineralization rate.")
    # Calculate recovery rate based on exercise and functional nutrition
    rate = 0.35 + (exercise_hours * 0.10) + (0.05 if (goat_milk > 0 and dates > 0) else 0)
    max_rec = 1.00

# 12-month recovery curve calculation
months = list(range(0, 13))
hybrid_density = []
earth_baseline = [100.0] * 13

for m in months:
    if m == 0:
        hybrid_density.append(85.0)
    else:
        rec = (15.0 * max_rec) * (1 - math.exp(-rate * m))
        hybrid_density.append(round(85.0 + rec, 2))

# DataFrame for visualization
df = pd.DataFrame({
    "Month": months,
    "Returning Astronaut BMD (Hybrid Protocol %)": hybrid_density,
    "Earth Control Astronaut BMD (%)": earth_baseline
}).set_index("Month")

st.subheader("📈 12-Month Bone Mineral Density (BMD) Recovery Curve")
st.line_chart(df)

st.subheader("📋 Detailed Monthly Recovery Schedule")
st.dataframe(df.T)
