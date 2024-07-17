#!/usr/bin/env python3
import redis

# Connect to the Redis server
r = redis.Redis(host='localhost', port=6379, db=0)

# Set a value in Redis
r.set('name', 'John Doe')

# Get a value from Redis
name = r.get('name')
print(name.decode('utf-8'))  # Output: John Doe


