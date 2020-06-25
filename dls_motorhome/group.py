from dls_motorhome.contants import PostHomeMove
from typing import List, Optional, cast

from .motor import Motor
from .template import Template


class Group:
    # TODO htype should have a class
    def __init__(
        self,
        group_num: int,
        axes: List[Motor],
        post_home: PostHomeMove,
        comment: str = None,  # supply a comment header for the group
    ) -> None:
        self.axes = axes
        self.post_home = post_home
        if comment is None:
            self.make_comment()
        else:
            self.comment = comment
        self.group_num = group_num
        self.templates: List[Template] = []

    the_group: Optional["Group"] = None

    def __enter__(self):
        assert not Group.the_group
        Group.the_group = self
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        Group.the_group = None

    @property
    def count(self) -> int:
        return len(self.templates)

    # this is a bit cheesy and really just for the tests to pass
    # I would recomment setting the comment in the Group constructor
    def make_comment(self, htype: str = "RLIM", post: str = "None") -> None:
        self.comment = "\n".join(
            [
                f";  Axis {ax.axis}: htype = {htype}, "
                f"jdist = {ax.jdist}, post = {post}"
                for ax in self.axes
            ]
        )

    @classmethod
    def add_snippet(cls, template_name: str, **args):
        # funky casting required for type hints since we init the_group to None
        group = cast("Group", cls.the_group)
        group.templates.append(Template(jinja_file=template_name, args=args))

    def _all_axes(self, format: str, separator: str, *arg) -> str:
        # to the string format: pass any extra arguments first, then the dictionary
        # of the axis object so its elements can be addressed by name
        all = [format.format(*arg, **ax.dict) for ax in self.axes]
        return separator.join(all)

    ############################################################################
    # the following functions are callled from Jinja templates to generate
    # snippets of PLC code that act on all motors in a group
    ############################################################################

    def jog_axes(self) -> str:
        return self._all_axes("#{axis}J^*", " ")

    def jog_axes_jdist(self) -> str:
        return self._all_axes("#{axis}J^*^{jdist}", " ")

    def set_large_jog_distance(self, negative: bool = True) -> str:
        sign = "-" if negative else ""
        return self._all_axes(
            "m{axis}72=100000000*({0}i{axis}23/ABS(i{axis}23))", " ", sign
        )

    def in_pos(self) -> str:
        return self._all_axes("m{axis}40", "&")

    def limits(self) -> str:
        return self._all_axes("m{axis}30", "|")

    def following_err(self) -> str:
        return self._all_axes("m{axis}42", "|")

    def homed(self) -> str:
        return self._all_axes("m{axis}45", "&")

    def clear_home(self) -> str:
        return self._all_axes("m{axis}45=0", " ")

    def store_position_diff(self):
        return self._all_axes(
            "P{pos}=(P{pos}-M{axis}62)/(I{axis}08*32)+{jdist}-(i{axis}26/16)",
            separator="\n        ",
        )

    def stored_pos_to_jogdistance(self):
        return self._all_axes("m{axis}72=P{pos}", " ")

    def jog_distance(self):
        return self._all_axes("#{axis}J=*", " ")

    def negate_home_flags(self):
        return self._all_axes("i{homed_flag}=P{not_homed}", " ")

    def restore_home_flags(self):
        return self._all_axes("i{homed_flag}=P{homed}", " ")

    def jog_to_home_jdist(self):
        return self._all_axes("#{axis}J^*^{jdist}", " ")

    def home(self) -> str:
        return self._all_axes("#{axis}hm", " ")
