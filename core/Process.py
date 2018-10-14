import subprocess

def run_and_return(process):
    proc = subprocess.Popen(process, stdout=subprocess.PIPE)
    out = proc.communicate()[0]
    return out

def run(process, logfile = None):
    if(logfile is None):
        return subprocess.call(process)
    else:
        with open(logfile, "w") as output_file:
            return subprocess.call(process, stdout = output_file, stderr = output_file)
