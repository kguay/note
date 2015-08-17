Bigelow Expense Report Web Application
======
by: Kevin C. Guay

https://github.com/kguay/bigelow_expense

This webapp allows users to submit, review, edit, and approve (supervisors only) credit card and purchase expense reports and receipts.

It is built using the Flask framework for Python. It uses Bootstrap in order to create a responsive, user-friendly experience on any device (mobile, tablet, and desktop).

A SQLite* database is used to store user information and expense reports.

\* *Before this application is deployed for Bigelow staff to use, the database should be changed to a more robust option (i.e. MySQL or PostgreSQL). I used SQLite here (for demonstration purposes) because it is self-contained and does not require any system configuration to use. Since I am using the SQLalchemy module, changing databases will be quick & easy.*

###Install & Run

*Note: steps 2, 3, and 6 can be combined by runnint the bash script `./run`*

1. Untar the file and navigate to the project directory (bigelow_expense)

2. Install virtual environment (if not already installed)

	`sudo pip install virtualenv`

3. Activate the virtual environment

	`source venv/bin/activate`

4. Run the python web application

	`./venv/bin/python main.py`

5. View the web application

	Go to: <a href="http://localhost:5000" target="_blank">http://localhost:5000</a>

6. Deactivate the virtual environment when you are done

	`deactivate`
