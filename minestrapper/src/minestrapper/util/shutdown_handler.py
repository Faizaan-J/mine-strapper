import traceback
import atexit
import ctypes
import os
import signal
import sys
import threading

from time import sleep as wait

from typing import TYPE_CHECKING, Callable
if (TYPE_CHECKING):
    from minestrapper.server import Server

class ShutdownHandler:
    def __init__(self, server: "Server"):
        self.server = server
        self.shutdown_callbacks: list[Callable] = []

        self.__shutdown_initiated = False
        self.__shutdown_complete = False

        self.__lock = threading.Lock()
        
        atexit.register(self.__call_all)
        signal.signal(signal.SIGINT, self.__signal_handler)
        signal.signal(signal.SIGBREAK, self.__signal_handler)

        if (os.name == "nt"):
            handler_routine = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_uint)

            CTRL_C_EVENT = 0
            CTRL_BREAK_EVENT = 1
            CTRL_CLOSE_EVENT = 2
            CTRL_LOGOFF_EVENT = 5
            CTRL_SHUTDOWN_EVENT = 6
            possible_ctrl_types = (CTRL_C_EVENT, CTRL_BREAK_EVENT, CTRL_CLOSE_EVENT, CTRL_LOGOFF_EVENT, CTRL_SHUTDOWN_EVENT)
            
            @handler_routine
            def console_handler(ctrl_type):
                if (ctrl_type in possible_ctrl_types):
                    if (ctrl_type == CTRL_CLOSE_EVENT):
                        self.server.logger.warning(
                            "Terminal window is being closed directly. The Minecraft Server process may not be terminated properly.", 
                            "Please use the 'stop' command, use Ctrl + C, or some other safer method to stop the server gracefully"
                        )

                    self.__call_all()
                return False
            self.__console_handler = console_handler
                
            ctypes.windll.kernel32.SetConsoleCtrlHandler(console_handler, True)
        else:
            signal.signal(signal.SIGTERM, self.__signal_handler)

    def __signal_handler(self, *_):
        self.__call_all()

    def __call_all(self):
        with (self.__lock):
            if (self.__shutdown_initiated):
                return
            self.server.logger.info("Shutdown initiated")
            self.__shutdown_initiated = True
        
        if (self.shutdown_callbacks):
            for callback in self.shutdown_callbacks:
                try:
                    callback()
                except Exception:
                    self.server.logger.error(f"Error while executing shutdown callback: {traceback.format_exc()}")
        self.server.logger.info("Shutdown cleanup processes complete")
        self.__shutdown_complete = True

    def on_shutdown(self, callback: Callable):
        self.shutdown_callbacks.append(callback)

        return callback

    def request_shutdown(self):
        self.__call_all()

    @property
    def shutdown_initiated(self) -> bool:
        return self.__shutdown_initiated

    def wait_for_shutdown_complete(self):
        while (not self.__shutdown_complete):
            wait(0.1)
