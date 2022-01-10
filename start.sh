#!/bin/bash
echo "starting..."
git pull
docker-compose up -d
echo "started..."