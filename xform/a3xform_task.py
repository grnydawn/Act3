'''task classes'''


class A3Task(object):
    # input is provided through __init__

    def perform(self):
        pass
    

# each stage is a collection of tasks or is a kind of task
class A3Stage(A3Task):
    def add_task(self, task):
        pass

# each chain is a series of stages or is a kind of stage
class A3Chain(A3Stage):
    def append_stage(self, stage):
        pass

    def insert_stage(self, index, stage):
        pass

# each cycle is repeats of a stage
class A3Cycle(A3Chain):
    pass
