import protocol_exp.touchtraining as touchtraining


def find_subclassess(module,clazz):
    print('TESTING', clazz)
    print('type: ',module)
    for name in dir(module):
        o = getattr(module,name)
        # print(o)
        print(name)

        try:
            if (o != clazz) and issubclass(o,clazz):
                yield name, o
        except TypeError: pass



print(list(find_subclassess(touchtraining,touchtraining.touchtraining_cls)))
