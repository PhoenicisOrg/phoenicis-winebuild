import subprocess

def run_and_return(process):
    proc = subprocess.Popen(process, stdout=subprocess.PIPE)
    out = proc.communicate()[0]
    return out

def run(process):
    return subprocess.call(process)
