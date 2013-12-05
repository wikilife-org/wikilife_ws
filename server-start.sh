#!/bin/sh
export PYTHONPATH=$PYTHONPATH:$PWD;
export PYTHONPATH=$PYTHONPATH:$PWD/../wikilife_utils;
export PYTHONPATH=$PYTHONPATH:$PWD/../wikilife_data;
export PYTHONPATH=$PYTHONPATH:$PWD/../wikilife_biz;

echo "wikilife_ws starting ... env=$1, port=$2"
nohup python2.7 wikilife_ws/manage.py $1 runserver $2 &
echo "Server Started";