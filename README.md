# podminator

Podminator is a small Kubernetes tool in order to terminate half of the pods deployed only on the replica sets. Then Kubernetes deployment objects try to recreate half of the pods again and you can monitor behaviour of the your system simulating hard circumstances. 

Project has been developed by using Python3 and its' Kubernetes library. 
To do the project up; clone the repo, get in it and run the commands below.
-   python3 -m venv env
-   source env/bin/activate
-   pip install -r requirements.txt
-  	python3 code/podminator.py
