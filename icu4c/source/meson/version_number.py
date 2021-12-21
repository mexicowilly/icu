import sys
import re

with open(sys.argv[1]) as f:
  for line in f:
    m = re.match('[ \t]*#define[ \t]+' + sys.argv[2] + '[ \t]+"(.*)"', line)
    if m:
      print(m.group(1))
      break
