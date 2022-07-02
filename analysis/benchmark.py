# benchmark the performance of a mouse
# determining if the mouse can be considered trained
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-p', '--path', help='path to performance csv file in benchmark task')
parser.add_argument('-m', '--mouse', help='mice code for the animal')