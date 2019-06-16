from .base import Module
from textwrap import wrap


class Handshake(Module):
    DESCRIPTION = "Generate Twitter handshake format messages"
    ARGC = 3

    def max_length(self, lines):
        length = 0
        for line in lines:
            length = max(length, len(line))
        return length

    def handshake(self, left, right, middle):
        side_width = 20
        middle_width = side_width
        left = wrap(left, side_width)
        right = wrap(right, side_width)
        middle = wrap(middle, middle_width)
        left_length = self.max_length(left)
        right_length = self.max_length(right)
        middle_length = self.max_length(middle)
        if len(left) > len(right):
            right = [""] * (len(left) - len(right)) + right
        elif len(right) > len(left):
            left = [""] * (len(right) - len(left)) + left
        lines = []
        for line in range(len(left)):
            lines.append(left[line].rjust(left_length) + (" " * middle_length) + right[line])
        lines.append(" " * (left_length + middle_length // 2 - 1) + "🤝")
        for line in middle:
            lines.append(" " * left_length + line)

        return "\n".join(lines)

    def response(self, query, message):
        phrases = self.lines(query)[:self.ARGC]

        # Split list into variable names
        left, right, middle = phrases
        return self.safe_spaces(self.handshake(left, right, middle))
