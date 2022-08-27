import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def make_plot(conflu_list):

    plt.plot(conflu_list)
    plt.xlabel('frame')
    plt.ylabel('confluency(%)')
    plt.show()
