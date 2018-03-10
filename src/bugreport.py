
import sys
import platform
import os
import datetime
import traceback

import build_info


TEMPLATE = """
BUGREPORT {timestamp}

    ERROR:
        // This section contains information about the error.

        TYPE      : {error_type}
        VALUE     : {error_value}
        BACKTRACE : {error_trace}

    BUILD INFO:
        // This section contains informations about the system your executable was build on.

        TIMESTAMP : {build_timestamp}
        SYSTEM    : {build_system}
        COMMIT    : {build_commit}
        STATUS    : {build_status}
        USER      : {build_user}
        PACKAGES  : {build_packages}

    SYSTEM INFO:
        // This section contains informations about your system.

        SYSTEM   : {system_system}


"""

INDENT = '\n' + ' ' * 20

def bugreport(exc_info=None):
    typ, value, raw_trace = exc_info if exc_info is not None else sys.exc_info()
    trace = ''.join('{}:{}  {}  {}'.format(*frame) for frame in traceback.extract_tb(raw_trace, 32))

    def prepare(value):
        iterable = None
        if isinstance(value, str):
            iterable = value.split('\n')
        else:
            try:
                iterable = iter(value)
            except:
                iterable = [str(value)]
        return INDENT.join(filter(None, iterable))

    aliases = platform.system_alias(platform.system(), platform.release(), platform.version())
    system = '{} {} {}'.format(*aliases)

    report = TEMPLATE.format(
            timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            error_type=prepare(typ),
            error_value=prepare(value),
            error_trace=prepare(trace),
            build_timestamp=prepare(build_info.TIMESTAMP),
            build_system=prepare(build_info.SYSTEM),
            build_commit=prepare(build_info.COMMIT),
            build_status=prepare(build_info.STATUS),
            build_user=prepare(build_info.USER),
            build_packages=prepare(build_info.PACKAGES),
            system_system=prepare(system))

    report_directory = os.path.expanduser('~')
    report_file = os.path.join(report_directory, 'bug-downstairs.txt')

    # with 'w' we override,... but i dont want to grow the file uncontrolled,
    # so maybe i rewrite it later to append,.. but then we need some kind of
    # ring buffer.
    with open(report_file, 'w') as f:
        f.write(report)


if __name__ == '__main__':
    try:
        x = 0
        y = 1
        z = y / x
    except:
        bugreport()



