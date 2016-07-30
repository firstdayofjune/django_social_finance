#!/usr/bin/env bash

# PG Database configuration
APP_DB_USER=django
APP_DB_PASS=31CrYPt1C_P4S5w0rD+
APP_DB_NAME=social_django

PG_VERSION=9.5


# Update package-list and upgrade all packages
yes | pacman -Syu

#######################################################################################
# 
#  Install PostgreSQL
#
#######################################################################################
echo "##############################################"
echo "Installing PostgreSQL..."
echo ""
	
yes | pacman -S postgresql=9.5.3

cat << EOF | su - postgres
-- initilaize db-cluster
initdb --locale $LANG -E UTF8 -D '/var/lib/postgres/data'
EOF

# auto-start service
systemctl enable postgresql.service
systemctl start postgresql.service


### The following is taken from:
# https://github.com/jackdb/pg-app-dev-vm/blob/master/Vagrant-setup/bootstrap.sh
###
PG_CONF="/var/lib/postgres/data/postgresql.conf"
PG_HBA="/var/lib/postgres/data/pg_hba.conf"

# Edit postgresql.conf to change listen address to '*':
sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" "$PG_CONF"

# Append to pg_hba.conf to add password auth:
echo "host    all             all             all                     md5" >> "$PG_HBA"

# Explicitly set default client_encoding
echo "client_encoding = utf8" >> "$PG_CONF"

# Restart so that all new config is loaded:
systemctl restart postgresql.service

cat << EOF | su - postgres -c psql
-- Create the database user:
CREATE USER $APP_DB_USER CREATEDB WITH PASSWORD '$APP_DB_PASS';

-- Create the database:
CREATE DATABASE $APP_DB_NAME WITH OWNER=$APP_DB_USER
                                  LC_COLLATE='en_US.utf8'
                                  LC_CTYPE='en_US.utf8'
                                  ENCODING='UTF8'
                                  TEMPLATE=template0;
EOF

echo "Successfully created PostgreSQL dev virtual machine."
echo "##############################################"
echo ""


#######################################################################################
# 
#  Install Python, pip & Django + requirements
#
#######################################################################################
echo "##############################################"
echo "Installing Python3, pip and django-packages"
echo ""
yes | pacman -S python python-pip

pip install -r requirements.pip


# set environment variables which will be read from django
echo 'export DJANGO_SECRET_KEY="io&o60txl_-0k=((ap@ykvrbs%n#!wpltaja-jul0pta(d40d4"' >> /etc/profile
echo "export DJANGO_DB_USER=$APP_DB_USER" >> /etc/profile
echo "export DJANGO_DB_NAME=$APP_DB_NAME" >> /etc/profile
echo "export DJANGO_DB_PW=$APP_DB_PASS" >> /etc/profile

echo "Successfully installed python & django."
echo "##############################################"
echo ""