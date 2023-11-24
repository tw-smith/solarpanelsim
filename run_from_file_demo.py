from main import solarsimulator


inputdata = {
  "propagation_parameters": {
    "initial_date": "2023-03-21T12:00:00.0Z",
    "final_date": "2023-03-21T18:00:00.0Z",
    "timestep": 180.0

  },
  "orbit_creation_parameters": {
    "apogee": 1200,
    "perigee": 900,
    "i": 25.0,
    "omega": 0.0,
    "raan": 45.0,
    "initial_lv": 0.0
  },
  "panel_parameters": {
    "panel_area": 1.0,
    "panel_efficiency": 0.3
  }
}

results = solarsimulator(inputdata)
print(results)