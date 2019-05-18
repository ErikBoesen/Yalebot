from textwrap import wrap
SIDE_WIDTH = 20


def handshake(left, right, middle):
    left = wrap(left, SIDE_WIDTH)
    right = wrap(right, SIDE_WIDTH)
