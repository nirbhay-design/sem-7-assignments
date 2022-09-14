#!/bin/bash

python solve_primal.py Q1_features.csv Q1_class.csv q1_primal.png
python solve_primal.py Q2_features.csv Q2_class.csv q2_primal.png
python solve_primal.py Q3_features.csv Q3_class.csv q3_primal.png

python solve_dual.py Q1_features.csv Q1_class.csv q1_dual.png
python solve_dual.py Q2_features.csv Q2_class.csv q2_dual.png
python solve_dual.py Q3_features.csv Q3_class.csv q3_dual.png