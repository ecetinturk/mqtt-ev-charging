Using Simulation and Web Interface:

1- Setting up MQTT Broker
	- In the command line go to the directory of the mosquitto program files on your computer and run the MQTT Broker on port 1884 with this command: 
		"mosquitto.exe -p 1884"

2- Setting up the Web Interface
	- Go to "Arayuz" folder on command line
	- Create a python virtual environment:
		"python -m venv env"
	- Activate the virtual environment:
		"env/Scripts/activate"
	- Install the required modules:
		"pip install -r requirements.txt"
	- Run app.py
		"python app.py"
	- Web interface will be set on "http://127.0.0.1:5000/", open this address on your browser.

3- Running SUMO simulation
	- Go to "simulation2" folder, run final.py. On opened SUMO simulation, set a delay (100ms recommended) and run simulation.

	- After running the simulation, values ​​will be updated as new values ​​come from the simulation.
	- You can follow the status of the vehicles live from this interface.

	