def compute_indicators(series):
    if not series or len(series) < 2:
        # Defaults if we can't compute
        return 0.95, 1.3, 5.8
    last, prev = series[-1], series[-2]
    rt = round((last / prev) if prev else 1.0, 2)
    # Keep a default R0; in real app you would estimate this
    r0 = 1.3
    # Hospitalization proxy: 3% + intensity factor
    change = (last - prev) / prev if prev else 0
    hosp = round(3.0 + max(0, change * 10), 1)
    return rt, r0, hosp

def compute_forecast(series):
    # Very simple illustrative forecast: decay by 10% per step from last value
    if not series:
        return [0, 0, 0]
    last = series[-1]
    f1 = round(last * 0.9)
    f2 = round(f1 * 0.9)
    f3 = round(f2 * 0.9)
    return [f1, f2, f3]
