import pytest
from insights.parsers.uname import Uname
from insights.parsers.redhat_release import RedhatRelease
from insights.combiners.redhat_release import redhat_release
from insights.tests import context_wrap

UNAME = "Linux localhost.localdomain 3.10.0-327.rt56.204.el7.x86_64 #1 SMP PREEMPT RT Thu Oct 29 21:54:23 EDT 2015 x86_64 x86_64 x86_64 GNU/Linux"
BAD_UNAME = "Linux localhost.localdomain 2.6.24.7-101.el5rt.x86_64 #1 SMP PREEMPT RT Thu Oct 29 21:54:23 EDT 2015 x86_64 x86_64 x86_64 GNU/Linux"

REDHAT_RELEASE = """
Red Hat Enterprise Linux Server release 7.2 (Maipo)
""".strip()

FEDORA = """
Fedora release 23 (Twenty Three)
""".strip()


def test_uname():
    un = Uname(context_wrap(UNAME))
    expected = (7, 2)
    result = redhat_release(None, un)
    assert result.major == expected[0]
    assert result.minor == expected[1]


def test_redhat_release():
    rel = RedhatRelease(context_wrap(REDHAT_RELEASE))
    expected = (7, 2)
    result = redhat_release(rel, None)
    assert result.major == expected[0]
    assert result.minor == expected[1]


def test_both():
    un = Uname(context_wrap(UNAME))
    rel = RedhatRelease(context_wrap(REDHAT_RELEASE))
    expected = (7, 2)
    result = redhat_release(rel, un)
    assert result.major == expected[0]
    assert result.minor == expected[1]


def test_raise():
    un = Uname(context_wrap(BAD_UNAME))
    with pytest.raises(Exception):
        redhat_release(None, un)
