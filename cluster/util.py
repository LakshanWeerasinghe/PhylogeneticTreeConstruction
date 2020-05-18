from enum import IntEnum


class ProcessMethodTypes(IntEnum):
    LSH = 1
    K_MEDOID_LSH_CLUSTER = 2
    K_MER = 3
    K_MEDOID_K_MER_CLUSTER = 4

    @classmethod
    def choises(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def get_key(cls, value):
        for keys in cls:
            if value == keys.value:
                return keys.name


class ProcessTypes(IntEnum):
    LSH = 1
    KMER = 2

    @classmethod
    def choises(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def get_key(cls, value):
        for keys in cls:
            if value == keys.value:
                return keys.name


class ProcessStatusTypes(IntEnum):
    PROGRESS = 1
    SUCCESS = 2
    FAILED = 3

    @classmethod
    def choises(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def get_key(cls, value):
        for keys in cls:
            if value == keys.value:
                return keys.name


class StatusTypes(IntEnum):
    PROGRESS = 1
    SUCCESS = 2

    @classmethod
    def choises(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def get_key(cls, value):
        for keys in cls:
            if value == keys.value:
                return keys.name


class TreeProcessType(IntEnum):
    TREE_CREATION = 1
    TREE_UPDATION = 2

    @classmethod
    def choises(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def get_key(cls, value):
        for keys in cls:
            if value == keys.value:
                return keys.name
