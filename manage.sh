#!/bin/bash
args="$@"
vagrant ssh -c "source /home/vagrant/.virtualenvs/waf/bin/activate && python /home/vagrant/waf/manage.py $args"
