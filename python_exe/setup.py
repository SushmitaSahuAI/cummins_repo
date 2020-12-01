# -*- coding: utf-8 -*-
"""


@author: 565637
"""

from cx_Freeze import setup, Executable

base = None
#import os
#os.environ['TCL_LIBRARY'] = r'C:\ProgramData\Anaconda3\tcl\tcl8.6'
#os.environ['TK_LIBRARY'] = r'C:\ProgramData\Anaconda3\tcl\tk8.6'

executables = [Executable("K-Medoids_demo.py", base=base)]

packages = ["pandas","pyclustering","time","math","pickle","numpy"]
options = {
    'build_exe': {

        'packages':packages,
    },

}

setup(
    name = "KMedoids",
    options = options,
    version = "1.0",
    description = 'python for K-medoid clustering',
    executables = executables
)