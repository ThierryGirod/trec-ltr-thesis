#!/bin/sh

docker build . -t ltrps-solr
docker-compose up