# change password and setup new database (local)

echo "Creating database $PROJECT_NAME for user $PROJECT_NAME"

sudo -i -u postgres psql -c "CREATE USER \"$PROJECT_NAME\" WITH PASSWORD '$PROJECT_NAME';"
sudo -i -u postgres psql -c "ALTER USER \"$PROJECT_NAME\" CREATEDB"
sudo -i -u postgres psql -c "CREATE DATABASE \"$PROJECT_NAME\";"
sudo -i -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE \"$PROJECT_NAME\" TO \"$PROJECT_NAME\";"
