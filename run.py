# -*- coding: utf-8 -*-
import sys
import os

# A�adir el directorio del proyecto al PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from MainWindow.main_window import main

if __name__ == '__main__':
    main()