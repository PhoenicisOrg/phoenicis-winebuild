from orchestrator.Orchestrator import Orchestrator
from orchestrator.EnvironmentCreationTask import EnvironmentCreationTask
from core.Environment import Environment

environment = Environment("wine_osxcross", "linux", "x86")

orchestrator = Orchestrator()
orchestrator.run_task(EnvironmentCreationTask(environment))

import time
while(len(orchestrator.tasks()) > 0):
    print(orchestrator.tasks())
    time.sleep(1)

print("Done")
