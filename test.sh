#!/bin/bash
args="$@"
vagrant ssh -c "cd /home/vagrant/waf/wagtail_advanced_form_builder/ && source /home/vagrant/.virtualenvs/waf/bin/activate && python -m pytest $args"
