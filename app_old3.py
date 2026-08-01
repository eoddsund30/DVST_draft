import pandas as pd
import altair as alt
import streamlit as st

df = pd.read_csv("OECD_merged_dataset.csv")

df = df.loc[:, ~df.columns.duplicated()].copy()

df.rename(columns={
    "TIME_PERIOD": "year",
    "Reference area": "country"
}, inplace=True)

df["year"] = pd.to_numeric(df["year"], errors="coerce")
df = df.dropna(subset=["year", "country"]).copy()
df["year"] = df["year"].astype(int)

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

for column in metric_labels:
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

df_time = (
    df.groupby("year", as_index=False)
    .mean(numeric_only=True)
)

st.markdown(
    """
    <h1 style="text-align: center; margin-bottom: 0.2em;">
        🌍 OECD Environmental Indicators Dashboard
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="text-align: center; color: gray;">
        Interactive exploration of environmental and economic indicators
    </p>
    """,
    unsafe_allow_html=True
)

st.sidebar.header("Country Filters")

country_options = ["All Countries"] + sorted(df["country"].unique())

selected_country = st.sidebar.selectbox(
    "Select Country:",
    options=country_options
)

exclude_us = st.sidebar.checkbox(
    "Exclude United States"
)

metric = st.selectbox(
    "Select a variable to display:",
    options=list(metric_labels.keys()),
    format_func=lambda x: metric_labels[x]
)

chart1_data = df_time.dropna(subset=[metric])

chart1 = alt.Chart(chart1_data).mark_line(
    point=True
).encode(
    x=alt.X(
        "year:O",
        title="Year"
    ),
    y=alt.Y(
        f"{metric}:Q",
        title=axis_labels[metric]
    ),
    tooltip=[
        alt.Tooltip(
            "year:O",
            title="Year"
        ),
        alt.Tooltip(
            f"{metric}:Q",
            title=metric_labels[metric],
            format=",.2f"
        )
    ]
).properties(
    height=400,
    title=alt.TitleParams(
        text=f"Global Average {metric_labels[metric]}",
        anchor="middle"
    )
)

st.altair_chart(
    chart1,
    use_container_width=True
)

st.divider()

st.markdown(
    """
    <p style="text-align: center; color: gray;">
        Compare countries for a selected year. Hover over a country to
        temporarily display its historical path, or click the country to
        keep it selected.
    </p>
    """,
    unsafe_allow_html=True
)

comparison_metrics = [
    variable
    for variable in metric_labels
    if variable != "fb_index"
]

comparison_metric = st.selectbox(
    "Select a variable to compare with biodiversity:",
    options=comparison_metrics,
    format_func=lambda x: metric_labels[x]
)

comparison_df = df.copy()

if selected_country != "All Countries":
    comparison_df = comparison_df[
        comparison_df["country"] == selected_country
    ]

elif exclude_us:
    comparison_df = comparison_df[
        comparison_df["country"] != "United States"
    ]

plot_df = comparison_df[
    [
        "year",
        "country",
        comparison_metric,
        "fb_index"
    ]
].dropna().copy()

plot_df = plot_df.rename(columns={
    comparison_metric: "comparison_value",
    "fb_index": "biodiversity"
})

minimum_year = int(plot_df["year"].min())
maximum_year = int(plot_df["year"].max())

selected_year = st.slider(
    "Select Year",
    min_value=minimum_year,
    max_value=maximum_year,
    value=minimum_year,
    step=1
)

x_min = float(plot_df["comparison_value"].min())
x_max = float(plot_df["comparison_value"].max())

y_min = float(plot_df["biodiversity"].min())
y_max = float(plot_df["biodiversity"].max())

x_padding = (x_max - x_min) * 0.05
y_padding = (y_max - y_min) * 0.05

if x_padding == 0:
    x_padding = 1

if y_padding == 0:
    y_padding = 1

x_domain = [
    x_min - x_padding,
    x_max + x_padding
]

y_domain = [
    y_min - y_padding,
    y_max + y_padding
]

hover_country = alt.selection_point(
    name="HoverCountry",
    fields=["country"],
    on="pointerover",
    clear="pointerout",
    empty=False
)

clicked_country = alt.selection_point(
    name="ClickedCountry",
    fields=["country"],
    on="click",
    clear="dblclick",
    empty=False
)

active_country = hover_country | clicked_country

base = alt.Chart(plot_df).encode(
    x=alt.X(
        "comparison_value:Q",
        title=axis_labels[comparison_metric],
        scale=alt.Scale(
            domain=x_domain,
            zero=False
        )
    ),
    y=alt.Y(
        "biodiversity:Q",
        title="Biodiversity",
        scale=alt.Scale(
            domain=y_domain,
            zero=False
        )
    )
)

country_paths = base.mark_line(
    strokeWidth=3
).encode(
    detail=alt.Detail("country:N"),
    order=alt.Order("year:O"),
    color=alt.value("steelblue"),
    opacity=alt.condition(
        active_country,
        alt.value(0.75),
        alt.value(0)
    )
)

historical_points = base.mark_circle(
    size=35
).encode(
    color=alt.value("steelblue"),
    opacity=alt.condition(
        active_country,
        alt.value(0.6),
        alt.value(0)
    ),
    tooltip=[
        alt.Tooltip(
            "country:N",
            title="Country"
        ),
        alt.Tooltip(
            "year:O",
            title="Year"
        ),
        alt.Tooltip(
            "comparison_value:Q",
            title=metric_labels[comparison_metric],
            format=",.2f"
        ),
        alt.Tooltip(
            "biodiversity:Q",
            title="Biodiversity",
            format=".2f"
        )
    ]
)

year_points = base.transform_filter(
    alt.datum.year == selected_year
).mark_circle(
    size=130,
    stroke="white",
    strokeWidth=1
).encode(
    color=alt.condition(
        active_country,
        alt.value("steelblue"),
        alt.value("lightgray")
    ),
    opacity=alt.condition(
        active_country,
        alt.value(1),
        alt.value(0.8)
    ),
    tooltip=[
        alt.Tooltip(
            "country:N",
            title="Country"
        ),
        alt.Tooltip(
            "year:O",
            title="Year"
        ),
        alt.Tooltip(
            "comparison_value:Q",
            title=metric_labels[comparison_metric],
            format=",.2f"
        ),
        alt.Tooltip(
            "biodiversity:Q",
            title="Biodiversity",
            format=".2f"
        )
    ]
)

country_labels = base.transform_filter(
    alt.datum.year == selected_year
).transform_filter(
    active_country
).mark_text(
    dy=-14,
    fontSize=12,
    fontWeight="bold"
).encode(
    text=alt.Text("country:N"),
    color=alt.value("black")
)

scatter = alt.layer(
    country_paths,
    historical_points,
    year_points,
    country_labels
).add_params(
    hover_country,
    clicked_country
).properties(
    height=500,
    title=alt.TitleParams(
        text=(
            f"{axis_labels[comparison_metric]} "
            f"vs Biodiversity ({selected_year})"
        ),
        subtitle=[
            "Hover to view a country's historical path.",
            "Click to retain a country and double-click to clear it.",
            "The axes remain fixed when the year changes."
        ],
        anchor="middle"
    )
)

trend_metric = st.selectbox(
    "Select a variable for the country change-over-time chart:",
    options=list(metric_labels.keys()),
    format_func=lambda x: metric_labels[x]
)

trend_df = comparison_df[
    [
        "year",
        "country",
        trend_metric
    ]
].dropna().copy()

trend_df = trend_df.rename(columns={
    trend_metric: "trend_value"
})

trend_min = float(trend_df["trend_value"].min())
trend_max = float(trend_df["trend_value"].max())

trend_padding = (trend_max - trend_min) * 0.05

if trend_padding == 0:
    trend_padding = 1

trend_domain = [
    trend_min - trend_padding,
    trend_max + trend_padding
]

trend = alt.Chart(trend_df).transform_filter(
    active_country
).mark_line(
    point=True,
    strokeWidth=3
).encode(
    x=alt.X(
        "year:O",
        title="Year"
    ),
    y=alt.Y(
        "trend_value:Q",
        title=axis_labels[trend_metric],
        scale=alt.Scale(
            domain=trend_domain,
            zero=False
        )
    ),
    color=alt.Color(
        "country:N",
        legend=None
    ),
    tooltip=[
        alt.Tooltip(
            "country:N",
            title="Country"
        ),
        alt.Tooltip(
            "year:O",
            title="Year"
        ),
        alt.Tooltip(
            "trend_value:Q",
            title=metric_labels[trend_metric],
            format=",.2f"
        )
    ]
).properties(
    height=320,
    title=alt.TitleParams(
        text=(
            f"{metric_labels[trend_metric]} "
            "Change Over Time"
        ),
        subtitle=(
            "Hover over or click a country in the scatterplot "
            "to display its trend."
        ),
        anchor="middle"
    )
)

coordinated_charts = alt.vconcat(
    scatter,
    trend,
    spacing=40
).resolve_scale(
    color="independent"
).configure_axis(
    gridOpacity=0.25
).configure_view(
    stroke=None
)

st.altair_chart(
    coordinated_charts,
    use_container_width=True
)

st.caption(
    "The second visualization uses axis ranges calculated from all "
    "available years, preventing the scale from changing as the year "
    "slider moves."
)