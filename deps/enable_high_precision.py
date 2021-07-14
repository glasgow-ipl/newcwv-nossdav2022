

with open('/etc/rsyslog.conf') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line == '$ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat\n':
        lines[i] = '# ' + lines[i]
        break

with open('/etc/rsyslog.conf', 'w') as f:
    f.write(''.join(lines))
