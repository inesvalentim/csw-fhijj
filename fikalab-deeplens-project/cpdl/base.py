"""
Capture - Process - Display - Loop base class
Authors: Diana Mendes, Samuel Pedro & Jason Bolito
"""
import time
from abc import ABCMeta, abstractmethod
from collections import OrderedDict

from concurrent.futures import ThreadPoolExecutor
from typing import TypeVar, Generic

T = TypeVar('T')


def do_nothing(*_):
    pass


class CaptureProcessDisplayLoop(Generic[T]):
    __metaclass__ = ABCMeta

    # def __init__(self, executor: Executor = ThreadPoolExecutor(max_workers=2)):
    def __init__(self, executor=ThreadPoolExecutor(max_workers=2)):
        # self.__capture_handlers: OrderedDict[int, Tuple[Callable[np.ndarray], Callable[T]], Callable[np.ndarray]] = []
        self.__capture_handlers = OrderedDict()

        # self.__loop: bool = False
        self.__loop = False

        # self.__last_handler_id: int = 0
        self.__last_handler_id = 0

        # self.__executor: Executor = executor
        self.__executor = executor

        # self.__on_stop_handlers: List[Callable] = []
        self.__on_stop_handlers = []

        # def register_capture_handler(self, capture_handler: Callable[np.ndarray, T],
        #                              process_handler: Callable[T] = do_nothing) -> int:

    def register_capture_handler(self, capture_handler, process_handler=do_nothing):
        handler_id = self.__last_handler_id
        self.__capture_handlers[handler_id] = (capture_handler, process_handler)
        self.__last_handler_id += 1
        return handler_id

    def register_on_stop_handler(self, handler):
        self.__on_stop_handlers.append(handler)

    # def unregister_capture_handler(self, handler_id: int):
    def unregister_capture_handler(self, handler_id):
        del self.__capture_handlers[handler_id]

    # def __publish_capture_update(self, frame: np.ndarray, timestamp: float):
    def __publish_capture_update(self, frame, timestamp):
        for capture_handler, process_handler in self.__capture_handlers.values():
            output = capture_handler(frame, timestamp)
            self.__executor.submit(process_handler, output)

    # def __capture_new_frame(self) -> np.ndarray:
    @abstractmethod
    def _capture_new_frame(self):
        pass

    def start_loop(self, blocking=True):
        self.__loop = True
        if blocking:
            self.__start_loop_callable()
        else:
            self.__executor.submit(self.__start_loop_callable)

    def __start_loop_callable(self):
        while self.__loop:
            self.__publish_capture_update(self._capture_new_frame(), time.time())

    def stop_loop(self):
        self.__loop = False
        self.__executor.shutdown()
        for on_stop_handler in self.__on_stop_handlers:
            on_stop_handler()
