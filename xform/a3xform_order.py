'''Order Handling Routines'''


class A3Order(object):
    class GeneralException(Exception):
        pass

    def execute(self):
        # may add parallel execution
        return self._execute()

