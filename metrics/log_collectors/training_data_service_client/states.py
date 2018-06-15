#!/usr/bin/env python
"""manage state transition details"""

import os
import logging
import threading

# I seem to have problems exiting directly, so, this sleep seems to help.
# My unsubstantiated theory is that gRPC needs time to flush.
# Note since we signaled, we won't actually wait n seconds, the
# job monitor will delete us.
SLEEP_BEFORE_EXIT_TIME = 15

SLEEP_BEFORE_LC_DONE = 4.0

DURATION_SHUTDOWN_DELAY = 10.00

DURATION_SHUTDOWN_DELAY_TF = 5.00

global_state_lock = threading.Lock()

global_scanner_count = 0


def register_scanner():
    global global_scanner_count
    with global_state_lock:
        global_scanner_count += 1


def unregister_scanner():
    global global_scanner_count
    with global_state_lock:
        global_scanner_count -= 1


def is_learner_done(logger=None):
    logger = logger or logging.getLogger()
    learner_exit_file_path = os.path.join(os.environ["JOB_STATE_DIR"], "learner.exit")
    halt_file_path = os.path.join(os.environ["JOB_STATE_DIR"], "halt")
    # logging.debug("Checking is learner done: %s, %s", learner_exit_file_path, halt_file_path)
    learner_is_done = os.path.exists(learner_exit_file_path) or os.path.exists(halt_file_path)
    if learner_is_done:
        logger.debug("Learner is done!")
    return learner_is_done


def signal_lc_done(exit_code=0, logger=logging.getLogger()):
    global global_scanner_count
    logger.info("signal_lc_done, global_scanner_count (after release): %d", global_scanner_count)
    with global_state_lock:
        global_scanner_count -= 1
    pass
