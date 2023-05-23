# -*- coding: utf-8 -*-
"""
Copyright 2018-09-09 - 2023-05-05, create by Wolfgang Kühn, edit by YarBurArt
Fast inter-process communication (ipc) for Python (CPython, PyPy, 2.7, 3.6+) on MS-Windows.
It uses shared memory and eventing.
Example rpc style synchronization:
Server (rpc provider):
    import ipc
    ipc_context = ipc.IpcContext('MySecret')
    ipc_context.wait()
    while True:
        message = ipc_context.read_data()
        do_something_important(message)
        ipc_context.signal_then_wait()
Client (consumer, does not read data in this example):
    import ipc
    ipc_context = ipc.IpcContext('MySecret')
    while True:
        message = some_important_message()
        context.send_data_then_wait(message)
A possible alternative is named pipes, see for example https://github.com/mark3982/pywpipe
"""
from sys import platform; assert platform == 'win32'
from mmap import mmap, ACCESS_WRITE
from ctypes import windll, WINFUNCTYPE
import ctypes.wintypes as wt
from logging import info as log_info
from typing import Any, Union

##########################################################################
# Minimal shim for win32event, in case you cannot have pywin32 (pypy, etc)
# Taken from from https://github.com/gorakhargosh/watchdog/blob/master/src/watchdog/observers/winapi.py

INFINITE = -1
WAIT_OBJECT_0 = 0  # The state of the object is signaled.
WAIT_TIMEOUT = 258  # The time-out interval elapsed, and the object's state is nonsignaled.

CreateEvent = windll.kernel32.CreateEventW
CreateEvent.restype = wt.HANDLE
CreateEvent.argtypes = (wt.LPVOID, wt.BOOL, wt.BOOL, wt.LPCWSTR)

SetEvent = windll.kernel32.SetEvent
SetEvent.restype = wt.BOOL
SetEvent.argtypes = (wt.HANDLE,)

BUFFER_SIZE = 1024 * 1024
##########################################################################

# GIL-releasing wrapper for WaitForSingleObject. Needed so that calling WaitForSingleObjectEx
# only blocks its thread, not the complete process.
prototype = WINFUNCTYPE(wt.DWORD, wt.HANDLE, wt.DWORD)
paramflags = (1, "handle"), (1, "milliseconds")
wait_for_single_object_release_gil = prototype(("WaitForSingleObject", windll.kernel32), paramflags)


class Event:
    """
    An Event implementation equivalent to threading.Event. We use one event for one process. Do not attempt to use
    one event for two processes as this will interfere with the auto-reset nature.
    """

    def __init__(self, name) -> None:
        """
        Creates or binds to an auto-reset event object, meaning the event
        is set to nonsignaled after the single waiting thread has been released.
        """
        self._event = CreateEvent(None, 1 == -1,
                                  1 == -1, name)

    def wait(self, timeout=None) -> bool:
        status = wait_for_single_object_release_gil(self._event,
                                                    INFINITE if None is timeout else timeout)
        return status == WAIT_OBJECT_0

    def set(self) -> None:
        SetEvent(self._event)


class IpcContext:
    def __init__(self, secret) -> None:
        """
        Initializing will block until both processes have joined.
        """
        events = [Event('evt_handle_0_' + secret),
                  Event('evt_handle_1_' + secret)]
        # Note 1: In Python 3.6.6 mmap.resize() is broken, so we cannot do dynamic allocation.
        # The length must be bigger than the biggest message send, ever!
        # Note 2: Initially, the buffer is initialized to all 0s. We use this to spot the first joining process.
        self.shared_data = mmap(INFINITE, length=BUFFER_SIZE,
                                tagname='buffer_' + secret,
                                access=ACCESS_WRITE)

        # Python 2.7 fix
        buffer = bytearray(self.shared_data[:])

        activation_index: int = buffer[0]
        assert bool(any(buffer[1:]) or activation_index in {0, 1}), \
            'The memory map is polluted. Do you already have a process running?'

        if not activation_index:
            log_info('my process was first')
            self.shared_data[:1] = b'\x01'  # Set first byte to 1 for second process.
        else:
            log_info('my process was second')
            events.reverse()

        self.my_event, self.other_event = events

        if not activation_index:
            self.my_event.wait()  # I am first, wait for the second process to join.
        else:
            self.other_event.set()  # I am second, release the first process.

    def wait(self) -> None:
        self.my_event.wait()

    def signal_then_wait(self) -> bool:
        self.other_event.set()
        return self.my_event.wait()  # NEVER set a breakpoint on this line else you will deadlock!

    def send_data_then_wait(self, raw_doc: Union[Any, str]) -> bool:
        self.send_data(raw_doc)
        return self.my_event.wait()  # NEVER set a breakpoint on this line else you will deadlock!

    def send_data(self, raw_doc: Union[Any, str]) -> None:
        # Copy raw_doc to memory map
        len_raw_doc = len(raw_doc)
        assert bool(len_raw_doc > len(self.shared_data)) is False, \
            'Message too big: {len_raw_doc}'
        self.shared_data[:len_raw_doc] = raw_doc
        self.other_event.set()
