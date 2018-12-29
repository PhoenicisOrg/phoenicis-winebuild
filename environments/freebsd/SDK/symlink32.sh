#!/bin/bash

ln -sf /usr/cross-freebsd/i368-pc-freebsd12/lib/libc.so.7 /usr/cross-freebsd/i368-pc-freebsd12/lib/libc.so
ln -sf /usr/cross-freebsd/i368-pc-freebsd12/lib/libthr.a /usr/cross-freebsd/i368-pc-freebsd12/lib/libpthread.a
ln -sf /usr/cross-freebsd/i368-pc-freebsd12/lib/libthr.so /usr/cross-freebsd/i368-pc-freebsd12/lib/libpthread.so
ln -sf /usr/cross-freebsd/i368-pc-freebsd12/lib/libthr_p.a /usr/cross-freebsd/i368-pc-freebsd12/lib/libpthread_p.a

ln -sf /usr/cross-freebsd/i368-pc-freebsd12/lib/include /usr/cross-freebsd/i368-pc-freebsd12/include

ln -sf /usr/cross-freebsd/i368-pc-freebsd12/include/sys/_semaphore.h /usr/cross-freebsd/i368-pc-freebsd12/include/_semaphore.h
ln -sf /usr/cross-freebsd/i368-pc-freebsd12/include/sys/aio.h /usr/cross-freebsd/i368-pc-freebsd12/include/aio.h
ln -sf /usr/cross-freebsd/i368-pc-freebsd12/include/sys/errno.h /usr/cross-freebsd/i368-pc-freebsd12/include/errno.h
ln -sf /usr/cross-freebsd/i368-pc-freebsd12/include/sys/fcntl.h /usr/cross-freebsd/i368-pc-freebsd12/include/fcntl.h
ln -sf /usr/cross-freebsd/i368-pc-freebsd12/include/sys/linker_set.h /usr/cross-freebsd/i368-pc-freebsd12/include/linker_set.h
ln -sf /usr/cross-freebsd/i368-pc-freebsd12/include/sys/poll.h /usr/cross-freebsd/i368-pc-freebsd12/include/poll.h
ln -sf /usr/cross-freebsd/i368-pc-freebsd12/include/sys/sched.h /usr/cross-freebsd/i368-pc-freebsd12/include/sched.h
ln -sf /usr/cross-freebsd/i368-pc-freebsd12/include/sys/stdatomic.h /usr/cross-freebsd/i368-pc-freebsd12/include/stdatomic.h
ln -sf /usr/cross-freebsd/i368-pc-freebsd12/include/sys/stdint.h /usr/cross-freebsd/i368-pc-freebsd12/include/stdint.h
ln -sf /usr/cross-freebsd/i368-pc-freebsd12/include/sys/syslog.h /usr/cross-freebsd/i368-pc-freebsd12/include/syslog.h
ln -sf /usr/cross-freebsd/i368-pc-freebsd12/include/sys/ucontext.h /usr/cross-freebsd/i368-pc-freebsd12/include/ucontext.h
ln -sf /usr/cross-freebsd/i368-pc-freebsd12/include/semaphore.h /usr/cross-freebsd/i368-pc-freebsd12/include/sys/semaphore.h

ln -sf /usr/cross-freebsd/i368-pc-freebsd12/include/machine/float.h /usr/cross-freebsd/i368-pc-freebsd12/include/float.h
ln -sf /usr/cross-freebsd/i368-pc-freebsd12/include/machine/floatingpoint.h /usr/cross-freebsd/i368-pc-freebsd12/include/floatingpoint.h
ln -sf /usr/cross-freebsd/i368-pc-freebsd12/include/machine/stdarg.h /usr/cross-freebsd/i368-pc-freebsd12/include/stdarg.h

ln -sf /usr/cross-freebsd/i368-pc-freebsd12/include/curses.h /usr/cross-freebsd/i368-pc-freebsd12/ncurses.h
