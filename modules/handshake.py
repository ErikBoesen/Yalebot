from .base import Module
from textwrap import wrap


class Handshake(Module):
    DESCRIPTION = "Generate Twitter handshake format messages"
    ARGC = 3

    def max_length(lines):
        length = 0
        for line in lines:
            length = max(length, len(line))
        return length

    def handshake(left, right, middle):
        SIDE_WIDTH = 20
        MIDDLE_WIDTH = SIDE_WIDTH
        EMOJI = "🤝"
        left = wrap(left, SIDE_WIDTH)
        right = wrap(right, SIDE_WIDTH)
        middle = wrap(middle, MIDDLE_WIDTH)
        left_length = max_length(left)
        right_length = max_length(right)
        middle_length = max_length(middle)
        if len(left) > len(right):
            right = [""] * (len(left) - len(right)) + right
        elif len(right) > len(left):
            left = [""] * (len(right) - len(left)) + left
        lines = []
        for line in range(len(left)):
            lines.append(left[line].rjust(left_length) + (" " * middle_length) + right[line])
        lines.append(" " * (left_length + middle_length // 2 - 1) + EMOJI)
        for line in middle:
            lines.append(" " * left_length + line)

        return "\n".join(lines)

    def response(self, query, message):
        phrases = self.lines(query)[:self.ARGC]

        # Split list into variable names
        left, right, middle = phrases
        return self.safe_space(self.handshake(left, right, middle))
