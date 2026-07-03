import pandas as pd
import altair as alt
import seaborn as sns
import streamlit as st

df = pd.read_csv('OECD_merged_dataset.csv')

#change variable names
df.rename(columns={'TIME_PERIOD': 'year'}, inplace=True)
df.rename(columns={'Reference area': 'country'}, inplace=True)

if "selected_country" not in st.session_state:
    st.session_state.selected_country = df["country"].iloc[0]

df_time = df.groupby('year', as_index=False).mean(numeric_only=True)

metric_labels = {
    "fb_index": "Biodiversity (wild bird index)",
    "tonnes_CO2": "Agricultural Greenhouse Gas Emissions (tonnes, thousands)",
    "hectares": "Agricultural Land Area (hectares)",
    "tonnes_oil": "Energy Use (tonnes, thousands)",
    "sq_km": "Land Use (sq km)",
    "cubic_m": "Freshwater Use (cubic meters, millions)"
}

axis_labels = {
    "fb_index": "Biodiversity",
    "tonnes_CO2": "GHG Emissions",
    "hectares": "Land Area",
    "tonnes_oil": "Energy Use",
    "sq_km": "Land Use",
    "cubic_m": "Freshwater Use"
}

#st.title("OECD Environmental Indicators Dashboard")

st.markdown(
    "<h1 style='text-align: center; margin-bottom: 0.2em;'>🌍 OECD Environmental Indicators Dashboard</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; color: gray;'>Interactive exploration of environmental and economic indicators</p>",
    unsafe_allow_html=True
)

metric = st.selectbox(
    "Select a variable to display:",
    options=list(metric_labels.keys()),
    format_func=lambda x: metric_labels[x]
)

#Chart 1
chart1 = alt.Chart(df_time).mark_line(point=True).encode(
    x=alt.X("year:O", title="Year"),
    y=alt.Y(f"{metric}:Q", title=axis_labels[metric]),
    tooltip=[
        alt.Tooltip("year:O", title="Year"),
        alt.Tooltip(f"{metric}:Q", title=metric_labels[metric], format=".2f")
    ]
).properties(
    title=alt.TitleParams(
        text=f"Global Average {metric_labels[metric]} (1990–2025)",
        anchor="middle"
    )
)

st.altair_chart(chart1, use_container_width=True)
st.divider()

#Chart 2
#year slider
year = st.slider(
    "Select Year",
    int(df["year"].min()),
    int(df["year"].max()),
    int(df["year"].min())
)

#filter the dataset
df_year = df[df["year"] == year]

#build scatterplot with click interaction
country_select = alt.selection_point(fields=["country"])

chart2 = alt.Chart(df_year).mark_circle(size=120).encode(
    x=alt.X(f"{metric}:Q", title=axis_labels[metric]),
    y=alt.Y("fb_index:Q", title="Biodiversity"),
    color=alt.condition(country_select, alt.value("steelblue"), alt.value("lightgray")),
    tooltip=[
        "country",
        "year",
        alt.Tooltip(f"{metric}:Q", format=".2f"),
        alt.Tooltip("fb_index:Q", format=".2f")
    ]
).add_params(
    country_select
).properties(
    title=alt.TitleParams(
        text=f"{axis_labels[metric]} vs Biodiversity ({year})",
        anchor="middle"
    )
)

st.altair_chart(chart2, use_container_width=True)
st.divider()

# Chart 3 (fixed + stable)

countries = df["country"].unique()

selected_country = st.selectbox(
    "Select Country for Trend View",
    countries
)

df_country = df[df["country"] == selected_country]

chart3 = alt.Chart(df_country).mark_line(point=True).encode(
    x=alt.X("year:Q", title="Year"),
    y=alt.Y("fb_index:Q", title="Biodiversity"),
    tooltip=["country", "year", "fb_index"]
).properties(
    title=alt.TitleParams(
        text=f"Biodiversity Trend: {selected_country}",
        anchor="middle"
    )
)

st.altair_chart(chart3, use_container_width=True)
