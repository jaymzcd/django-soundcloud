import logging


def setup_logging(name='soundcloud_import', level=logging.DEBUG):
    # Taken as-is from: http://docs.python.org/2/howto/logging.html#configuring-logging
    logger = logging.getLogger(name)
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
