from framework.util import logger
import os
FILENAME = 'test-csv'

path = logger.createCSV(FILENAME)
logger.writeTo(path, 1, 1, 1)
