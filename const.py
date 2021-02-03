class Const(object):
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't change const.%s" % name)
        if not name.isupper():
            raise self.ConstCaseError('const name "%s" is not all supercase' % name)

        self.__dict__[name] = value


const = Const()

# mysql
const.DB_HOST = '139.196.53.66'
const.DB_USER = 'root'
const.DB_PASS = 'Duyimin1996'
const.DB_NAME = 'baostock'
const.DB_PORT = 3306
