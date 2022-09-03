import logging

logger = logging.getLogger(__name__)


class Todo:
    def __init__(self, file="todo.yaml"):
        if not path.isfile(file):
            logger.info("Todo file does not exist, creating one instead")
            try:
                Path(file).touch()
            except Exception as e:
                logger.critical(f"Failed to create Todo file ({file}): {e}")
                return

        with open(file, "r", encoding="utf-8") as file:
            self._raw = yaml.safe_load(file)


data = Todo()

for key in data._raw:
    print(key)
