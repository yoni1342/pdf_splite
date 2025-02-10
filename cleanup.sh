#!/bin/bash

# Remove files older than 1 hour from the temp directory
find /temp -type f -mmin +60 -exec rm -f {} \;
find /temp -type d -empty -delete
