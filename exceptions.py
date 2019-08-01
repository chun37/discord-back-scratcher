class Signal(Exception):
    pass

class RestartSignal(Signal):
    pass

class EndSignal(Signal):
    pass