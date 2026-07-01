import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# ----------------------------
# Page setup
# ----------------------------

st.set_page_config(
    page_title="Fourth Down Decision Dashboard",
    page_icon="🏈",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "v1_fourth_down_fbs_dataset.csv"
INDEX_PATH = BASE_DIR / "data" / "v1_team_aggressiveness_index.csv"
DECK_DIR = BASE_DIR / "deck"

ND_BLUE = "#0C2340"
ND_GOLD = "#C99700"
DARK_GRAY = "#333333"

distance_order = ["1", "2", "3-4", "5-7", "8+"]
field_order = ["own_territory", "midfield", "opponent_territory", "red_zone"]

field_labels = {
    "own_territory": "Own Territory",
    "midfield": "Midfield",
    "opponent_territory": "Opponent Territory",
    "red_zone": "Red Zone"
}

decision_colors = {
    "punt": "#9E9E9E",
    "field_goal": ND_GOLD,
    "go_for_it": ND_BLUE
}

# ----------------------------
# Load data
# ----------------------------

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    team_index = pd.read_csv(INDEX_PATH)

    if "rank" in team_index.columns:
        team_index = team_index.sort_values("rank")

    return df, team_index

df, team_index = load_data()

# ----------------------------
# Helper functions
# ----------------------------

def decision_rate_table(data, group_col):
    counts = (
        data
        .groupby([group_col, "decision"])
        .size()
        .unstack(fill_value=0)
    )

    pct = counts.div(counts.sum(axis=1), axis=0)

    for col in ["punt", "field_goal", "go_for_it"]:
        if col not in pct.columns:
            pct[col] = 0

    return pct


def format_index_table(table):
    display = table.copy()

    for col in ["actual_go_rate", "expected_go_rate"]:
        if col in display.columns:
            display[col] = display[col].map(lambda x: f"{x:.1%}")

    if "aggressiveness_index" in display.columns:
        display["aggressiveness_index"] = display["aggressiveness_index"].map(lambda x: f"{x:+.3f}")

    return display


def plot_stacked(pct_df, title, order=None, labels=None):
    if order:
        pct_df = pct_df.loc[[x for x in order if x in pct_df.index]]

    if labels:
        pct_df = pct_df.copy()
        pct_df.index = [labels.get(x, x) for x in pct_df.index]

    cols = ["punt", "field_goal", "go_for_it"]

    fig, ax = plt.subplots(figsize=(9, 5))

    pct_df[cols].plot(
        kind="bar",
        stacked=True,
        ax=ax,
        color=[decision_colors[c] for c in cols]
    )

    ax.set_title(title, fontsize=14, weight="bold")
    ax.set_ylabel("Share of Decisions")
    ax.set_xlabel("")
    ax.set_ylim(0, 1)

    ticks = np.arange(0, 1.1, 0.2)
    ax.set_yticks(ticks)
    ax.set_yticklabels([f"{int(x*100)}%" for x in ticks])

    ax.grid(axis="y", alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(["Punt", "Field Goal", "Go For It"], loc="upper right")

    plt.tight_layout()
    return fig


def plot_go_comparison(national_pct, team_pct, order, title, labels=None):
    comparison = pd.DataFrame({
        "National": national_pct["go_for_it"],
        "Selected Team": team_pct["go_for_it"]
    })

    comparison = comparison.loc[[x for x in order if x in comparison.index]]

    if labels:
        comparison = comparison.copy()
        comparison.index = [labels.get(x, x) for x in comparison.index]

    fig, ax = plt.subplots(figsize=(9, 5))

    comparison.plot(
        kind="bar",
        ax=ax,
        color=[DARK_GRAY, ND_BLUE]
    )

    ax.set_title(title, fontsize=14, weight="bold")
    ax.set_ylabel("Go-For-It Rate")
    ax.set_xlabel("")
    ax.set_ylim(0, 1)

    ticks = np.arange(0, 1.1, 0.2)
    ax.set_yticks(ticks)
    ax.set_yticklabels([f"{int(x*100)}%" for x in ticks])

    ax.grid(axis="y", alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    return fig

# ----------------------------
# Sidebar
# ----------------------------

st.sidebar.title("Controls")

teams = sorted(df["offense"].dropna().unique())
default_team = "Notre Dame" if "Notre Dame" in teams else teams[0]

selected_team = st.sidebar.selectbox(
    "Select Team",
    teams,
    index=teams.index(default_team)
)

team_df = df[df["offense"] == selected_team].copy()
team_row = team_index[team_index["offense"] == selected_team]

# ----------------------------
# Header
# ----------------------------

st.title("🏈 Fourth Down Decision Dashboard")

st.markdown(
    """
    This Version 1 dashboard explores **FBS fourth-down decision-making from 2023–2025**.
    It compares national tendencies, selected-team behavior, Notre Dame-specific trends, and a simple
    context-adjusted Aggressiveness Index.
    """
)

with st.expander("Project Summary", expanded=True):
    st.markdown(
        """
        **Research question:** When do college football teams choose aggression on fourth down?

        **Dataset:** 2023–2025 FBS play-by-play data.

        **Decision categories:** Punt, field goal, or go-for-it.

        **Aggressiveness Index:** Actual Go Rate − Expected Go Rate, where expected go rate is based on
        national FBS behavior in similar distance and field-position situations.
        """
    )

# ----------------------------
# Key findings
# ----------------------------

st.subheader("Key Findings")

k1, k2, k3 = st.columns(3)

with k1:
    st.info("Teams go for it **74.6%** of the time on 4th & 1, but only **30.7%** on 4th & 3–4.")

with k2:
    st.info("Midfield is the most conservative zone: teams punt **72.7%** of the time.")

with k3:
    st.info("Notre Dame ranks **36th** in the Version 1 Aggressiveness Index.")

# ----------------------------
# PowerPoint deck reference
# ----------------------------

pptx_files = list(DECK_DIR.glob("*.pptx"))

if pptx_files:
    deck_path = pptx_files[0]
    with open(deck_path, "rb") as f:
        st.download_button(
            label="Download PowerPoint Deck",
            data=f,
            file_name=deck_path.name,
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
else:
    st.caption("PowerPoint deck not found in the deck/ folder.")

st.divider()

# ----------------------------
# Team profile
# ----------------------------

st.header(f"{selected_team} Profile")

col1, col2, col3, col4 = st.columns(4)

team_decisions = len(team_df)
team_go_rate = (team_df["decision"] == "go_for_it").mean()

col1.metric("Fourth-Down Decisions", f"{team_decisions:,}")
col2.metric("Go-For-It Rate", f"{team_go_rate:.1%}")

if not team_row.empty:
    rank = int(team_row.iloc[0]["rank"])
    index_value = team_row.iloc[0]["aggressiveness_index"]
    expected_rate = team_row.iloc[0]["expected_go_rate"]

    col3.metric("Aggressiveness Rank", f"#{rank}")
    col4.metric("Aggressiveness Index", f"{index_value:+.3f}")

    st.caption(
        f"{selected_team}'s actual go rate is {team_go_rate:.1%}. "
        f"The expected go rate based on distance and field position is {expected_rate:.1%}."
    )
else:
    col3.metric("Aggressiveness Rank", "N/A")
    col4.metric("Aggressiveness Index", "N/A")

# ----------------------------
# Tables and charts
# ----------------------------

national_distance = decision_rate_table(df, "distance_bucket")
team_distance = decision_rate_table(team_df, "distance_bucket")

national_field = decision_rate_table(df, "field_zone")
team_field = decision_rate_table(team_df, "field_zone")

tab1, tab2, tab3, tab4 = st.tabs([
    "Team Profile",
    "National Comparison",
    "Aggressiveness Index",
    "Raw Plays"
])

with tab1:
    c1, c2 = st.columns(2)

    with c1:
        st.pyplot(
            plot_stacked(
                team_distance,
                f"{selected_team}: Decisions by Distance",
                order=distance_order
            )
        )

    with c2:
        st.pyplot(
            plot_stacked(
                team_field,
                f"{selected_team}: Decisions by Field Position",
                order=field_order,
                labels=field_labels
            )
        )

with tab2:
    c1, c2 = st.columns(2)

    with c1:
        st.pyplot(
            plot_go_comparison(
                national_distance,
                team_distance,
                distance_order,
                f"{selected_team} vs National: Go Rate by Distance"
            )
        )

    with c2:
        st.pyplot(
            plot_go_comparison(
                national_field,
                team_field,
                field_order,
                f"{selected_team} vs National: Go Rate by Field Position",
                labels=field_labels
            )
        )

with tab3:
    top_cols = [
        "rank",
        "offense",
        "fourth_down_decisions",
        "actual_go_rate",
        "expected_go_rate",
        "aggressiveness_index"
    ]

    st.subheader("Most Aggressive FBS Teams")
    st.dataframe(
        format_index_table(team_index.head(15)[top_cols]),
        width="stretch"
    )

    st.subheader("Most Conservative FBS Teams")
    st.dataframe(
        format_index_table(team_index.tail(15)[top_cols]),
        width="stretch"
    )

    st.subheader(f"{selected_team} Ranking")

    if not team_row.empty:
        st.dataframe(
            format_index_table(team_row[top_cols]),
            width="stretch"
        )
    else:
        st.write("No ranking available for this team.")

with tab4:
    st.dataframe(
        team_df[
            [
                "season",
                "week",
                "offense",
                "defense",
                "period",
                "distance",
                "yardsToGoal",
                "decision",
                "yardsGained",
                "playType",
                "playText"
            ]
        ],
        width="stretch"
    )

st.divider()

st.markdown(
    """
    **Version 1 scope:** This dashboard is intentionally descriptive. Future versions could add expected value modeling,
    coach-level rankings, similar-play search, and machine-learning decision models.
    """
)
