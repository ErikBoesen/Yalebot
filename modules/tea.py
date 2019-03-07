from .base import Module

CUP = '''>Today's tea:

          (
      )      )
    )     (      )
_(___(____)____(___(_
\  {str0}  /__
 \  {str1}  /   |
  \  {str2}  /____|
   \  {str3}  /
    \  {str4}  /
     \_________/'''

class Tea(Module):
    DESCRIPTION = 'Spills the tea.'
    def response(self, query, message):
        lines = []
        offset = 0
        for row in range(0, 5):
            lines.append(('{0: <' + str(15-2*row) + '}').format(query[offset:offset+(15-2*row)]))
            offset += (15-2*row)

        tea = CUP.format(str0=lines[0], str1=lines[1], str2=lines[2], str3=lines[3], str4=lines[4]).replace(' ', ' ')
        return tea

print(Tea().response('this is a test', None))
