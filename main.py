import sys
import argparse # for handling command line arguments
import logging  # for handling debug output
import datetime # for printing time in the case of a crash

from PyQt5.QtWidgets import QApplication    # for starting UI

from ui.mainWindow import MainWindow    # local import

def main(debug):
    logging.info("Starting application.")
    app = QApplication(sys.argv)
    mainWindow = MainWindow(debug)
    sys.exit(app.exec_())

if __name__ == "__main__":
    # command line arguments
    parser = argparse.ArgumentParser(description="Passive Sonar Demonstration System")
    parser.add_argument('-d', '--debug', action='store_true', help="run application in debug mode")
    parser.add_argument('-v', '--verbose', action='store_true', help="run application with verbose outputs, prints which buttons are pressed")
    parser.add_argument('-a', '--amplitude', action='store_true', help="prints amplitudes of of input device during input mode")
    parser.add_argument('-b', '--bytes', action='store_true', help="prints size of input samples in bytes")
    parser.add_argument('-s', '--samples', action='store_true', help="prints number of samples received during each audio stream callback")
    parser.add_argument('-l', '--localization', action='store_true', help="prints localization angle with highest amplitude")
    parser.add_argument('-tb', '--time_buttons', action='store_true', help="prints button response time (ms)")
    parser.add_argument('-tp', '--time_processing', action='store_true', help="prints audio processing time (ms)")
    parser.add_argument('-tl', '--time_localization', action='store_true', help="prints audio processing + localization time (ms)")
    parser.add_argument('-tu', '--time_update', action='store_true', help="prints the time it takes for each plot update (ms)")
    args = parser.parse_args()
    debug = {
        "amplitude": False,
        "bytes": False,
        "samples": False,
        "localization": False,
        "time_buttons": False,
        "time_processing": False,
        "time_localization": False,
        "time_update": False,
    }

    # if using verbose output set logging to display level and message
    # print anything level debug or higher
    # logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

    if args.debug:
        # debug = True
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
        logging.debug("In DEBUG mode.")
    if args.verbose:
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
        # logging.info("Using verbose output.")
    if args.amplitude:
        debug["amplitude"] = True
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
    if args.bytes:
        debug["bytes"] = True
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
    if args.samples:
        debug["samples"] = True
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
    if args.localization:
        debug["localization"] = True
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
    if args.time_buttons:
        debug["time_buttons"] = True
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
    if args.time_processing:
        debug["time_processing"] = True
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
    if args.time_localization:
        debug["time_localization"] = True
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
    if args.time_update:
        debug["time_update"] = True
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
    # else:
    #     # if not using verbose output only print errors and warnings
    #     logging.basicConfig(format="%(levelname)s: %(message)s")

    try:
        main(debug)
    except Exception:
        print(f"ERROR OCCURRED AT: {datetime.datetime.now()}")
