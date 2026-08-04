import pandas as pd
import altair as alt
import streamlit as st
import base64

#helper function
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

df = pd.read_csv("OECD_merged_dataset.csv")

df = df.loc[:, ~df.columns.duplicated()].copy()

df.rename(columns={
    "TIME_PERIOD": "year",
    "Reference area": "country"
}, inplace=True)

df["year"] = pd.to_numeric(df["year"], errors="coerce")
df = df.dropna(subset=["year", "country"]).copy()
df["year"] = df["year"].astype(int)

#increase dropdown + slider font sizes
st.markdown("""
<style>
div[data-baseweb="select"] * {
    font-size:18px !important;
}

div[data-testid="stSlider"] * {
    font-size:18px !important;
}

label {
    font-size:18px !important;
    font-weight:600 !important;
}
</style>
""", unsafe_allow_html=True)

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

tab1, tab2, tab3 = st.tabs(
    [
        "📖 Introduction",
        "🌍 Indicator Explorer",
        "🌎 Country Comparison"
    ]
)

with tab1:

    img = get_base64_image(
        "images/intro_background.jpg"
    )

    st.markdown(
        f"""
        <div style="
            background-image: linear-gradient(
                rgba(0,0,0,0.45),
                rgba(0,0,0,0.45)
            ),
            url('data:image/jpg;base64,{img}');
            background-size: cover;
            background-position: center;
            height: 350px;
            border-radius: 15px;
            text-align: center;
        ">

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <h1 style="
            text-align:center;
            margin-top:-230px;
            color:white;
            font-size:42px;
        ">
            🌍 OECD Environmental Indicators Dashboard
        </h1>

        <div style="
            text-align:center;
            color:white;
            font-size:22px;
        ">
            Interactive exploration of environmental change across OECD countries
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        ## Overview

        This dashboard provides an interactive exploration of environmental
        indicators across OECD (Organization for Economic Co-operation and Development) countries over time.

        Users can examine trends in biodiversity, greenhouse gas emissions,
        energy consumption, land use, freshwater use, and agricultural
        indicators.
        """
    )

    st.image(
        "images/world_map.jpg",
        use_container_width=True
    )

    st.markdown(
        """
        ## Environmental Indicators

        The dashboard explores six key environmental indicators.
        These measurements provide insight into biodiversity,
        resource consumption, and environmental pressures across OECD countries.
        """
    )

    indicator_table = pd.DataFrame({
        "Indicator": [
            "Biodiversity",
            "Agricultural Greenhouse Gas Emissions",
            "Agricultural Land Area",
            "Energy Use",
            "Land Use",
            "Freshwater Use"
        ],
        "Measurement": [
            "Wild Bird Index",
            "Tonnes of CO₂ (thousands)",
            "Hectares",
            "Tonnes of oil equivalent (thousands)",
            "Square kilometers",
            "Cubic meters (millions)"
        ],
        "Description": [
            "Tracks changes in bird populations as an indicator of ecosystem health.",
            "Measures greenhouse gas emissions associated with agricultural activities.",
            "Measures total agricultural land area. One hectare equals approximately 2.5 acres.",
            "Measures energy consumption using oil-equivalent units for comparison across sources.",
            "Represents total land area associated with environmental indicators.",
            "Measures freshwater consumption and demand on water resources."
        ]
    })

    st.dataframe(
        indicator_table,
        hide_index=True,
        use_container_width=True
    )

    st.image(
        "images/biodiversity.jpg",
        use_container_width=True
    )

    st.markdown(
        """
        ## Understanding the Environmental Indicators

        The dashboard explores six environmental indicators that capture
        biodiversity, resource use, and environmental pressures across OECD countries.
        """
    )

    card_col1, card_col2, card_col3 = st.columns(3)

    with card_col1:
        st.markdown(
            """
            ### 🌿 Biodiversity

            **Wild Bird Index**

            Tracks changes in bird populations as an indicator of ecosystem health.
            """
        )

    with card_col2:
        st.markdown(
            """
            ### 💨 Emissions

            **Agricultural GHG Emissions**

            Measures agricultural greenhouse gas emissions in tonnes of CO₂.
            """
        )

    with card_col3:
        st.markdown(
            """
            ### ⚡ Energy

            **Energy Use**

            Measures energy consumption using tonnes of oil equivalent.
            """
        )


    card_col4, card_col5, card_col6 = st.columns(3)

    with card_col4:
        st.markdown(
            """
            ### 🌾 Agriculture

            **Agricultural Land Area**

            Measures agricultural land coverage in hectares.
            """
        )

    with card_col5:
        st.markdown(
            """
            ### 🗺️ Land Use

            **Total Land Area**

            Represents land use measured in square kilometers.
            """
        )

    with card_col6:
        st.markdown(
            """
            ### 💧 Freshwater

            **Water Use**

            Measures freshwater consumption in cubic meters.
            """
        )


    st.image(
        "images/env_monitoring.jpg",
        use_container_width=True
    )
        
    st.markdown(
        """
        ## How to Use This Dashboard

        **Global Trends**
        - Use the first dropdown to explore worldwide average trends for
          different environmental indicators.

        **Country Explorer**
        - Use the scatter plot to compare countries across environmental
          dimensions.
        - Hover over or click countries to reveal their historical paths.

        **Country Timeline**
        - Select a variable to view how a country's indicator changes
          over time.

        ## Data Source

        Data used in this dashboard are derived from OECD environmental
        indicator datasets.

        Source:
        [OECD Data Explorer](https://www.oecd.org/en/data/datasets.html?orderBy=mostRelevant&page=3&facetTags=oecd-languages%3Aen%2Coecd-policy-areas%3Apa8%2Coecd-policy-areas%3Apa13%2Coecd-policy-areas%3Apa1%2Coecd-policy-areas%3Apa2)

        The **Organisation for Economic Co-operation and Development (OECD)** is an international organization that works with more than 100 countries and partners to promote policies that improve economic prosperity, environmental sustainability, and quality of life. The OECD collects and publishes high-quality, internationally comparable data to support evidence-based decision-making across a wide range of topics, including the environment, education, health, and the economy.


        Indicators were aggregated across available countries and years to
        support exploratory visualization and comparison.
        """
    )

with tab2:
    st.markdown(
    """
    <h1 style="text-align: center; margin-bottom: 0.2em;">
        🌍 OECD Indicator Exploration
    </h1>
    """,
    unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="text-align: center; color: gray;">
            Explore global environmental indicators through interactive visualizations. Compare variables, adjust the year, and examine country-level trends over time.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.header("Country Filters")

    st.sidebar.markdown(
    """
    <p style="font-size:14px; color:gray;">
        Use this selection box in the Dashboard Explorer tab.
    </p>
    """,
    unsafe_allow_html=True
    )

    country_options = ["All Countries"] + sorted(df["country"].unique())

    selected_country = st.sidebar.selectbox(
        "Select Country:",
        options=country_options
    )

    exclude_us = st.sidebar.checkbox(
        "Exclude United States (outlier)"
    )

    exclude_canada = st.sidebar.checkbox(
        "Exclude Canada (outlier)"
    )

    metric = st.selectbox(
        "Select a variable to display:",
        options=list(metric_labels.keys()),
        format_func=lambda x: metric_labels[x]
    )

    chart1_data = df_time.dropna(subset=[metric])

    chart1 = (
        alt.Chart(chart1_data)
        .mark_line(point=True)
        .encode(
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
        )
        .properties(
            height=400,
            title=alt.TitleParams(
                text=f"Global Average {metric_labels[metric]}",
                anchor="middle"
            )
        )
        .configure_axis(
            labelFontSize=14,
            titleFontSize=18,
            titleFontWeight="bold"
        )
        .configure_title(
            fontSize=22,
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
        "Scatter plot dropdown: select a variable to compare with biodiversity in the SCATTER PLOT:",
        options=comparison_metrics,
        format_func=lambda x: metric_labels[x]
    )

    comparison_df = df.copy()

    if selected_country != "All Countries":
        comparison_df = comparison_df[
            comparison_df["country"] == selected_country
        ]

    else:
        if exclude_us:
            comparison_df = comparison_df[
                comparison_df["country"] != "United States"
            ]

        if exclude_canada:
            comparison_df = comparison_df[
                comparison_df["country"] != "Canada"
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
        "Select Year: this only changes the scatter plot's display",
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
        dy=-16,
        fontSize=15,
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
        "Change Over Time dropdown: select a variable for the COUNTRY TIMELINE chart (this selection only affects the line chart BELOW the scatterplot)",
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
        gridOpacity=0.25,
        labelFontSize=14,
        titleFontSize=18,
        titleFontWeight="bold"
    ).configure_title(
        fontSize=22,
        anchor="middle"
    ).configure_legend(
        titleFontSize=16,
        labelFontSize=14
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

with tab3:                          
    st.markdown(
        """
        <h1 style="text-align:center;">
        🌎 Country Comparison
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="text-align:center; color:gray;">
        Compare how environmental indicators have changed over time
        between two selected countries.
        </p>
        """,
        unsafe_allow_html=True
    )

    compare_col1, compare_col2 = st.columns(2)

    country_options = sorted(df["country"].unique())

    with compare_col1:
        country_1 = st.selectbox(
            "Select first country (blue):",
            options=country_options
        )

    with compare_col2:
        country_2 = st.selectbox(
            "Select second country (red):",
            options=country_options,
            index=1
        )


    def create_comparison_chart(variable, country_1, country_2):

        comparison = df[
            df["country"].isin(
                [country_1, country_2]
            )
        ][
            [
                "year",
                "country",
                variable
            ]
        ].dropna()

        chart = alt.Chart(comparison).mark_line(
            point=True,
            strokeWidth=3
        ).encode(
            x=alt.X(
                "year:O",
                title="Year"
            ),
            y=alt.Y(
                f"{variable}:Q",
                title=axis_labels[variable]
            ),
            color=alt.Color(
                "country:N",
                scale=alt.Scale(
                    domain=[country_1, country_2],
                    range=["steelblue", "firebrick"]
                ),
                legend=alt.Legend(title="Country")
            ),
            tooltip=[
                "country",
                "year",
                alt.Tooltip(
                    f"{variable}:Q",
                    format=",.2f"
                )
            ]
        ).properties(
            height=250,
            title=metric_labels[variable]
        )

        return chart

    comparison_charts = [
        create_comparison_chart(
            variable,
            country_1,
            country_2
        )
        for variable in metric_labels
    ]


    for chart in comparison_charts:
        st.altair_chart(
            chart,
            use_container_width=True
        )
