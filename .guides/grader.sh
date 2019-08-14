#!/usr/bin/env bash

cd .guides/teacherFiles/hw-ruby-intro-ci/

bundle exec rspec -I /home/codio/workspace/assignment/hw-ruby-intro/lib/ -r ruby_intro.rb autograder/part$1_spec.rb --format j | python ~/workspace/.guides/saas_grade.py