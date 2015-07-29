#!/bin/bash

curl -v -o - -d '{"id": 123, "protocol": "test"}' http://localhost:8000/message
