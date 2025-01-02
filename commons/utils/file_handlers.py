import os
import shutil

from commons.config.logging_config import get_logger


class FileHandlers(object):

    def __init__(self):
        self.logger = get_logger("FileHandlers")
        self.logger.info("File Handlers")

    def delete_file_or_directory(self, filepath):
        if os.path.exists(filepath):
            for item in os.listdir(filepath):
                item_path = os.path.join(filepath, item)
                # Remove file if it's a file
                if os.path.isfile(item_path):
                    os.remove(item_path)
                    self.logger.info(f"Deleted file: {item_path}")
                    # Remove directory and all its contents if it's a directory
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    self.logger.info(f"Deleted directory and its contents: {item_path}")

