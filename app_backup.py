import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

st.set_page_config(
    page_title="Fourth Down Decision Dashboard",
    page_icon="🏈",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "v1_fourth_down_fbs_dataset.csv"
INDEX_PATH = BASE_DIR / "data" / "v1_team_aggressiveness_index.csv"

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

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    team_index = pd.read_csv(INDEX_PATH)
    return df, team_index

df, team_index = load_data()

def decision_rate_table(data, group_col):
    counts = (
        data
        .groupby([group_col, "decision"])
        .size()
        .unstack(fill_value=0)
    )
    return counts.div(counts.sum(axis=1), axis=0)

def plot_stacked(pct_df, title, order=None, labels=None):
    if order:
        pct_df = pct_df.loc[[x for x in order if x in pct_df.index]]

    if labels:
        pct_df = pct_df.copy()
        pct_df.index = [labels.get(x, x) for x in pct_df.index]

    cols = [c for c in ["punt", "field_goal", "go_for_it"] if c in pct_df.columns]

    fig, ax = plt.subplots(figsize=(9, 5))

    pct_df[cols].plot(
        kind="bar",
        stacked=True,
        ax=ax,
        color=[decision_colors[c] for c in cols]
    )

    ax.set_title(title, fontsize=14, weight="bold")
    ax.set_ylabel("Share of Decisions")
    ax.set_ylim(0, 1)
    ax.set_yticks(np.arange(0, 1.1, 0.2))
    ax.set_yticklabels([f"{int(x*100)}%" for x in np.arange(0, 1.1, 0.2)])
    ax.grid(axis="y", alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(["Punt", "Field Goal", "Go For It"])

    plt.tight_layout()
    return fig

st.title("🏈 Fourth Down Decision Dashboard")

st.markdown(
    """
    This dashboard summarizes FBS fourth-down decision-making from the 2023–2025 seasons.
    It compares national tendencies, selected-team behavior, and a simple Aggressiveness Index.
    """
)

teams = sorted(df["offense"].dropna().unique())
default_team = "Notre Dame" if "Notre Dame" in teams else teams[0]

selected_team = st.sidebar.selectbox(
    "Select Team",
    teams,
    index=teams.index(default_team)
)

team_df = df[df["offense"] == selected_team].copy()
team_row = team_index[team_index["offense"] == selected_team]

st.header(selected_team)

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

st.divider()

national_distance = decision_rate_table(df, "distance_bucket")
team_distance = decision_rate_table(team_df, "distance_bucket")

national_field = decision_rate_table(df, "field_zone")
team_field = decision_rate_table(team_df, "field_zone")

tab1, tab2, tab3 = st.tabs([
    "Team Profile",
    "National Comparison",
    "Aggressiveness Index"
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

    go_distance = pd.DataFrame({
        "National": national_distance["go_for_it"],
        selected_team: team_distance["go_for_it"]
    }).loc[distance_order]

    fig, ax = plt.subplots(figsize=(9, 5))
    go_distance.plot(kind="bar", ax=ax, color=[DARK_GRAY, ND_BLUE])
    ax.set_title("Go-For-It Rate by Distance", fontsize=14, weight="bold")
    ax.set_ylabel("Go-For-It Rate")
    ax.set_ylim(0, 1)
    ax.set_yticklabels([f"{int(y*100)}%" for y in ax.get_yticks()])
    ax.grid(axis="y", alpha=0.25)
    c1.pyplot(fig)

    go_field = pd.DataFrame({
        "National": national_field["go_for_it"],
        selected_team: team_field["go_for_it"]
    }).loc[field_order]

    go_field.index = [field_labels[x] for x in go_field.index]

    fig, ax = plt.subplots(figsize=(9, 5))
    go_field.plot(kind="bar", ax=ax, color=[DARK_GRAY, ND_BLUE])
    ax.set_title("Go-For-It Rate by Field Position", fontsize=14, weight="bold")
    ax.set_ylabel("Go-For-It Rate")
    ax.set_ylim(0, 1)
    ax.set_yticklabels([f"{int(y*100)}%" for y in ax.get_yticks()])
    ax.grid(axis="y", alpha=0.25)
    c2.pyplot(fig)

with tab3:
    st.subheader("Most Aggressive FBS Teams")

    st.dataframe(
        team_index.head(15)[
            [
                "rank",
                "offense",
                "fourth_down_decisions",
                "actual_go_rate",
                "expected_go_rate",
                "aggressiveness_index"
            ]
        ],
        use_container_width=True
    )

    st.subheader("Selected Team Ranking")

    st.dataframe(
        team_row[
            [
                "rank",
                "offense",
                "fourth_down_decisions",
                "actual_go_rate",
                "expected_go_rate",
                "aggressiveness_index"
            ]
        ],
        use_container_width=True
    )

st.divider()

with st.expander("View selected-team fourth-down plays"):
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
        ].head(500),
        use_container_width=True
    )
