from typing import List

from converter.globals import NO_HOMING_YET, HomingSequence, HomingSequences
from converter.motor import Motor


class Group:
    def __init__(self, group, pre, post, checks):
        self.group_num = group
        self.pre = pre
        self.post = post
        self.checks = checks

        self.htype = NO_HOMING_YET
        self.sequence: HomingSequence = HomingSequence()
        self.motors: List[Motor] = []

        self.error = 0
        self.error_msg = ""

    def set_htype(self, htype: int):
        if self.htype == NO_HOMING_YET:
            self.htype = htype = htype
            self.sequence = HomingSequences[htype]
        elif self.htype != htype:
            self.error = 1
            self.error_msg = "Mixed Homing types in a group is not supported"
