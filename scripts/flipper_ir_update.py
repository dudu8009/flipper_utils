#!/usr/bin/env python3

import os
import shutil

from flipper.app import App
from flipper.storage import FlipperStorage, FlipperStorageOperations
from flipper.utils.cdc import resolve_port


class Main(App):
    """
    A Flipper Zero file IRDB update utility.
    from the https://github.com/Lucaslhm/Flipper-IRDB repo
    Usage:
        flipper_irdb_update.py <src>
        flipper_irdb_update.py <src> <flipper_dest>
    """

    def init(self):
        self.parser.add_argument("-p", "--port", help="CDC Port", default="auto")
        self.parser.add_argument("src", help="Path to IRDB repo")
        self.parser.add_argument("--dst", help="Flipper IR path", default="/ext/infrared", required=False)
        self.parser.set_defaults(func=self.copy)

    def copy(self):
        if not (port := resolve_port(self.logger, self.args.port)):
            return 1

        try:
            """
            If the IRDB folder doesn't exits clones it from the IRDB repo
            If there is an IRDB folder, updates it from github and copies all valid folders to _IR_ and 
            uploads it to the flipper
            """

            flipper_path = self.args.dst
            irdb_path = self.args.src

            if not os.path.exists(irdb_path):
                self.logger.debug(f'Cloning IRDB to {irdb_path}')
                os.system(f'git clone https://github.com/Lucaslhm/Flipper-IRDB {irdb_path}')

            os.chdir(irdb_path)
            self.logger.debug(f'Updating IRDB')
            os.system("git pull")

            ir_folder = os.path.join(irdb_path, "_IR_")
            if not os.path.exists(ir_folder):
                self.logger.debug(f'Creating {ir_folder}')
                os.makedirs(ir_folder)

            # iterate over all files in the irdb repo and copy only the valid ones
            for folder in os.listdir(irdb_path):
                folder_name = os.path.join(ir_folder, folder)
                if os.path.isdir(folder) and not folder.startswith("_") and not folder.startswith("."):
                    self.logger.debug(f'Copying "{folder}" to "{folder_name}"')
                    shutil.copytree(folder, folder_name, dirs_exist_ok=True)

            with FlipperStorage(port) as storage:
                storage_ops = FlipperStorageOperations(storage)

                self.logger.info(f'Uploading "{ir_folder}" to "{flipper_path}"')
                storage_ops.recursive_send(flipper_path, ir_folder, force=True)

                return 0

        except Exception as e:
            self.logger.error(f"Error: {e}")
            # raise
            return 4


if __name__ == "__main__":
    Main()()
