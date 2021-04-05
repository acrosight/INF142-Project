import random
locations = ["Bergen", "Stavanger", "Trondheim"]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Juni"]

temps = list(range(20))
precips = list(range(70, 200))
precip_days = list(range(1, 30))
sim_intervals = list(range(2500, 6000))

dummy_data = []

for i in range(20):
    location: str = locations[random.randint(0, len(locations) - 1)]
    month: str = months[random.randint(0, len(months) - 1)]
    avg_high_temp: int = temps[random.randint(0, len(temps) - 1)]
    avg_low_temp: int = temps[random.randint(0, len(temps) - 1)]
    avg_precipitation: int = precips[random.randint(0, len(precips) - 1)]
    avg_precipitation_days: int = precip_days[random.randint(0, len(precip_days) - 1)]
    simulation_interval: int = sim_intervals[random.randint(0, len(sim_intervals) - 1)]
    dummy_data.append({
        'location': location,
        'month': month,
        'avg_high_temp': avg_high_temp,
        'avg_low_temp': avg_low_temp,
        'avg_precipitation': avg_precipitation,
        'avg_precipitation_days': avg_precipitation_days,
        'simulation_interval': simulation_interval
    })
