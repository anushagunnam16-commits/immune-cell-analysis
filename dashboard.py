import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Immune Cell Analysis",
    layout="wide"
)

st.title("Immune Cell Population Analysis")

st.write(
    "Interactive dashboard for analyzing immune cell populations "
    "and treatment response."
)


# --------------------------------------------------
# PART 2 - CELL FREQUENCY OVERVIEW
# --------------------------------------------------

st.header("Part 2: Cell Population Frequencies")

frequencies = pd.read_csv("cell_frequencies.csv")

st.write(
    "Relative frequency of each immune cell population "
    "for every biological sample."
)

st.dataframe(
    frequencies,
    use_container_width=True
)


# --------------------------------------------------
# PART 3 - STATISTICAL ANALYSIS
# --------------------------------------------------

st.header("Part 3: Miraclib Treatment Response")

st.write(
    "Comparison of immune cell relative frequencies between "
    "responders and non-responders among melanoma patients "
    "receiving Miraclib using PBMC samples."
)

stats = pd.read_csv("statistical_results.csv")

st.subheader("Statistical Results")

st.dataframe(
    stats,
    use_container_width=True
)


# Significant populations
significant = stats[
    stats["significant_after_correction"] == True
]

st.subheader("Significant Cell Populations")

if significant.empty:

    st.write(
        "No cell populations showed a statistically "
        "significant difference."
    )

else:

    for _, row in significant.iterrows():

        st.success(
            f"{row['population']} showed a significant difference "
            f"between responders and non-responders "
            f"(adjusted p-value = {row['adjusted_p_value']:.4f})."
        )


# --------------------------------------------------
# PART 3 - BOXPLOTS
# --------------------------------------------------

st.subheader("Responder vs Non-responder Boxplots")

cell_types = [
    "b_cell",
    "cd8_t_cell",
    "cd4_t_cell",
    "nk_cell",
    "monocyte"
]

selected_cell = st.selectbox(
    "Select a cell population:",
    cell_types
)

boxplot_file = f"{selected_cell}_boxplot.png"

st.image(
    boxplot_file,
    caption=f"{selected_cell}: Responders vs Non-responders"
)


# --------------------------------------------------
# PART 4 - SUBSET ANALYSIS
# --------------------------------------------------

st.header("Part 4: Baseline Subset Analysis")

st.write(
    "Melanoma PBMC samples collected at baseline "
    "(time from treatment start = 0) from patients "
    "treated with Miraclib."
)


col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Total Baseline Samples",
        "656"
    )

with col2:

    st.metric(
        "Responders",
        "331"
    )

with col3:

    st.metric(
        "Non-responders",
        "325"
    )


col4, col5 = st.columns(2)

with col4:

    st.metric(
        "Female Subjects",
        "312"
    )

with col5:

    st.metric(
        "Male Subjects",
        "344"
    )


st.subheader("Samples by Project")

project_data = pd.DataFrame({
    "Project": ["prj1", "prj3"],
    "Samples": [384, 272]
})

st.dataframe(
    project_data,
    use_container_width=True
)


# --------------------------------------------------
# FINAL B-CELL QUESTION
# --------------------------------------------------

st.subheader("Average B-cell Count")

st.metric(
    "Male Melanoma Responders at Time 0",
    "10206.15"
)


# --------------------------------------------------
# QUINTAZIDE NOTE
# --------------------------------------------------

st.info(
    "Quintazide was considered as an additional treatment of "
    "interest for future subset analyses. It is not present in "
    "the supplied dataset, so no quintazide-specific results "
    "are reported."
)