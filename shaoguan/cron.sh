#!/bin/bash

touch jobs.data

#use phantomjs to get the radarTime,will take serveral seconds
path/to/phantomjs radarTime.js

#check radarTime.dat file

python3 shaoguan-dl.py