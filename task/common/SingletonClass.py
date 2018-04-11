from functools import wraps


class SingletonClass(object):
    """
    单例模式
    # 实现__new__方法
    # 并在将一个类的实例绑定到类变量_instance上,
    # 如果cls._instance为None说明该类还没有实例化过,实例化该类,并返回
    # 如果cls._instance不为None,直接返回cls._instance
    """
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(SingletonClass, cls)  # farther class
            cls._instance = orig.__new__(cls)
        return cls._instance  # 具体的实例


def singletonfunc(cls):
    """
    单例模式
    # 使用装饰器来装饰某个类，使其只能生成一个实例
    """
    instances = {}
    @wraps(cls)
    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return getinstance


class Singleton(type):
    """
    单例模式
    元类（metaclass）可以控制类的创建过程：拦截类的创建、修改类的定义、返回修改后的类

    # Python2
    # class MyClass(object):
    #     __metaclass__ = Singleton

    # Python3
    # class MyClass(metaclass=Singleton):
    #    pass
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

