#!/bin/bash

echo "Running async unit tests first..."
pytest tests/unit/test_jwt.py tests/unit/test_redis.py -vv

echo "Running the rest of the test suite..."
pytest -vv --ignore=tests/unit/test_jwt.py --ignore=tests/unit/test_redis.py