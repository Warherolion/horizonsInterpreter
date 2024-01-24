from Horizons import horizonsMainRun

import json


d = horizonsMainRun("499")

a = {}
a.update({"data":d})

b = json.dumps(a)
print (b)
