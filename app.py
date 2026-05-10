import math
import random
import re
import secrets
from pathlib import Path
from dataclasses import dataclass
import json

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(page_title="Itigol", page_icon="🌍", layout="wide")


@dataclass
class Person:
    name: str
    year: int
    country_iso3: str
    country_name: str
    difficulty: int


COUNTRIES = {
    "USA": {"name": "United States", "lat": 39.8, "lon": -98.6},
    "CAN": {"name": "Canada", "lat": 56.1, "lon": -106.3},
    "MEX": {"name": "Mexico", "lat": 23.6, "lon": -102.5},
    "BRA": {"name": "Brazil", "lat": -14.2, "lon": -51.9},
    "ARG": {"name": "Argentina", "lat": -38.4, "lon": -63.6},
    "CHL": {"name": "Chile", "lat": -35.7, "lon": -71.5},
    "COL": {"name": "Colombia", "lat": 4.6, "lon": -74.1},
    "PER": {"name": "Peru", "lat": -9.2, "lon": -75.0},
    "GBR": {"name": "United Kingdom", "lat": 55.4, "lon": -3.4},
    "FRA": {"name": "France", "lat": 46.2, "lon": 2.2},
    "DEU": {"name": "Germany", "lat": 51.2, "lon": 10.4},
    "ITA": {"name": "Italy", "lat": 42.8, "lon": 12.5},
    "ESP": {"name": "Spain", "lat": 40.5, "lon": -3.7},
    "NLD": {"name": "Netherlands", "lat": 52.1, "lon": 5.3},
    "BEL": {"name": "Belgium", "lat": 50.5, "lon": 4.5},
    "CHE": {"name": "Switzerland", "lat": 46.8, "lon": 8.2},
    "AUT": {"name": "Austria", "lat": 47.5, "lon": 14.6},
    "POL": {"name": "Poland", "lat": 52.1, "lon": 19.1},
    "UKR": {"name": "Ukraine", "lat": 48.4, "lon": 31.2},
    "RUS": {"name": "Russia", "lat": 61.5, "lon": 105.3},
    "SWE": {"name": "Sweden", "lat": 60.1, "lon": 18.6},
    "NOR": {"name": "Norway", "lat": 60.5, "lon": 8.5},
    "DNK": {"name": "Denmark", "lat": 56.2, "lon": 9.5},
    "GRC": {"name": "Greece", "lat": 39.1, "lon": 21.8},
    "TUR": {"name": "Turkey", "lat": 39.0, "lon": 35.2},
    "EGY": {"name": "Egypt", "lat": 26.8, "lon": 30.8},
    "ETH": {"name": "Ethiopia", "lat": 9.1, "lon": 40.5},
    "NGA": {"name": "Nigeria", "lat": 9.1, "lon": 8.7},
    "ZAF": {"name": "South Africa", "lat": -30.6, "lon": 22.9},
    "MAR": {"name": "Morocco", "lat": 31.8, "lon": -7.1},
    "SAU": {"name": "Saudi Arabia", "lat": 23.9, "lon": 45.1},
    "IRN": {"name": "Iran", "lat": 32.4, "lon": 53.7},
    "IRQ": {"name": "Iraq", "lat": 33.0, "lon": 43.7},
    "ISR": {"name": "Israel", "lat": 31.0, "lon": 35.0},
    "IND": {"name": "India", "lat": 22.9, "lon": 79.0},
    "PAK": {"name": "Pakistan", "lat": 30.4, "lon": 69.3},
    "BGD": {"name": "Bangladesh", "lat": 23.7, "lon": 90.4},
    "CHN": {"name": "China", "lat": 35.9, "lon": 104.2},
    "JPN": {"name": "Japan", "lat": 36.2, "lon": 138.3},
    "KOR": {"name": "South Korea", "lat": 36.5, "lon": 127.8},
    "IDN": {"name": "Indonesia", "lat": -0.8, "lon": 113.9},
    "THA": {"name": "Thailand", "lat": 15.9, "lon": 101.0},
    "VNM": {"name": "Vietnam", "lat": 14.1, "lon": 108.3},
    "PHL": {"name": "Philippines", "lat": 12.9, "lon": 121.8},
    "AUS": {"name": "Australia", "lat": -25.3, "lon": 133.8},
    "NZL": {"name": "New Zealand", "lat": -41.3, "lon": 174.8},
    "AFG": {"name": "Afghanistan", "lat": 33.9, "lon": 67.7},
    "UZB": {"name": "Uzbekistan", "lat": 41.4, "lon": 64.6},
    "VEN": {"name": "Venezuela", "lat": 6.4, "lon": -66.6},
    "MLI": {"name": "Mali", "lat": 17.6, "lon": -3.9},
    "NPL": {"name": "Nepal", "lat": 28.4, "lon": 84.1},
    "MKD": {"name": "North Macedonia", "lat": 41.6, "lon": 21.7},
    "HRV": {"name": "Croatia", "lat": 45.1, "lon": 15.2},
    "SRB": {"name": "Serbia", "lat": 44.0, "lon": 20.8},
    "SYR": {"name": "Syria", "lat": 34.8, "lon": 38.9},
    "TUN": {"name": "Tunisia", "lat": 34.0, "lon": 9.6},
    "IRL": {"name": "Ireland", "lat": 53.1, "lon": -8.0},
    "HTI": {"name": "Haiti", "lat": 19.0, "lon": -72.3},
    "MNG": {"name": "Mongolia", "lat": 46.8, "lon": 103.8},
    "KEN": {"name": "Kenya", "lat": 0.0, "lon": 37.9},
    "GHA": {"name": "Ghana", "lat": 7.9, "lon": -1.0},
    "HUN": {"name": "Hungary", "lat": 47.2, "lon": 19.5},
}


COUNTRY_NAME_TO_ISO3 = {data["name"]: iso3 for iso3, data in COUNTRIES.items()}
COUNTRY_NAME_ALIASES = {
    "USA": "United States",
    "United States of America": "United States",
    "N. Macedonia": "North Macedonia",
}

DIFFICULTY_TO_ROUND = {"Easy": 1, "Medium": 2, "Hard": 3}
PEOPLE_PER_ROUND = 3
TOTAL_ROUNDS = 3
MAP_CHART_HEIGHT_PX = 920

DATA_DIR = Path(__file__).parent
DATA_FILE = DATA_DIR / "personalities_v1.json"


ROUND_RULES = {
    1: {"time_window": 1500.0, "distance_window_km": 9000.0},
    2: {"time_window": 1000.0, "distance_window_km": 6000.0},
    3: {"time_window": 600.0, "distance_window_km": 3500.0},
}


def parse_birth_year(time_period: str) -> int | None:
    cleaned = time_period.replace("\u2013", "-").replace("\u2014", "-")
    century_match = re.search(r"(\d+)(?:st|nd|rd|th)\s*C\.\s*BCE", cleaned, flags=re.I)
    if century_match:
        century = int(century_match.group(1))
        return -(century * 100 - 50)
    year_match = re.search(r"(\d+)", cleaned)
    if not year_match:
        return None
    year = int(year_match.group(1))
    if "BCE" in cleaned.upper():
        return -year
    return year


def normalize_birth_country(raw_country: str) -> str:
    first_country = raw_country.split("/")[0].strip()
    return COUNTRY_NAME_ALIASES.get(first_country, first_country)


def load_people_from_json() -> tuple[list[Person], list[str]]:
    with DATA_FILE.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    people: list[Person] = []
    errors: list[str] = []
    for entry in payload:
        name = str(entry.get("Personality", "")).strip()
        country_name = normalize_birth_country(str(entry.get("Modern Nation-State", "")).strip())
        period = str(entry.get("Time Period", "")).strip()
        difficulty_label = str(entry.get("Difficulty", "")).strip()

        birth_year = parse_birth_year(period)
        round_num = DIFFICULTY_TO_ROUND.get(difficulty_label)
        iso3 = COUNTRY_NAME_TO_ISO3.get(country_name)

        if not name or birth_year is None or round_num is None or iso3 is None:
            errors.append(
                f"{name or 'Unknown'} | birth origin '{country_name}' | "
                f"time '{period}' | difficulty '{difficulty_label}'"
            )
            continue

        people.append(
            Person(
                name=name,
                year=birth_year,
                country_iso3=iso3,
                country_name=country_name,
                difficulty=round_num,
            )
        )
    return people, errors


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius_earth_km = 6371.0
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = (
        math.sin(d_phi / 2.0) ** 2
        + math.cos(phi_1) * math.cos(phi_2) * math.sin(d_lambda / 2.0) ** 2
    )
    return 2.0 * radius_earth_km * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))


def score_time(guess_year: int, actual_year: int, window: float) -> tuple[float, int]:
    diff = abs(guess_year - actual_year)
    points = max(0.0, 100.0 * (1.0 - min(diff, window) / window))
    return round(points, 1), diff


def score_country(
    guessed_iso3: str, actual_iso3: str, window_km: float
) -> tuple[float, float]:
    if guessed_iso3 not in COUNTRIES or actual_iso3 not in COUNTRIES:
        return 0.0, window_km

    guessed = COUNTRIES[guessed_iso3]
    actual = COUNTRIES[actual_iso3]
    dist = haversine_km(guessed["lat"], guessed["lon"], actual["lat"], actual["lon"])
    points = max(0.0, 100.0 * (1.0 - min(dist, window_km) / window_km))
    return round(points, 1), dist


def year_label(year: int) -> str:
    if year < 0:
        return f"{abs(year)} BCE"
    return f"{year} AD"


def build_timeline_chart(selected_year: int | None) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=[-1000, 2100],
            y=[0, 0],
            mode="lines",
            line={"width": 16, "color": "#4B91F1"},
            hoverinfo="skip",
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[-1000, -500, 0, 500, 1000, 1500, 2000],
            y=[0, 0, 0, 0, 0, 0, 0],
            mode="markers+text",
            marker={"size": 8, "color": "#112A46"},
            text=["1000 BCE", "500 BCE", "0", "500", "1000", "1500", "2000"],
            textposition="top center",
            hoverinfo="skip",
            showlegend=False,
        )
    )
    if selected_year is not None:
        fig.add_trace(
            go.Scatter(
                x=[selected_year],
                y=[0],
                mode="markers+text",
                marker={"size": 16, "color": "#FF9F1C"},
                text=[f"Your guess: {year_label(selected_year)}"],
                textposition="bottom center",
                showlegend=False,
            )
        )
    fig.update_xaxes(range=[-1000, 2100], visible=False)
    fig.update_yaxes(range=[-1, 1], visible=False)
    fig.update_layout(
        height=220,
        margin={"l": 10, "r": 10, "t": 10, "b": 10},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def build_map_chart(selected_iso3: str | None) -> go.Figure:
    df = pd.DataFrame(
        {
            "iso3": list(COUNTRIES.keys()),
            "country": [COUNTRIES[k]["name"] for k in COUNTRIES],
            "z": list(range(len(COUNTRIES))),
        }
    )
    fig = go.Figure(
        data=go.Choropleth(
            locations=df["iso3"],
            z=df["z"],
            text=df["country"],
            colorscale="Turbo",
            marker_line_color="#F7F7F7",
            marker_line_width=0.8,
            showscale=False,
            hovertemplate="%{text}<extra></extra>",
        )
    )
    if selected_iso3 in COUNTRIES:
        selected = COUNTRIES[selected_iso3]
        fig.add_trace(
            go.Scattergeo(
                lon=[selected["lon"]],
                lat=[selected["lat"]],
                mode="markers+text",
                marker={"size": 10, "color": "#E63946"},
                text=[f"Your pick: {selected['name']}"],
                textposition="top center",
                showlegend=False,
            )
        )
    fig.update_geos(
        projection_type="natural earth",
        showframe=False,
        showcoastlines=True,
        coastlinecolor="#2D4A63",
        showcountries=True,
        countrycolor="#F7F7F7",
        bgcolor="rgba(0,0,0,0)",
    )
    fig.update_layout(
        height=MAP_CHART_HEIGHT_PX,
        dragmode=False,
        margin={"l": 10, "r": 10, "t": 10, "b": 10},
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def init_state(people: list[Person]) -> None:
    if "round" not in st.session_state:
        st.session_state.round = 1
        st.session_state.person_idx = 0
        st.session_state.score_total = 0.0
        st.session_state.results = []
        st.session_state.selected_year = None
        st.session_state.selected_country = None
        # Wide-range seed so each new session gets an unpredictable personality order.
        st.session_state.seed = secrets.randbelow(1 << 62)
        for diff in (1, 2, 3):
            arr = [p for p in people if p.difficulty == diff].copy()
            rng = random.Random(st.session_state.seed + diff)
            rng.shuffle(arr)
            st.session_state[f"round_{diff}_people"] = arr


def reset_pick_state() -> None:
    st.session_state.selected_year = None
    st.session_state.selected_country = None


def get_current_person() -> Person | None:
    current_round = st.session_state.round
    if current_round > TOTAL_ROUNDS:
        return None
    people = st.session_state[f"round_{current_round}_people"]
    idx = st.session_state.person_idx
    if idx >= len(people):
        return None
    return people[idx]


def next_person_or_round() -> None:
    st.session_state.person_idx += 1
    if st.session_state.person_idx >= PEOPLE_PER_ROUND:
        st.session_state.round += 1
        st.session_state.person_idx = 0
    reset_pick_state()


def submit_guess(person: Person) -> None:
    round_num = st.session_state.round
    rules = ROUND_RULES[round_num]
    guessed_year = int(st.session_state.selected_year)
    guessed_country = str(st.session_state.selected_country)

    time_points, year_diff = score_time(guessed_year, person.year, rules["time_window"])
    country_points, country_distance = score_country(
        guessed_country, person.country_iso3, rules["distance_window_km"]
    )
    total_points = time_points + country_points
    st.session_state.score_total += total_points

    st.session_state.results.append(
        {
            "round": round_num,
            "person": person.name,
            "actual_year": year_label(person.year),
            "guessed_year": year_label(guessed_year),
            "year_error": year_diff,
            "actual_country": person.country_name,
            "guessed_country": COUNTRIES.get(guessed_country, {}).get("name", guessed_country),
            "distance_km": round(country_distance, 1),
            "time_points": time_points,
            "country_points": country_points,
            "total_points": round(total_points, 1),
        }
    )

    st.success(
        f"Scored {total_points:.1f} points. "
        f"Time error: {year_diff} years. Country distance: {country_distance:.0f} km."
    )
    next_person_or_round()


def render_header() -> None:
    st.title("Itigol")
    st.caption(
        "Pick each person's time and birth-origin country. 3 rounds x 3 people. "
        "Later rounds have stricter scoring."
    )
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Round", min(st.session_state.round, 3))
    col_b.metric("Current Score", f"{st.session_state.score_total:.1f}")
    answered = len(st.session_state.results)
    col_c.metric("Answered", f"{answered}/{TOTAL_ROUNDS * PEOPLE_PER_ROUND}")


def render_round_end_screen(round_finished: int) -> None:
    st.subheader(f"Round {round_finished} complete")
    round_df = pd.DataFrame(
        [r for r in st.session_state.results if r["round"] == round_finished]
    )[
        [
            "person",
            "actual_year",
            "guessed_year",
            "year_error",
            "actual_country",
            "guessed_country",
            "distance_km",
            "total_points",
        ]
    ]
    st.dataframe(round_df, use_container_width=True)
    if st.button("Continue"):
        st.session_state.round = round_finished + 1
        st.session_state.person_idx = 0
        reset_pick_state()
        st.rerun()


def render_final_screen() -> None:
    st.subheader("Game complete")
    max_score = TOTAL_ROUNDS * PEOPLE_PER_ROUND * 200
    st.write(f"Final score: **{st.session_state.score_total:.1f}** / {max_score}")
    st.dataframe(pd.DataFrame(st.session_state.results), use_container_width=True)
    if st.button("Play Again"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()


if not DATA_FILE.exists():
    st.error(f"Missing input JSON file: {DATA_FILE.name}")
    st.stop()

ALL_PEOPLE, LOAD_ERRORS = load_people_from_json()
if LOAD_ERRORS:
    st.warning(
        f"Skipped {len(LOAD_ERRORS)} invalid entries from {DATA_FILE.name}. "
        "Using all remaining valid personalities."
    )
    with st.expander("Show skipped rows (first 20)"):
        st.code("\n".join(LOAD_ERRORS[:20]))

for diff, label in ((1, "Easy"), (2, "Medium"), (3, "Hard")):
    count = len([p for p in ALL_PEOPLE if p.difficulty == diff])
    if count < PEOPLE_PER_ROUND:
        st.error(
            f"Need at least {PEOPLE_PER_ROUND} '{label}' personalities in JSON. Found {count}."
        )
        st.stop()

init_state(ALL_PEOPLE)
render_header()

if st.session_state.round > TOTAL_ROUNDS:
    render_final_screen()
    st.stop()

current_person = get_current_person()

if current_person is None:
    render_round_end_screen(st.session_state.round - 1)
    st.stop()

st.markdown(
    f"### Round {st.session_state.round} - Person {st.session_state.person_idx + 1} of {PEOPLE_PER_ROUND}"
)
st.info(f"Who is {current_person.name}?")

st.markdown("#### 1) Timeline")
st.markdown(
    """
<div style="
    width: 100%;
    height: 16px;
    border-radius: 10px;
    background: linear-gradient(90deg, #2D6CDF 0%, #58A6FF 100%);
    margin-top: 0.25rem;
    margin-bottom: 0.35rem;
"></div>
""",
    unsafe_allow_html=True,
)
year_options = list(range(-1000, 2101, 50))
default_year = (
    st.session_state.selected_year
    if st.session_state.selected_year in year_options
    else 0
)
st.session_state.selected_year = st.select_slider(
    "Timeline year",
    options=year_options,
    value=default_year,
    format_func=year_label,
    label_visibility="collapsed",
    key=f"timeline_slider_{st.session_state.round}_{st.session_state.person_idx}",
)
st.write("Selected year:", year_label(st.session_state.selected_year))

st.markdown("#### 2) Click a country on the map")
map_fig = build_map_chart(st.session_state.selected_country)
map_event = st.plotly_chart(
    map_fig,
    use_container_width=True,
    key=f"map_{st.session_state.round}_{st.session_state.person_idx}",
    on_select="rerun",
    selection_mode="points",
    config={
        "scrollZoom": False,
        "doubleClick": False,
        "displayModeBar": False,
    },
)
map_points = map_event.get("selection", {}).get("points", [])
if map_points and "location" in map_points[0]:
    st.session_state.selected_country = map_points[0]["location"]

country_label = (
    COUNTRIES[st.session_state.selected_country]["name"]
    if st.session_state.selected_country in COUNTRIES
    else "Not selected"
)
st.write("Selected country:", country_label)

can_submit = (
    st.session_state.selected_year is not None
    and st.session_state.selected_country is not None
)
if st.button("Submit Guess", type="primary", disabled=not can_submit):
    submit_guess(current_person)
    st.rerun()

st.divider()
st.caption(
    "Scoring per person: up to 100 for time + 100 for geography. "
    "Geography score decreases with centroid-to-centroid distance."
)
