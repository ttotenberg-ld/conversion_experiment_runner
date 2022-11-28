from dotenv import load_dotenv #pip install python-dotenv
import ldclient
from ldclient.config import Config
import names
import os
import random
import time
import uuid
from utils.user_countries import random_country


'''
Get environment variables
'''
load_dotenv()

SDK_KEY = os.environ.get('SDK_KEY')
FLAG_NAME = os.environ.get('FLAG_NAME')
METRIC_NAME = os.environ.get('METRIC_NAME')
TRUE_PERCENT_CONVERTED = os.environ.get('TRUE_PERCENT_CONVERTED')
FALSE_PERCENT_CONVERTED = os.environ.get('FALSE_PERCENT_CONVERTED')
NUMBER_OF_ITERATIONS = os.environ.get('NUMBER_OF_ITERATIONS')


'''
Initialize the LaunchDarkly SDK
'''
ldclient.set_config(Config(SDK_KEY))


'''
Construct and return a random user
'''
def random_ld_user():
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    plan = random.choice(["free", "silver", "gold"])
    email = first_name + "." + last_name + random.choice(["@gmail.com", "@yahoo.com", "@hotmail.com"])

    user = {
        "key": str(uuid.uuid4()),
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "country": random_country(),
        "custom": {
          "plan": plan
        }
    }
    return user


'''
Conversion true or false calculator.
Pass in TRUE_PERCENT_CONVERTED or FALSE_PERCENT_CONVERTED, which refer to the true/false flag variation served
'''
def conversion_chance(chance_number):
    chance_calc = random.randint(1, 100)
    if chance_calc <= chance_number:
        return True
    else:
        return False


'''
Evaluate the flags for randomly generated users, and make the track() calls to LaunchDarkly
'''
def callLD():
    for i in range(int(NUMBER_OF_ITERATIONS)):

        random_user = random_ld_user()
        flag_variation = ldclient.get().variation(FLAG_NAME, random_user, False)

        if flag_variation:
            print("Executing " + str(flag_variation) + ": " + str(i+1) + "/" + NUMBER_OF_ITERATIONS)
            if conversion_chance(int(TRUE_PERCENT_CONVERTED)):
                ldclient.get().track(METRIC_NAME, random_user)

        else:
            print("Executing " + str(flag_variation) + ": " + str(i+1) + "/" + NUMBER_OF_ITERATIONS)
            if conversion_chance(int(FALSE_PERCENT_CONVERTED)):
                ldclient.get().track(METRIC_NAME, random_user)


'''
Execute!
'''
callLD()


'''
Flush any pending analytics events & the responsibly close the LD Client
'''
ldclient.get().flush()
ldclient.get().close()