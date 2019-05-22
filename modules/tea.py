from .base import Module
from textwrap import wrap

CUP = r""">
          (
      )      )
    )     (      )
_(___(____)____(___(_
\ {} /__
 \ {} /   |
  \ {} /____|
   \ {} /
    \ {} /
     \_________/"""


class Tea(Module):
    DESCRIPTION = "Spills the tea."
    ARGC = 1
    ARGUMENT_WARNING = "Please specify tea to spill!"

    def width(self, row):
        """
        Given the number of the row, calculate how long that row should be.
        """
        return 17 - 2 * row

    def response(self, query, message):
        num_rows = 5
        lines = []
        offset = 0
        for row in range(0, num_rows):
            width = self.width(row)
            wrapped = wrap(query, width)
            line = wrapped[0] if len(wrapped) > 0 else ""
            lines.append(line.ljust(width))
            query = " ".join(wrapped[1:])
        tea = CUP.format(*lines).replace(" ", " ")
        return tea
