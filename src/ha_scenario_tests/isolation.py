"""Worker-only I/O guard, not an OS security sandbox."""

import sys

BLOCKED = {
    "socket.connect",
    "socket.bind",
    "socket.getaddrinfo",
    "socket.gethostbyname",
    "socket.gethostbyaddr",
    "socket.sendto",
    "socket.sendmsg",
    "subprocess.Popen",
    "os.system",
    "os.posix_spawn",
    "os.posix_spawnp",
    "os.exec",
    "os.fork",
}


def install_guard():
    violations = []

    def audit(event, args):
        if event in BLOCKED:
            violations.append(event)
            raise RuntimeError("scenario worker blocked I/O: " + event)

    sys.addaudithook(audit)
    return violations
