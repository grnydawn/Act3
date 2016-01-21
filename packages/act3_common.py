import subprocess

# act3_common.py

# log


# exception


# system config



# constants


# utility functions
def pyrocall(func, *args, **kwargs):
    import Pyro4.util
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print("".join(Pyro4.util.getPyroTraceback()))
        raise e


def runcmd(cmd, input=None):
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, \
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return proc.communicate(input=input)
