import re
import os
from python_settings import settings


string = "R-PL111161"
os.environ["SETTINGS_MODULE"] = 'settings'

print(settings.PATTERN)
pattern = re.compile(settings.PATTERN)
result = re.search(pattern, string)
print(result)

if re.search(pattern, string):
    print("re ok")