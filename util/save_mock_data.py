import sys
sys.path.append('..')

from themoviedb import get_cast_filmographies
from collections import OrderedDict
import json
cf = get_cast_filmographies("the martian")
with open('the_martian_cast_filmographies.json', 'w') as f:
    json.dump(cf, f, indent=4)
