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
os.makedirs(ws, exist_ok=True)
executor = ProcessExecutor(max_workers)
jobids = []

# Start processes
for i in range(0, n):
    p_fail = random()
    if p_fail > fail_rate:
        print("Running a success.")
        jobid = executor.submit(
            success, ws, str(randint(j_min, j_max)))
    else:
        print("Running a failure.")
        jobid = executor.submit(
            fail, ws, str(randint(j_min, j_max)))

    jobids.append(jobid)
    print("JOBID: ", jobid, " -- ", executor.get_status(jobid))
    print(f"{i}: Looping...")
```

Once this executes, go ahead and run the following command:
```python
pprint(dict(executor.get_all_status()))
```

The output should look similar to:
```
{'00f6fa63-a6a4-4412-b56d-6469194f633f': <ExecTaskState.RUNNING: 3>,
 '0388f3f0-b6a6-424c-842e-e363208b0045': <ExecTaskState.PENDING: 2>,
 '0523a101-aa21-47f0-bf7f-57d0bccbfd3e': <ExecTaskState.PENDING: 2>,
 '0863cc38-ec4f-4a8b-82d9-5834a6ca17fe': <ExecTaskState.PENDING: 2>,
 '1b62623b-0ffa-4066-aaf3-cfd678b76833': <ExecTaskState.PENDING: 2>,
 '1b9eddd1-0b7a-40cb-bb32-55e9a4511912': <ExecTaskState.PENDING: 2>,
 '1c6e845a-8cfe-4a4a-95e0-2662ee0306fb': <ExecTaskState.PENDING: 2>,
 '1e534cf7-22ff-4d58-a9fc-9dd8352508c8': <ExecTaskState.PENDING: 2>,
 '2f163d9e-06b5-4d26-af1a-72ae8439b946': <ExecTaskState.PENDING: 2>,
 '302c808d-daee-4be2-ae74-dbb2ccfaead0': <ExecTaskState.PENDING: 2>,
 '34c3115c-71ab-4033-a208-22a52d2a92af': <ExecTaskState.PENDING: 2>,
 '38838bef-5c24-49d8-a832-3a82d5cc59ea': <ExecTaskState.PENDING: 2>,
 '4bd78b37-fed5-447a-a9d2-08192c75801c': <ExecTaskState.PENDING: 2>,
 '526160d2-c533-4ae9-b03f-67e1f8ea6b6c': <ExecTaskState.PENDING: 2>,
 '5801c730-5c06-4fbe-a792-8f7c6fcc84b0': <ExecTaskState.PENDING: 2>,
 '5ae9b9db-0c05-4e67-881a-f150dc75421c': <ExecTaskState.PENDING: 2>,
 '60a2828c-67c3-424e-a6cf-f5f3148a1a01': <ExecTaskState.RUNNING: 3>,
 '6573085e-506f-4e57-94d3-4c30e33033c7': <ExecTaskState.RUNNING: 3>,
 '6f455d3b-3dbd-4fde-bfda-d3aaecdf4da0': <ExecTaskState.RUNNING: 3>,
 '7d581194-af08-49a0-81bf-510e19a308c7': <ExecTaskState.PENDING: 2>,
 '93a1ab39-4766-4e2b-aae1-28a5f506fe6c': <ExecTaskState.PENDING: 2>,
 'a03a4c4d-ce0c-45cc-881d-463110419933': <ExecTaskState.PENDING: 2>,
 'a69a6631-3809-40ea-a4aa-9f3d8a2b3436': <ExecTaskState.PENDING: 2>,
 'a909db31-f16c-4642-8c79-bf1261c2e9ab': <ExecTaskState.PENDING: 2>,
 'ae105ae4-9cc4-4986-a694-7a9e58e80e7f': <ExecTaskState.PENDING: 2>,
 'c911caaf-1c34-46d1-a95b-6f432de54c7f': <ExecTaskState.PENDING: 2>,
 'de204bd0-8988-4fbe-a2f2-362f48aef4cd': <ExecTaskState.PENDING: 2>,
 'e09b2a73-3e5a-4d27-b6ff-524ac44187d9': <ExecTaskState.PENDING: 2>,
 'ecc0c983-ef8c-4d90-823a-28fe02d8ea98': <ExecTaskState.PENDING: 2>,
 'ffe2b0f4-2d07-4056-aaed-650613ec828c': <ExecTaskState.PENDING: 2>}
```

If you want to throw more into the mix:

```python
# Add more processes
for i in range(0, randint(5, n)):
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

You can cancel submitted processes by running:

```python
executor.cancel('<task uuid>')
```

or to cancel all

```python
executor.cancel_all()
```

Processes that have completed will not be reflected as cancelled.
These processes are considered to have terminated already with some
status code.