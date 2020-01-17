

import pandas as pd
import os
import numpy as np
from sqlalchemy import create_engine

def acquire():
    sqlitedb_path = '../data/raw/abacucmendezsala.db'
    eng = create_engine(f'sqlite:///{sqlitedb_path}')
    return eng