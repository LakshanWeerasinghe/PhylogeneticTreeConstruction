from enum import IntEnum


class ProcessMethodTypes(IntEnum):
    LSH = 1
    K_MEDOID_LSH_CLUSTER = 2
    K_MER = 3
    K_MEDOID_K_MER_CLUSTER = 4

    @classmethod
    def choises(cls):
        return [(key.value, key.name) for key in cls]


class StatusTypes(IntEnum):
    PROGRESS = 1
    SUCCESS = 2

    @classmethod
    def choises(cls):
        return [(key.value, key.name) for key in cls]


class ProcessType(IntEnum):
    MATRIX_GENERATION = 1
    TREE_GENERATION = 2

    @classmethod
    def choises(cls):
        return [(key.value, key.name) for key in cls]
