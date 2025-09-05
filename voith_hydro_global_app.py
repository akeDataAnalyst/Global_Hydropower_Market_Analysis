import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration

st.set_page_config(
    page_title="Global Hydropower Market Analysis",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Load Data

# Use Streamlit's cache decorator to load data only once
@st.cache_data
def load_data():
    market_trends_df = pd.read_csv("synthetic_iea_hydropower_data.csv")
    growth_potential_df = pd.read_csv("growth_potential_recommendations.csv")
    competitor_analysis_df = pd.read_csv("voith_hydro_competition_analysis.csv")
    return market_trends_df, growth_potential_df, competitor_analysis_df

market_trends_df, growth_potential_df, competitor_analysis_df = load_data()

# 3. Build the Application Layout

st.title("Voith Hydro: Global Market Growth Strategy 📈")

# Add a "hider button" using an expander widget
with st.expander("Show/Hide Executive Summary"):
    st.markdown("### Executive Summary")
    st.write(
        """
        This interactive dashboard presents a comprehensive market analysis to identify strategic growth opportunities for Voith Hydro. 
        The analysis combines global market data, a custom growth potential index, and a detailed competitor overview to inform business development decisions for the 2024-2025 period.
        """
    )

# Use radio buttons for main page navigation in the main content area
page = st.radio("Go to:", ["Market Analysis", "Competitor Overview"], horizontal=True)

if page == "Market Analysis":
    st.header("Global Market Analysis & Growth Opportunities")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Global Hydropower Trends (Capacity & Generation)")
        # Filter out non-country rows for more accurate trends
        global_trends_df = market_trends_df[~market_trends_df['country'].isin(['Africa Eastern and Southern', 'Africa Western and Central', 'Albania', 'Algeria', 'Angola'])].groupby('year').sum(numeric_only=True).reset_index()
        
        # Melt the DataFrame to create a single column for both capacity and generation trends
        melted_trends_df = global_trends_df.melt(
            id_vars=["year"],
            value_vars=["hydropower_capacity_gw", "hydropower_generation_twh"],
            var_name="Trend Type",
            value_name="Value"
        )
        
        # Create a line chart with two trends
        fig = px.line(
            melted_trends_df,
            x="year",
            y="Value",
            color="Trend Type",
            title="Global Hydropower Capacity and Generation Trends",
            labels={
                "Value": "Value (GW or TWh)",
                "Trend Type": "Trend"
            }
        )
        
        # Update the y-axis to be more descriptive
        fig.update_yaxes(title_text="Value (GW for Capacity, TWh for Generation)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Top Recommended Countries for Expansion")
        # Use a radio button to toggle between table and map view
        view_option = st.radio("Select View", ["Data Table", "World Map"], horizontal=True)
        
        if view_option == "Data Table":
            # Display the table of top countries
            st.dataframe(
                growth_potential_df.sort_values(
                    by="growth_score", ascending=False
                ).head(10),
                use_container_width=True,
                hide_index=True
            )
            st.write("This table shows the top countries ranked by our custom growth potential index.")
        else:
            # Create a world map, colored by growth score
            fig_map = px.choropleth(
                growth_potential_df,
                locations="country_name",
                locationmode="country names",
                color="growth_score",
                hover_name="country_name",
                color_continuous_scale=px.colors.sequential.Viridis,
                title="Top Recommended Countries by Growth Score",
            )
            st.plotly_chart(fig_map, use_container_width=True)
            st.write("This section shows the top countries ranked by our custom growth potential index.")

elif page == "Competitor Overview":
    st.header("Competitor Landscape")
    st.markdown("---")

    st.subheader("Key Competitors & Strategic Positioning")
    # Display the full competitor analysis table
    st.dataframe(
        competitor_analysis_df,
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown(
        "---"
    )

    # Use a multiselect filter in the main content area to highlight competitors
    competitor_filter = st.multiselect(
        "Select Competitors to Highlight",
        competitor_analysis_df["Competitor Name"].unique(),
        ["Voith Hydro", "GE Renewable Energy", "Siemens Energy"],
    )
    
    st.subheader("Selected Competitors' Key Services")
    filtered_df = competitor_analysis_df[
        competitor_analysis_df["Competitor Name"].isin(competitor_filter)
    ]
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
