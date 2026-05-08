# ChronoOrigins (Streamlit Game)

ChronoOrigins is a world-history guessing game built with Streamlit.

Players are shown 5 personalities per round and must guess:
- when they lived (clicking a timeline from 1000 BCE to 2100 AD),
- where they are from (clicking a country on a world map).

The game has 3 rounds, and each round is harder because scoring windows get stricter.

## Gameplay

- 3 rounds total, 5 personalities each.
- For every personality, submit:
  - guessed year on the timeline,
  - guessed country on the map.
- Per personality score:
  - up to 100 points for timeline accuracy,
  - up to 100 points for geographic proximity.

Maximum possible score: 3000 points.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this folder to a GitHub repository.
2. Go to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Create a new app and select:
   - repository: your GitHub repo,
   - branch: your preferred branch,
   - main file path: `app.py`.
4. Deploy.

## Notes

- Country scoring uses centroid-to-centroid distance as a proximity estimate.
- The personality list is currently hardcoded in `app.py`, so you can easily edit and expand rounds.
