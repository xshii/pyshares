import os.path
from dataclasses import dataclass

VER = 0.1

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))


@dataclass
class MODULE:
    STOCK = "stock"


if __name__ == "__main__":
    print(PROJECT_ROOT)