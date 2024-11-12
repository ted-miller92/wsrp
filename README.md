# Website Security Research Project

The first steps to get the project running are to create a virtual environment

Install Oracle Virtual Box

Create a virtual machine running Ubuntu 22.04 LTS available here:
https://releases.ubuntu.com/jammy/

install the apt packages required with the following command:

`sudo apt install git python3.10-venv `

Clone this repository

`git clone https://github.com/ted-miller92/wsrp.git`

Install MySQL:

`wget https://dev.mysql.com/get/mysql-apt-config_0.8.33-1_all.deb`

`sudo dpkg -i mysql-apt-config_0.8.33-1_all.deb`

`sudo apt update`

`sudo apt install mysql-server`

Choose a memorable password for the root user.

Set up server

`python3 -m venv server_env`

`source server_env/bin/activate`

`pip install -r requirements.txt`

`flask --app server.py run`

At this point you should be able to access the API endpoints in the browser. 