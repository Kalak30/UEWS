# A decorator to create a static function variable
def static(name, val):
    def decorate(func):
        setattr(func, name, val)
        return func
    return decorate