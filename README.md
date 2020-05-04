In order to test the Executor utility class, you'll need the two bash 
scripts provided in the `tests/scripts` directory.
The first represents a process that's successful.

```bash
#!/bin/bash

sleep $1
```

And the second represents a process that has failed.

```bash
#!/bin/bash

sleep $1
exit 1
```

In order to start testing, install the wheel as follows along with the
`requirements.txt`:
```
pip install 
pip install -r requirements.txt
```

Once installed, go ahead and start `ipython`.

Both scripts represent variable length user processes that naturally are 
submitted and that could either succeed or fail. We will start `n` total
instances, with a `max_worker` count of `4`.

```python
from pprint import pprint
import os
from pprint import pprint
from random import randint, random
from time import sleep 

from pyaestro.utilities.executor import Executor

# Pathing
success = './tests/scripts/sleep.sh'
fail = './tests/scripts/fail.sh'
ws = './workspace'

# Configuration
j_min = 5    # seconds
j_max = 300  # seconds
fail_rate = 0.15
max_workers = 4
n = 30

# Setup
os.mkdirs(ws)
executor = Executor(max_workers) 
jobids = []

# Start processes
for i in range(0, n):
    p_fail = random()
    if p_fail > fail_rate:
        jobid = executor.submit(
            success, ws, str(randint(j_min, j_max))) 
    else:
        jobid = executor.submit(
            fail, ws, str(randint(j_min, j_max)))

    jobids.append(jobid)
    print("JOBID: ", jobid, " -- ", executor.get_status(jobid)) 
    print(f"{i}: Looping...")
```

Once this executes, go ahead and run the following command, and it 
should look similar to below:

```python
pprint(dict(executor.get_all_status()))

```