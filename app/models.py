from sqlalchemy import PickleType
from app import db
from sqlalchemy.ext.mutable import Mutable, MutableDict


class MutableDictInList(MutableDict):
    parent = None

    def __init__(self, parent, value):
        self.parent = parent
        super(MutableDictInList, self).__init__(value)

    def changed(self):
        if self.parent:
            self.parent.changed()


class MutableList(Mutable, list):
    """A list type that implements :class:`.Mutable`.

    """

    def __init__(self, value):
        super(MutableList, self).__init__(self._dict(v) for v in value)

    def _dict(self, value):
        value = MutableDictInList(self, value)
        return value

    def __setitem__(self, key, value):
        """Detect dictionary set events and emit change events."""
        list.__setitem__(self, key, self._dict(value))
        self.changed()

    def append(self, value):
        list.append(self, self._dict(value))
        self.changed()

    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, MutableList):
            if isinstance(value, list):
                return MutableList(value)
            return Mutable.coerce(key, value)
        else:
            return value

    def __getstate__(self):
        return list(dict(v) for v in self)

    def __setstate__(self, state):
        self[:] = [self._dict(value) for value in state]


class Game_obj(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uId = db.Column(db.String(30))
    # board = db.Column(ScalarListType(int))
    board = db.Column(PickleType())
    c_score = db.Column(db.Integer)


db.create_all()
