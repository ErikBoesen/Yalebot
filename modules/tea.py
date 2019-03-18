from .base import Module

CUP = r""">Today"s tea:

          (
      )      )
    )     (      )
_(___(____)____(___(_
\ {str0} /__
 \ {str1} /   |
  \ {str2} /____|
   \ {str3} /
    \ {str4} /
     \_________/"""


class Tea(Module):
    DESCRIPTION = "Spills the tea."
    ARGC = 1

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
        tea = CUP.format(str0=lines[0], str1=lines[1], str2=lines[2], str3=lines[3], str4=lines[4]).replace(" ", " ")
        return tea
