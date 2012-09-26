# -*- coding: utf-8 -*-
import sys, os
def daemonize (stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    # Perform first fork.
    try:
        pid = os.fork( )
        if pid > 0:
            sys.exit(0) # Exit first parent.
    except OSError, e:
        sys.stderr.write("fork #1 failed: (%d) %sn" % (e.errno, e.strerror))
        sys.exit(1)
    # Decouple from parent environment.
    cwd_save = os.getcwd()
    os.chdir("/")
    os.umask(0)
    os.setsid( )
    
    # The process is now daemonized, redirect standard file descriptors.
    if stdout == '/dev/null' or stdout[0] == '/':
        for f in sys.stdout, sys.stderr: f.flush( )
        so = file(stdout, 'a+')
        se = file(stderr, 'a+', 0)
    
    else:
        for f in sys.stdout, sys.stderr: f.flush( )
        so = file(__file__[:-12] + stdout, 'a+')
        se = file(__file__[:-12] + stderr, 'a+', 0)

    si = file(stdin, 'r')
    os.dup2(si.fileno( ), sys.stdin.fileno( ))
    os.dup2(so.fileno( ), sys.stdout.fileno( ))
    os.dup2(se.fileno( ), sys.stderr.fileno( ))
    os.chdir(cwd_save)
