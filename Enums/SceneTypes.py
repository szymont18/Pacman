from enum import Enum


class SceneTypes(Enum):
    MAIN = 0
    START = 1
    LEVEL_CREATOR = 2
    INSTRUCTIONS = 3
    LEADER = 4
    SETTINGS = 5
    EXIT = 6

    @staticmethod
    def to_int(scene_type):
        if scene_type == SceneTypes.MAIN: return 0
        elif scene_type == SceneTypes.START: return 1
        elif scene_type == SceneTypes.LEVEL_CREATOR: return 2
        elif scene_type == SceneTypes.INSTRUCTIONS: return 3
        elif scene_type == SceneTypes.LEADER: return 4
        elif scene_type == SceneTypes.SETTINGS: return 5
        else: return 6




