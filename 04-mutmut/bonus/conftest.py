import pathlib
import sys

# чтобы тесты видели grading.py из родительской папки
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
