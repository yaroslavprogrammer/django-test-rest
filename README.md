# django-test-rest

### Simple 'Site' app including API with plain django admin

## How to use
0. Prerequirements (globally installed `virtualenvwrapper`) you can install it by typing `sudo pip install virtualenvwrapper`
1. Clone package:
   `git clone https://github.com/yaroslavprogrammer/django-test-rest`
2. Go to cloned dir and run `source activate` or `. activate` than all setup will be automated
3. If you have different postgres user or want to use other database, just change configuration in .env file then type `. .env`
and then `f bootstrap_db` or manually create database using `psql`
3. To run project just type `f run` (f - shortcut for fabric)
4. For tests run `m tests` (m - shortcut for manage.py)
