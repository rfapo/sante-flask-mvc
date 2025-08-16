import pandas as pd
from services.analytics import compute_indicators, compute_forecast
from models import db, City, Observation, Indicator

REQUIRED_COLUMNS = {"city","state","country","week_label","cases"}

def allowed(df: pd.DataFrame) -> bool:
    return REQUIRED_COLUMNS.issubset(set(c.lower() for c in df.columns))

def load_csv(file_storage) -> City:
    df = pd.read_csv(file_storage)
    # Normalize columns to lowercase
    df.columns = [c.lower().strip() for c in df.columns]
    if not allowed(df):
        raise ValueError(f"CSV must contain the following columns: {sorted(REQUIRED_COLUMNS)}")
    # Take first row to create/find the City
    first = df.iloc[0]
    name, state, country = str(first["city"]).strip(), str(first["state"]).strip(), str(first["country"]).strip()

    city = City.query.filter_by(name=name, state=state, country=country).first()
    if city is None:
        city = City(name=name, state=state, country=country)
        db.session.add(city)
        db.session.flush()  # to get city.id

    # Wipe previous observations for idempotent re-upload
    # (could be changed to append/versioning later)
    for obs in list(city.observations):
        db.session.delete(obs)

    observations = []
    for _, row in df.iterrows():
        week_label = str(row["week_label"]).strip()
        cases = int(row["cases"])
        observations.append(Observation(city_id=city.id, week_label=week_label, cases=cases))
    db.session.add_all(observations)

    # Compute and store indicators
    rt, r0, hosp = compute_indicators([o.cases for o in observations])
    db.session.add(Indicator(city_id=city.id, rt=rt, r0=r0, hospitalization_rate=hosp))

    db.session.commit()
    return city

def get_city_series(city_id: int):
    obs = Observation.query.filter_by(city_id=city_id).order_by(Observation.id.asc()).all()
    labels = [o.week_label for o in obs]
    values = [o.cases for o in obs]
    forecast = compute_forecast(values)
    return labels, values, forecast
