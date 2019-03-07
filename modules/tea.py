from .base import Module

CUP = '''>today's tea:

          (
      )      )
    )     (      )
_(___(____)____(___(_
\                   /__
 \  {str1}  /   |
  \  {str2}  /____|
   \  {str3}  /
    \  {str4}  /
     \_________/'''

class Tea(Module):
    DESCRIPTION = 'Spills the tea.'
    def response(self, query, message):
        msg1 = '{0: <13}'.format(query[0:13])
        msg2 = '{0: <11}'.format(query[13:24])
        msg3 = '{0: <9}'.format(query[24:33])
        msg4 = '{0: <7}'.format(query[33:40])

        tea = CUP.format(str1=msg1, str2 = msg2, str3 = msg3, str4 = msg4).replace(' ', ' ')
        return tea
