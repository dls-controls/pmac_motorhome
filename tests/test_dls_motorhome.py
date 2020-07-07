from filecmp import cmp
from pathlib import Path

from dls_motorhome.commands import (
    Controller,
    PostHomeMove,
    command,
    comment,
    group,
    home_home,
    home_hsw,
    home_limit,
    home_slits_hsw,
    motor,
    plc,
)

# TODO Arvinders original tests could be reinstated but the new Group object
# must be created with some parameters

# import pytest

# from dls_motorhome._snippets import P_VARIABLE_API
# from dls_motorhome.group import Group

# def test_Group_class_is_context_manager():
#     assert hasattr(Group(), "__enter__")
#     assert hasattr(Group(), "__exit__")


# def test_Group_class_has_axes_attr():
#     assert hasattr(Group(), "axes")


# def test_plc_number_set_to_default_if_not_specified():
#     assert Group().plc_number == 9


# def test_plc_number_set_to_argument_parameter():
#     assert Group(plc_number=10).plc_number == 10


# def test_plc_number_must_be_within_range():
#     plc_number_min = 8
#     plc_number_max = 32
#     with pytest.raises(ValueError):
#         Group(plc_number=plc_number_max + 1)
#         Group(plc_number=plc_number_min - 1)
#         Group(plc_number=10.0)


# def test_Group_object_has_Pvar_api_in_string_list():
#     g = Group()
#     assert P_VARIABLE_API in g.code()


# def test_code_starts_with_CLOSE():
#     g = Group()
#     assert "CLOSE" in g.code().split("\n")[0]


# def test_timer_code_snippet_has_plc_number():
#     g = Group(plc_number=12)
#     lines = [line for line in g.code().split("\n") if "#define timer" in line]
#     assert "i(5111+(12&30)*50+12%2)" in lines[0]


# def test_code_has_Milliseconds_defined():
#     g = Group()
#     lines = [line for line in g.code().split("\n") if "#define MilliSeconds" in line]
#     print(lines)
#     assert "* 8388608/i10" in lines[0]


def test_BL07I_STEP_04_plc11():
    from dls_motorhome.commands import (
        motor,
        group,
        plc,
        comment,
        Controller,
        home_rlim,
    )

    file = "BL07I-MO-STEP-04.plc11"
    tmp_file = Path("/tmp") / file
    with plc(plc_num=11, controller=Controller.brick, filepath=tmp_file):
        motor(axis=1)
        motor(axis=2)
        motor(axis=4)
        motor(axis=5)

        with group(group_num=2, axes=[1, 2]):
            comment("RLIM", "None")
            home_rlim()

        with group(group_num=3, axes=[4, 5]):
            comment("RLIM", "None")
            home_rlim()

        this_path = Path(__file__).parent

    example = this_path / "examples" / file
    assert cmp(tmp_file, example), f"files {tmp_file} and {example} do not match"


# TODO add tests (and code) exactly like test_bl07i_step06_plc11 which reproduce
# existing examples generated by the original motorhome.py.
#
#
# Pick examples which exercise modes
# "HOME",
# "LIMIT",          done
# "HSW",            done
# "HSW_HLIM",
# "HSW_DIR",
# "RLIM",           done
# "NOTHING",
# "HSW_HSTOP"       done
# also exercise each of the post home move modes
#
# NOTE existing examples will require 'Convert Indentation to Spaces' VSCode cmd
# NOTE when tests fail you can easily see what has gone wrong with a command like:
#   code --diff tests/examples/BL18B-MO-STEP-01.plc13 /tmp/BL18B-MO-STEP-01.plc13


def test_BL02I_STEP_13_plc11():
    from dls_motorhome.commands import (
        motor,
        group,
        plc,
        comment,
        Controller,
        home_hsw_hstop,
    )

    file = "BL02I-MO-STEP-13.plc11"
    tmp_file = Path("/tmp") / file
    with plc(plc_num=11, controller=Controller.brick, filepath=tmp_file):
        motor(axis=1, jdist=-10000)
        motor(axis=2, jdist=-10000)
        motor(axis=3, jdist=10000)

        with group(group_num=2, axes=[1]):
            comment("HSW_HSTOP", "None")
            home_hsw_hstop()

        with group(group_num=3, axes=[2]):
            comment("HSW_HSTOP", "None")
            home_hsw_hstop()

        with group(group_num=4, axes=[3]):
            comment("HSW_HSTOP", "None")
            home_hsw_hstop()

        this_path = Path(__file__).parent

    example = this_path / "examples" / file
    assert cmp(tmp_file, example), f"files {tmp_file} and {example} do not match"


def test_BL18B_STEP01_plc13():
    file_name = "BL18B-MO-STEP-01.plc13"
    tmp_file = Path("/tmp") / file_name

    with plc(plc_num=13, controller=Controller.brick, filepath=tmp_file):
        motor(axis=1, jdist=-400)
        motor(axis=2, jdist=-400)
        motor(axis=3, jdist=-400)
        motor(axis=4, jdist=-400)

        initial = PostHomeMove.initial_position

        with group(group_num=2, axes=[1, 2], post_home=initial):
            comment(htype="HSW", post="i")
            home_hsw()

        with group(group_num=3, axes=[3, 4], post_home=initial):
            comment(htype="HSW", post="i")
            home_hsw()

    this_path = Path(__file__).parent
    example = this_path / "examples" / file_name
    assert cmp(tmp_file, example), f"files {tmp_file} and {example} do not match"


def test_BL20I_STEP02_plc11():
    file_name = "BL20I-MO-STEP-02.plc11"
    tmp_file = Path("/tmp") / file_name

    with plc(plc_num=11, controller=Controller.brick, filepath=tmp_file):
        motor(axis=3)
        motor(axis=4)
        motor(axis=5)
        motor(axis=6)
        motor(axis=1)
        motor(axis=2)
        motor(axis=7)

        initial = PostHomeMove.initial_position

        with group(group_num=2, axes=[3, 4], post_home=initial):
            comment(htype="LIMIT", post="i")
            home_limit()

        with group(group_num=3, axes=[5, 6], post_home=initial):
            comment(htype="LIMIT", post="i")
            home_limit()

        with group(group_num=4, axes=[1, 2], post_home=initial):
            comment(htype="LIMIT", post="i")
            home_limit()

        with group(group_num=5, axes=[7], post_home=initial):
            comment(htype="LIMIT", post="i")
            home_limit()

    this_path = Path(__file__).parent
    example = this_path / "examples" / file_name
    assert cmp(tmp_file, example), f"files {tmp_file} and {example} do not match"


def test_HOME_two_axes_post_L():
    file_name = "HOME_two_axes_post_L.pmc"
    tmp_file = Path("/tmp") / file_name
    with plc(plc_num=12, controller=Controller.brick, filepath=tmp_file):
        motor(axis=3, jdist=-500)
        motor(axis=4, jdist=-500)

        low_limit = PostHomeMove.hard_lo_limit

        with group(group_num=2, axes=[3, 4], post_home=low_limit):
            comment(htype="HOME", post="L")
            home_home()

    this_path = Path(__file__).parent
    example = this_path / "examples" / file_name
    assert cmp(tmp_file, example), f"files {tmp_file} and {example} do not match"


def test_BL18B_STEP01_plc13_slits():
    # generate a similar plc as test_BL18B_STEP01_plc13 but use the shortcut
    # home_slits() command
    # this separates the two pairs of slits so that they will not clash
    # the resulting PLC looks exactly like BL18B-MO-STEP-01.plc13 except that
    # it has an additional drive_to_limit for all axes at the start
    # and it has only one group instead of two
    file_name = "BL18B-MO-STEP-01_slits.plc13"
    tmp_file = Path("/tmp") / file_name
    with plc(plc_num=13, controller=Controller.brick, filepath=tmp_file):
        home_slits_hsw(
            group_num=2,
            posx=1,
            negx=2,
            posy=3,
            negy=4,
            jdist=-400,
            post=PostHomeMove.initial_position,
        )

    this_path = Path(__file__).parent
    example = this_path / "examples" / file_name
    assert cmp(tmp_file, example), f"files {tmp_file} and {example} do not match"


def test_any_code():
    # test the 'command' command which inserts arbitrary code
    file_name = "any_code.plc"
    tmp_file = Path("/tmp") / file_name
    with plc(plc_num=13, controller=Controller.brick, filepath=tmp_file):
        motor(axis=1)
        motor(axis=2)
        with group(group_num=2, axes=[1, 2]):
            command("Any old string will do for this test")
            command(" - multiple commands can be on the same line\n")

    this_path = Path(__file__).parent
    example = this_path / "examples" / file_name
    assert cmp(tmp_file, example), f"files {tmp_file} and {example} do not match"


def test_two_plcs():
    # verfiy that you can create two plcs in a single definition file
    file_name1 = "two_plcs1.pmc"
    tmp_file1 = Path("/tmp") / file_name1
    file_name2 = "two_plcs2.pmc"
    tmp_file2 = Path("/tmp") / file_name2

    with plc(plc_num=11, controller=Controller.brick, filepath=tmp_file1):
        motor(axis=1)

        with group(group_num=2, axes=[1]):
            home_hsw()

    with plc(plc_num=12, controller=Controller.brick, filepath=tmp_file2):
        motor(axis=2)

        with group(group_num=3, axes=[2]):
            home_hsw()

    this_path = Path(__file__).parent
    example1 = this_path / "examples" / file_name1
    example2 = this_path / "examples" / file_name2
    assert cmp(tmp_file1, example1), f"files {tmp_file1} and {example1} do not match"
    assert cmp(tmp_file2, example2), f"files {tmp_file2} and {example2} do not match"
