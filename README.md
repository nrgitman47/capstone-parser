# capstone-parser

## Setup
First, setup `git` on your local computer. Then create and navigate to the directory in which you'd like to clone this repository. Alternatively, you can download the ZIP file from the repository home page. 

Prerequisites: Python3

1. To clone this repository, run the command below:

   ```bash
   git clone https://github.com/nrgitman47/capstone-parser.git
   ```
2. Navigate inside the repository, then run readbinary.py

    ```bash
    cd capstone-parser
    ```
    ```bash
    python3 readbinary.py
    ```

Running `readbinary.py` should create two csv files inside your directory, one for IMU data and one for ATOF. More information about the data can be found here: https://docs.ceruleansonar.com/c/surveyor-240-16/application-programming-interface 

***Important***: you may run into issues when running the python script. Here are some errors I think may occur.
1. The script cannot find the svlog file. Fix this by moving or downloading one of the .svlog files into the same directory as your python script. Change the line below to match the name of the file. The current script is parsing our most recent test where we ran the sonar with channel data enabled.
   
    ```bash
    with open("<filename>.svlog", "rb") as file:
    ```
2. more to come
