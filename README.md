# Plot Visualizer Application

- Desktop application that allows users to load a CSV file and visualize the data using various types of plots (e.g., line, bar, histogram, etc.) 

- Based on PyQt5 and Matplotlib.



## Features

- **CSV File Loader**: Load data from a CSV file.
- **Plot Visualization**: Visualize data with plot types such as line, bar, horizontal bar, histogram, box, and area plots.
- **Dynamic Updation of Plots**: Switch between different plot types dynamically using a combo box.
- **Toolbar for Navigation**: A Matplotlib navigation toolbar - created to zoom, pan, and save plots.
- **CSV File Viewer**: A window to view the CSV file.

## Prerequisites

Before running the application, ensure that you have the following packages installed:

- Python 3.7+
- PyQt5
- Matplotlib
- Pandas
- SIP


## Getting Started

### 1. Creating a Virtual Environment

Before setting up the prerequisites, it is important to create a virtual environment for this project.

***For Linux:***

If pip is not in your system, run:

```$ sudo apt-get install python-pip```

Then install virtualenv:

```$ pip install virtualenv```

Then check if virtualenv has been successfully installed:

```$ virtualenv --version```

Now, we create a virtual environment:

```$ virtualenv venv_name```

After this, a folder named **venv_name** will be created. To activate this virtual environment:

```$ source venv_name/bin/activate```

To deactivate:

```$ deactivate```

***For Windows:***

Make sure to have Python 3.7+ installed from the official Python website (www.python.org). 

Then install the virtualenv package:

```$ pip install virtualenv```

Now, we create a virtual environment within the selected directory, where `myenv` is the name of the virtual environment:

```$ python -m venv myenv```

After this, a folder named **myenv** will be created. To activate this virtual environment:

```$ myenv/Scripts/activate```

To deactivate:

```$ deactivate```


### 2. Prerequisites

Make sure to install the prerequisites from the 'requirements.txt' file:

```pip install -r requirements.txt```

Or

```pip install PyQt5 matplotlib seaborn pandas sip```

### 2. Running the Application
With the packages installed, you can run the application using:

```python main.py```

----


Thanks for reading!







