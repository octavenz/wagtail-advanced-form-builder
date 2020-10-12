# Contributing

PR's are welcome. The repository comes with Vagrant machine instructions and Ansible provisioning to get a basic Wagtail build up and running.

## Pre-requisites

* Install [Vagrant](https://www.vagrantup.com/downloads)
* Install [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
* Install [NVM](https://github.com/nvm-sh/nvm) 

## Getting started

0.  Build the machine

        vagrant up
        
0. Create a superuser

        ./manage.sh createsuperuser
        
0. Run the site. It will be accessible at http://localhost:8019

        ./run.sh
        
0. Go to the admin and start building forms by creating child pages.

        http://localhost:8019/admin                
        
0. You can also run Mailcatcher to catch any emails the site sends if you want to test email functionality. Mailcatcher will be accessible at http://localhost:1080

        ./mailcatcher.sh       
        
## Working on the front end

0. Install packages

        nvm use
        npm install
        
0. Run the watch task

        npm run watch
        
0. Modify the JS and SASS source files in wagtail_advanced_form_builder/static_src/                                          
