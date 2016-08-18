#!/bin/bash
APP=`jq -r .$1 /app.json`
BASE=`jq -r .$1 /base.json`

if [ "$APP" = "null" ]
then
   echo $BASE
else
   echo $APP
fi
