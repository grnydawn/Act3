'''task classes'''



class A3Task(object):
    '''Stateless information converter

    input and output should be value not reference.
    '''

    # input is provided through __init__

    def input(self, inp):
        pass

    def output(self):
        pass

    def perform(self):
        pass
    

# each stage is a collection of tasks or is a kind of task
class A3Stage(A3Task):
    '''A collection of tasks or is a kind of a task'''

    def add_task(self, task):
        pass

# each chain is a series of stages or is a kind of stage
class A3Chain(A3Task):
    '''A series of stages of is a kind of a task'''

    def append_stage(self, stage):
        pass

    def insert_stage(self, index, stage):
        pass

# each cycle is repeats of a stage
class A3Cycle(A3Task):
    '''repeats of a chain or a kind of task'''
    pass

