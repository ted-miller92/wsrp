# Website Security Research Project

## Set Up Instructions to Test 

The first steps to get the project running are to create a virtual environment

Install Oracle Virtual Box

Create a virtual machine running Ubuntu 22.04 LTS available here:
https://releases.ubuntu.com/jammy/

install the apt packages required with the following command:

`sudo apt install git python3.10-venv curl`

Clone this repository

`git clone https://github.com/ted-miller92/wsrp.git`

## Database 

Install MySQL:

`wget https://dev.mysql.com/get/mysql-apt-config_0.8.33-1_all.deb`

`sudo dpkg -i mysql-apt-config_0.8.33-1_all.deb`

`sudo apt update`

`sudo apt install mysql-server`

Choose a memorable password for the root user.

Start MySQL and enter the password you just created:

`mysql -u root -p`

Create the database with the script:

`source database_setup_v0.sql`

## Server/API

Set up server

`python3 -m venv server_env`

`source server_env/bin/activate`

`pip install -r requirements.txt`

`flask --app server.py run`

At this point you should be able to access the API endpoints in the browser. 

## Frontend / Vue

Make sure node is installed via Node Version Manager. Download and install nvm:

`curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash`

Verify version:

`nvm --version`

Should show the version specified in the `curl` command above.

Now install node:

`nvm install node`

The latest version will be installed. Change to the `wsrp_vue` directory to start the vue front end with the following command:

`npm run dev`

Or build with:

`npm run build`


## Testing it out

The first feature that is "testable" is SQL injection. Open a web browser and navigate to `localhost:5173/login`. In the Username field enter `' OR ''='` with single quotes, as pictured below:

![sql injection](public/sql_injection_1.png)

Enter anything for the Password field. Before clicking "Login", open the web browser console (On Firefox, right-click > "Inspect"). After submitting the login form you will not be directed anywhere, but in the console you will see a list of all of the users in the database.