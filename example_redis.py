#import the library
import redis
# Create connection object
r = redis.Redis(host='redis-10386.c10.us-east-1-3.ec2.cloud.redislabs.com', port=10386)
# set a value for the foo object
r.set('foo', 'bar')
# retrieve and print the value for the foo object
print(r.get('foo'))