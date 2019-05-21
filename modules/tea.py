from .base import Module

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
        lines = []
        offset = 0
        for row in range(0, 5):
            lines.append(("{0: <" + str(self.width(row)) + "}").format(query[offset:offset + self.width(row)]))
            offset += self.width(row)
        # TODO: Format this list more efficiently
        tea = CUP.format(*lines).replace(" ", " ")
        return tea
