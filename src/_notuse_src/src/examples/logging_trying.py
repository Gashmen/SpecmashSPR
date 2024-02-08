import logging

logger = logging.getLogger('__name__')
logger.setLevel(logging.DEBUG)
logger_file = logging.FileHandler(filename='test.txt')
logger_file.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(name)s %(message)s'))
logger.addHandler(logger_file)

logger.debug('debug information')
logger.info('info')

# logger.setLevel(logging.DEBUG)