# publish_group_task

*To start the project you need to execute:*

* clone project repo
* Create an .env file and populate it following the default.env file example



* execute the command `make build` for build container
* execute the command `make cmd` for using console
* execute the command `make run` for run container

* execute the command `python manage.py migrate` for run migrations (if you don`t use dump)

You can fill db or run `make load` for load dump (**when container is running**)
* execute the command `make test` for run tests

you can use user from dump:

*admin creds for admin panel or site:*
 username:"admin123", password:"admin123"


*users creds for test site (or you can create a profile):*
 username:"new_user", password:"testpwd123"

**steps for using site:**
1) go to http://0.0.0.0:8000/ go to home page
2) go to http://0.0.0.0:8000/account/register/and sign up
3) go to http://0.0.0.0:8000/account/login/ and login
4) click on "Data Aggregator" button or "Get Started" Button
5) Load file on http://0.0.0.0:8000/data-aggregator/upload/ or use admin creds with data
6) See data on http://0.0.0.0:8000/data-aggregator/summary/ (you can select a filter by month or year)

**steps for using admin panel:**
1) go to http://0.0.0.0:8000/admin and login (as new superuser or admin)
2) go to http://0.0.0.0:8000/admin/account/user/  to manage users
3) go to http://0.0.0.0:8000/admin/data_aggregator/file/  to manage files
4) go to http://0.0.0.0:8000/admin/data_aggregator/datarow/  to manage data rows
