## Introduction
SolarPanelSim is a piece of Python software which models the power output of a solar panel in orbit around Earth. It accounts for the various orbital parameters such as inclination and right ascension of the ascending node as well as the variation of solar panel power output throughout the year with the seasons. The user can set starting and final dates for the simulation and also select the timestep used in the orbit propagation process.

SolarPanelSim has some limitations that the user should be aware of:
- There is no ability to steer the solar panel. The panel is assumed to always be pointing away from nadir.
- The orbit definition and propagation model uses a Keplerian orbit. This type of orbit definition is known to have issues for orbits which are close to circular (i.e. apogee = perigee) or close to zero inclination (i.e. i = 0). If orbits like these are to be simulated, the results should be treated with caution.
## Dependencies
SolarPanelSim uses a handful of third party libraries to support functionality like orbit definition and propagation, data plotting and code tests. These are listed below, along with the versions that were used during development. Note that earlier versions may work but no testing has been carried out to check for backwards compatibility. 
- Python (3.11.6)
- Orekit (v12.0)
	- Used for orbit definition and propagation.
- Orekit data pack
	- Contains data needed by Orekit. Automatically downloaded and installed by SolarPanelSim.
- Matplotlib (3.8.2)
	- Used to produce plots of power output vs time.
- Pytest (7.4.3)
	- Used to run test suite.
- Miniconda/Anaconda
	- For installation and management of the above packages.

## Setup / Installation
- Install miniconda as per documentation: https://docs.conda.io/projects/miniconda/en/latest/
- Create a new conda environment and install dependencies from the supplied environment.yaml file
	- `conda env create -f environment.yaml`
- Activate the newly created conda environment
	- `conda activate SolarSimEnv`

## User Guide
In order to carry out the simulation, SolarPanelSim needs a number of parameters which describe the orbit and the solar panel itself. These are described below along with their input units and the <*parameter name*> which must be used for SolarPanelSim to recognise the input.
- **Orbit Creation Parameters** <*orbit_creation_parameters*>
	- Apogee <*apogee*> (km)
	- Perigee <*perigee*> (km)
	- Inclination <*i*> (degrees)
	- Argument of periapsis <*omega*> (degrees)
	- Right ascension of ascending node <*raan*> (degrees)
	- Initial true anomaly <*initial_lv*> (degrees)
- **Propagation Parameters** <*propagation_parameters*>
	- Initial date <*initial_date*> (ISO8601)
	- Final date <*final_date*> (ISO8601)
	- Timestep <*timestep*> (seconds)
- **Panel Parameters** <*panel_parameters*>
	- Panel surface area <*panel_area*> (m^2)
	- Panel efficiency <*panel_efficiency*> (-)

These parameters can be supplied to SolarPanelSim either by passing a file path string to a JSON file containing the parameters to SolarPanelSim as a command line argument:
```bash
python main.py './input.json'
```

Or by importing and calling SolarPanelSim from another Python program. In this case, a dictionary containing the parameters described above should be passed to the imported `solarsimulator` Python function as an input argument:
```python
from main import solarsimulator
inputdata = {dictionary containing input parameters}
solarsimulator(inputdata)
```

An example showing how the input data should be formatted (whether in JSON or Python dictionary) is shown below. If there are any errors in the input data, a `UserInputError` exception will be raised with a message describing the error.
```JSON
{
	"orbit_creation_parameters": {
		"apogee": 1200,
		"perigee": 900,
		"i": 25.0,
		"omega": 0.0,
		"raan": 45.0,
		"initial_lv": 0.0
	},
	"propagation_parameters": {
		"initial_date": "2023-03-21T12:00:00",
		"final_date": "2023-03-21T18:00:00",
		"timestep": 180.0
	},
	"panel_parameters": {
		"panel_area": 1.0,
		"panel_efficiency": 0.3
	}
}
```

Upon successful completion of the simulation, SolarPanelSim will save a PNG file with a plot of solar panel power output against time to the "plot_results" subfolder and a CSV file with a time history of power output to the "csv_results" subfolder. In both cases, the saved files will have file names describing the orbit simulated for easy identification of results. The plot will also be directly shown to the user for immediate results evaluation. Note: the matplotlib plot.show() function is blocking so the user may need to close the plot manually to terminate the execution of SolarPanelSim.

## Further Work
There are a number of things which could be done, given more time, to improve the accuracy and robustness of SolarPanelSim. These are:
#### Solar Panel Degradation
The efficiency of solar panels is known to decrease with time. By defining an efficiency degradation rate along with satellite launch date in addition to the start and final dates for the simulation, this decrease in panel efficiency could be modelled.
#### Update Orbit Definition
As mentioned above, SolarPanelSim currently uses a Keplerian orbit model which has known issues for circular or equatorial orbits. SolarPanelSim could be updated to use something like an Equinoctial Orbit (as recommended by Orekit) to remove this limitation.
#### Timestep Selection
Currently the user has to define a timestep for the orbit propagation manually. An algorithm could be developed which, given the start and end dates for the simulation, calculates an appropriate timestep automatically.
#### Modularity of plotting
The production of the plots of power vs time is currently carried out by the plot_power_output method in the OutputManager class. The plot_power_output method can only plot power output and so isn't very modular. If we wanted to plot other parameters (e.g. beta angle), a generic ResultsPlotter class could be created with subclasses for each parameter inheriting from it (e.g. BetaPlotter, PowerPlotter etc). This would be a more modular approach and would make the code more extensible.
#### Further integration with Orekit
Depending on the use case, it may be desirable to integrate further with Orekit. If SolarPanelSim were to be used as part of a wider Orekit based software package for example, it might be preferable to pass Orekit classes such as KeplerianOrbit directly to SolarPanelSim rather than the dictionary of orbital parameters outlined above.
#### Further user options
SolarPanelSim currently saves output plots and CSV files every time it is run. There may be cases where the user does not want to save this output data (if they are just using the returned results in another script for example). It would be relatively simple to add a `user_options` parameter to the input JSON/dictionary described above with a series of booleans to turn the data saving functionality on or off. This `user_options` parameter could also be used to select between different orbit definition models or propagation methods if that functionality was implemented.




