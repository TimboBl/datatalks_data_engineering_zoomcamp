#### Local env setup

I have chosen to go with a local conda env using miniconda. I have installed miniconda via homebrew and created a new env using the command below:
```conda env create -f environment.yml```

The environment.yml file contains the following packages:
- sqlalchemy
- pandas

The file is stored in the root folder of the repo. 
The environemnt file will give a name to the conda env and also pull from the conda-forge channel. The python version is also set to 3.12.8 to ensure consistency across the project. 

Using the conda env also makes sure to not install packages into the global scope of the machine. This makes it easier to keep the machine clean and to avoid conflicts with other packages or projects using the same packages in diffrent versions.

To activate the env, the command below can be used:
```conda activate data-engineering```

#### Question 1 
Running docker in interactive mode
> docker run -it python:3.12.8 bash

Pip version in this image is 24.3.1

#### Question 2
Connecting to Postgres 

> The hostname and port to use for pgadmin should be postgres:5433

