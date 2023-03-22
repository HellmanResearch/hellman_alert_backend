from enum import Enum


class FiledType(Enum):
    INPUT = "input"
    CHOICE = "choice"
    SELECT = "select"

    @classmethod
    def get_choices(cls):
        return list(((filed.name, filed.value) for filed in cls._member_map_.values()))


if __name__ == '__main__':
    r = FiledType.get_choices()
    print(r)
