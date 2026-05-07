import re

logs = """
July 31 07:51:48 mycomputer bad_process[12345]: ERROR Disk full
July 31 08:00:01 mycomputer good_process[99]: INFO All good
July 31 08:15:22 mycomputer bad_process[67890]: ERROR Memory low
"""

pattern = r".*ERROR.*"
result = re.findall(pattern, logs)

for line in result:
    print(line)
