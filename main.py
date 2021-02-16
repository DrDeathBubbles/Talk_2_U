import logging
from logging import handlers
import multiprocessing

from listener import listener_process
from worker import worker_process


logger = logging.getLogger(__name__)  # use module name


def root_configurer(queue):
    h = handlers.QueueHandler(queue)
    root = logging.getLogger()
    root.addHandler(h)
    root.setLevel(logging.DEBUG)


def main():
    queue = multiprocessing.Queue(-1)
    listener = multiprocessing.Process(
        target=listener_process, args=(queue,))
    listener.start()

    root_configurer(queue)

    logger.info('Logging from main')
    workers = []
    for i in range(3):
        worker = multiprocessing.Process(target=worker_process, args=(queue,))
        workers.append(worker)
        worker.start()
    for w in workers:
        w.join()
    logger.info('main function ends')


if __name__ == '__main__':
    main()