import itertools
from copy import deepcopy
from typing import List, Callable
import random
import numpy as np

from prtpy import Bins, BinsKeepingContents


def base_check_bins(bins: Bins, items: List[any], valueof: Callable = lambda x: x) -> (Bins, bool):
    """
    This function is a base function for partition algorithms,
    It's get a list of items and number of bins (from the initialize given bins)
    and return True flag and the new bins if needed for base cases when k = 0, k = 1 or k = number of items
    The flag will equal to True if and only if this function has return a new bins (one of the base cases conditions was found)

    Author: Kfir Goldfarb
    Date: 08/06/2022
    Email: kfir.goldfarb@msmail.ariel.ac.il

    >>> base_check_bins(bins=BinsKeepingContents(0), items=[1, 2, 3, 4, 5, 6])[0].bins
    []

    >>> base_check_bins(bins=BinsKeepingContents(0), items=[1, 2, 3, 4, 5, 6])[1]
    True

    >>> base_check_bins(bins=BinsKeepingContents(0), items=[random.randint(0, 100) for i in range(random.randint(100, 1000))])[0].bins
    []

    >>> base_check_bins(bins=BinsKeepingContents(0), items=[random.randint(0, 100) for i in range(random.randint(100, 1000))])[1]
    True

    >>> base_check_bins(bins=BinsKeepingContents(1), items=[1, 2, 3, 4, 5, 6])[0].bins
    [[1, 2, 3, 4, 5, 6]]

    >>> base_check_bins(bins=BinsKeepingContents(1), items=[3, 6, 13, 20, 30, 40, 73])[0].bins
    [[3, 6, 13, 20, 30, 40, 73]]

    >>> base_check_bins(bins=BinsKeepingContents(1), items=[1, 2, 3, 4, 5, 6])[1]
    True

    >>> base_check_bins(bins=BinsKeepingContents(1), items=[random.randint(0, 100) for i in range(random.randint(100, 1000))])[1]
    True

    >>> base_check_bins(bins=BinsKeepingContents(1), items=[1])[0].bins
    [[1]]

    >>> base_check_bins(bins=BinsKeepingContents(5), items=[1, 2, 3, 4, 5])[0].bins
    [[1], [2], [3], [4], [5]]

    >>> base_check_bins(bins=BinsKeepingContents(6), items=[1, 2, 3, 4, 5, 6])[0].bins
    [[1], [2], [3], [4], [5], [6]]

    """
    flag = False
    k = bins.num
    if k == 0:
        flag = True
    elif k == 1:
        for item in items:
            bins.add_item_to_bin(item=item, bin_index=0)
        flag = True

    if not flag and len(items) == k:
        for index, item in enumerate(items):
            bins.add_item_to_bin(item=item, bin_index=index)
        flag = True

    return bins, flag


def get_best_best_k_combination(k_combinations):
    """
    This function get a k_combinations and return the combination that has the minimal different sum error

    Author: Kfir Goldfarb
    Date: 08/06/2022
    Email: kfir.goldfarb@msmail.ariel.ac.il

    >>> get_best_best_k_combination(k_combinations=[[[95], [85], [75, 25, 15, 5]], [[95], [75], [85, 25, 15, 5]], [[95], [25], [85, 75, 15, 5]], [[95], [15], [85, 75, 25, 5]], [[95], [5], [85, 75, 25, 15]], [[95], [85, 75], [25, 15, 5]], [[95], [85, 25], [75, 15, 5]], [[95], [85, 15], [75, 25, 5]], [[95], [85, 5], [75, 25, 15]], [[95], [75, 25], [85, 15, 5]], [[95], [75, 15], [85, 25, 5]], [[95], [75, 5], [85, 25, 15]], [[95], [25, 15], [85, 75, 5]], [[95], [25, 5], [85, 75, 15]], [[95], [15, 5], [85, 75, 25]], [[85], [75], [95, 25, 15, 5]], [[85], [25], [95, 75, 15, 5]], [[85], [15], [95, 75, 25, 5]], [[85], [5], [95, 75, 25, 15]], [[85], [95, 75], [25, 15, 5]], [[85], [95, 25], [75, 15, 5]], [[85], [95, 15], [75, 25, 5]], [[85], [95, 5], [75, 25, 15]], [[85], [75, 25], [95, 15, 5]], [[85], [75, 15], [95, 25, 5]], [[85], [75, 5], [95, 25, 15]], [[85], [25, 15], [95, 75, 5]], [[85], [25, 5], [95, 75, 15]], [[85], [15, 5], [95, 75, 25]], [[75], [25], [95, 85, 15, 5]], [[75], [15], [95, 85, 25, 5]], [[75], [5], [95, 85, 25, 15]], [[75], [95, 85], [25, 15, 5]], [[75], [95, 25], [85, 15, 5]], [[75], [95, 15], [85, 25, 5]], [[75], [95, 5], [85, 25, 15]], [[75], [85, 25], [95, 15, 5]], [[75], [85, 15], [95, 25, 5]], [[75], [85, 5], [95, 25, 15]], [[75], [25, 15], [95, 85, 5]], [[75], [25, 5], [95, 85, 15]], [[75], [15, 5], [95, 85, 25]], [[25], [15], [95, 85, 75, 5]], [[25], [5], [95, 85, 75, 15]], [[25], [95, 85], [75, 15, 5]], [[25], [95, 75], [85, 15, 5]], [[25], [95, 15], [85, 75, 5]], [[25], [95, 5], [85, 75, 15]], [[25], [85, 75], [95, 15, 5]], [[25], [85, 15], [95, 75, 5]], [[25], [85, 5], [95, 75, 15]], [[25], [75, 15], [95, 85, 5]], [[25], [75, 5], [95, 85, 15]], [[25], [15, 5], [95, 85, 75]], [[15], [5], [95, 85, 75, 25]], [[15], [95, 85], [75, 25, 5]], [[15], [95, 75], [85, 25, 5]], [[15], [95, 25], [85, 75, 5]], [[15], [95, 5], [85, 75, 25]], [[15], [85, 75], [95, 25, 5]], [[15], [85, 25], [95, 75, 5]], [[15], [85, 5], [95, 75, 25]], [[15], [75, 25], [95, 85, 5]], [[15], [75, 5], [95, 85, 25]], [[15], [25, 5], [95, 85, 75]], [[5], [95, 85], [75, 25, 15]], [[5], [95, 75], [85, 25, 15]], [[5], [95, 25], [85, 75, 15]], [[5], [95, 15], [85, 75, 25]], [[5], [85, 75], [95, 25, 15]], [[5], [85, 25], [95, 75, 15]], [[5], [85, 15], [95, 75, 25]], [[5], [75, 25], [95, 85, 15]], [[5], [75, 15], [95, 85, 25]], [[5], [25, 15], [95, 85, 75]], [[95, 85], [75, 25], [15, 5]], [[95, 85], [75, 15], [25, 5]], [[95, 85], [75, 5], [25, 15]], [[95, 75], [85, 25], [15, 5]], [[95, 75], [85, 15], [25, 5]], [[95, 75], [85, 5], [25, 15]], [[95, 25], [85, 75], [15, 5]], [[95, 25], [85, 15], [75, 5]], [[95, 25], [85, 5], [75, 15]], [[95, 15], [85, 75], [25, 5]], [[95, 15], [85, 25], [75, 5]], [[95, 15], [85, 5], [75, 25]], [[95, 5], [85, 75], [25, 15]], [[95, 5], [85, 25], [75, 15]], [[95, 5], [85, 15], [75, 25]]])
    [[95, 5], [85, 15], [75, 25]]

    >>> get_best_best_k_combination(k_combinations=[[[73], [40], [30], [20, 13, 6, 3]], [[73], [40], [20], [30, 13, 6, 3]], [[73], [40], [13], [30, 20, 6, 3]], [[73], [40], [6], [30, 20, 13, 3]], [[73], [40], [3], [30, 20, 13, 6]], [[73], [40], [30, 20], [13, 6, 3]], [[73], [40], [30, 13], [20, 6, 3]], [[73], [40], [30, 6], [20, 13, 3]], [[73], [40], [30, 3], [20, 13, 6]], [[73], [40], [20, 13], [30, 6, 3]], [[73], [40], [20, 6], [30, 13, 3]], [[73], [40], [20, 3], [30, 13, 6]], [[73], [40], [13, 6], [30, 20, 3]], [[73], [40], [13, 3], [30, 20, 6]], [[73], [40], [6, 3], [30, 20, 13]], [[73], [30], [20], [40, 13, 6, 3]], [[73], [30], [13], [40, 20, 6, 3]], [[73], [30], [6], [40, 20, 13, 3]], [[73], [30], [3], [40, 20, 13, 6]], [[73], [30], [40, 20], [13, 6, 3]], [[73], [30], [40, 13], [20, 6, 3]], [[73], [30], [40, 6], [20, 13, 3]], [[73], [30], [40, 3], [20, 13, 6]], [[73], [30], [20, 13], [40, 6, 3]], [[73], [30], [20, 6], [40, 13, 3]], [[73], [30], [20, 3], [40, 13, 6]], [[73], [30], [13, 6], [40, 20, 3]], [[73], [30], [13, 3], [40, 20, 6]], [[73], [30], [6, 3], [40, 20, 13]], [[73], [20], [13], [40, 30, 6, 3]], [[73], [20], [6], [40, 30, 13, 3]], [[73], [20], [3], [40, 30, 13, 6]], [[73], [20], [40, 30], [13, 6, 3]], [[73], [20], [40, 13], [30, 6, 3]], [[73], [20], [40, 6], [30, 13, 3]], [[73], [20], [40, 3], [30, 13, 6]], [[73], [20], [30, 13], [40, 6, 3]], [[73], [20], [30, 6], [40, 13, 3]], [[73], [20], [30, 3], [40, 13, 6]], [[73], [20], [13, 6], [40, 30, 3]], [[73], [20], [13, 3], [40, 30, 6]], [[73], [20], [6, 3], [40, 30, 13]], [[73], [13], [6], [40, 30, 20, 3]], [[73], [13], [3], [40, 30, 20, 6]], [[73], [13], [40, 30], [20, 6, 3]], [[73], [13], [40, 20], [30, 6, 3]], [[73], [13], [40, 6], [30, 20, 3]], [[73], [13], [40, 3], [30, 20, 6]], [[73], [13], [30, 20], [40, 6, 3]], [[73], [13], [30, 6], [40, 20, 3]], [[73], [13], [30, 3], [40, 20, 6]], [[73], [13], [20, 6], [40, 30, 3]], [[73], [13], [20, 3], [40, 30, 6]], [[73], [13], [6, 3], [40, 30, 20]], [[73], [6], [3], [40, 30, 20, 13]], [[73], [6], [40, 30], [20, 13, 3]], [[73], [6], [40, 20], [30, 13, 3]], [[73], [6], [40, 13], [30, 20, 3]], [[73], [6], [40, 3], [30, 20, 13]], [[73], [6], [30, 20], [40, 13, 3]], [[73], [6], [30, 13], [40, 20, 3]], [[73], [6], [30, 3], [40, 20, 13]], [[73], [6], [20, 13], [40, 30, 3]], [[73], [6], [20, 3], [40, 30, 13]], [[73], [6], [13, 3], [40, 30, 20]], [[73], [3], [40, 30], [20, 13, 6]], [[73], [3], [40, 20], [30, 13, 6]], [[73], [3], [40, 13], [30, 20, 6]], [[73], [3], [40, 6], [30, 20, 13]], [[73], [3], [30, 20], [40, 13, 6]], [[73], [3], [30, 13], [40, 20, 6]], [[73], [3], [30, 6], [40, 20, 13]], [[73], [3], [20, 13], [40, 30, 6]], [[73], [3], [20, 6], [40, 30, 13]], [[73], [3], [13, 6], [40, 30, 20]], [[73], [40, 30], [20, 13], [6, 3]], [[73], [40, 30], [20, 6], [13, 3]], [[73], [40, 30], [20, 3], [13, 6]], [[73], [40, 20], [30, 13], [6, 3]], [[73], [40, 20], [30, 6], [13, 3]], [[73], [40, 20], [30, 3], [13, 6]], [[73], [40, 13], [30, 20], [6, 3]], [[73], [40, 13], [30, 6], [20, 3]], [[73], [40, 13], [30, 3], [20, 6]], [[73], [40, 6], [30, 20], [13, 3]], [[73], [40, 6], [30, 13], [20, 3]], [[73], [40, 6], [30, 3], [20, 13]], [[73], [40, 3], [30, 20], [13, 6]], [[73], [40, 3], [30, 13], [20, 6]], [[73], [40, 3], [30, 6], [20, 13]], [[40], [30], [20], [73, 13, 6, 3]], [[40], [30], [13], [73, 20, 6, 3]], [[40], [30], [6], [73, 20, 13, 3]], [[40], [30], [3], [73, 20, 13, 6]], [[40], [30], [73, 20], [13, 6, 3]], [[40], [30], [73, 13], [20, 6, 3]], [[40], [30], [73, 6], [20, 13, 3]], [[40], [30], [73, 3], [20, 13, 6]], [[40], [30], [20, 13], [73, 6, 3]], [[40], [30], [20, 6], [73, 13, 3]], [[40], [30], [20, 3], [73, 13, 6]], [[40], [30], [13, 6], [73, 20, 3]], [[40], [30], [13, 3], [73, 20, 6]], [[40], [30], [6, 3], [73, 20, 13]], [[40], [20], [13], [73, 30, 6, 3]], [[40], [20], [6], [73, 30, 13, 3]], [[40], [20], [3], [73, 30, 13, 6]], [[40], [20], [73, 30], [13, 6, 3]], [[40], [20], [73, 13], [30, 6, 3]], [[40], [20], [73, 6], [30, 13, 3]], [[40], [20], [73, 3], [30, 13, 6]], [[40], [20], [30, 13], [73, 6, 3]], [[40], [20], [30, 6], [73, 13, 3]], [[40], [20], [30, 3], [73, 13, 6]], [[40], [20], [13, 6], [73, 30, 3]], [[40], [20], [13, 3], [73, 30, 6]], [[40], [20], [6, 3], [73, 30, 13]], [[40], [13], [6], [73, 30, 20, 3]], [[40], [13], [3], [73, 30, 20, 6]], [[40], [13], [73, 30], [20, 6, 3]], [[40], [13], [73, 20], [30, 6, 3]], [[40], [13], [73, 6], [30, 20, 3]], [[40], [13], [73, 3], [30, 20, 6]], [[40], [13], [30, 20], [73, 6, 3]], [[40], [13], [30, 6], [73, 20, 3]], [[40], [13], [30, 3], [73, 20, 6]], [[40], [13], [20, 6], [73, 30, 3]], [[40], [13], [20, 3], [73, 30, 6]], [[40], [13], [6, 3], [73, 30, 20]], [[40], [6], [3], [73, 30, 20, 13]], [[40], [6], [73, 30], [20, 13, 3]], [[40], [6], [73, 20], [30, 13, 3]], [[40], [6], [73, 13], [30, 20, 3]], [[40], [6], [73, 3], [30, 20, 13]], [[40], [6], [30, 20], [73, 13, 3]], [[40], [6], [30, 13], [73, 20, 3]], [[40], [6], [30, 3], [73, 20, 13]], [[40], [6], [20, 13], [73, 30, 3]], [[40], [6], [20, 3], [73, 30, 13]], [[40], [6], [13, 3], [73, 30, 20]], [[40], [3], [73, 30], [20, 13, 6]], [[40], [3], [73, 20], [30, 13, 6]], [[40], [3], [73, 13], [30, 20, 6]], [[40], [3], [73, 6], [30, 20, 13]], [[40], [3], [30, 20], [73, 13, 6]], [[40], [3], [30, 13], [73, 20, 6]], [[40], [3], [30, 6], [73, 20, 13]], [[40], [3], [20, 13], [73, 30, 6]], [[40], [3], [20, 6], [73, 30, 13]], [[40], [3], [13, 6], [73, 30, 20]], [[40], [73, 30], [20, 13], [6, 3]], [[40], [73, 30], [20, 6], [13, 3]], [[40], [73, 30], [20, 3], [13, 6]], [[40], [73, 20], [30, 13], [6, 3]], [[40], [73, 20], [30, 6], [13, 3]], [[40], [73, 20], [30, 3], [13, 6]], [[40], [73, 13], [30, 20], [6, 3]], [[40], [73, 13], [30, 6], [20, 3]], [[40], [73, 13], [30, 3], [20, 6]], [[40], [73, 6], [30, 20], [13, 3]], [[40], [73, 6], [30, 13], [20, 3]], [[40], [73, 6], [30, 3], [20, 13]], [[40], [73, 3], [30, 20], [13, 6]], [[40], [73, 3], [30, 13], [20, 6]], [[40], [73, 3], [30, 6], [20, 13]], [[30], [20], [13], [73, 40, 6, 3]], [[30], [20], [6], [73, 40, 13, 3]], [[30], [20], [3], [73, 40, 13, 6]], [[30], [20], [73, 40], [13, 6, 3]], [[30], [20], [73, 13], [40, 6, 3]], [[30], [20], [73, 6], [40, 13, 3]], [[30], [20], [73, 3], [40, 13, 6]], [[30], [20], [40, 13], [73, 6, 3]], [[30], [20], [40, 6], [73, 13, 3]], [[30], [20], [40, 3], [73, 13, 6]], [[30], [20], [13, 6], [73, 40, 3]], [[30], [20], [13, 3], [73, 40, 6]], [[30], [20], [6, 3], [73, 40, 13]], [[30], [13], [6], [73, 40, 20, 3]], [[30], [13], [3], [73, 40, 20, 6]], [[30], [13], [73, 40], [20, 6, 3]], [[30], [13], [73, 20], [40, 6, 3]], [[30], [13], [73, 6], [40, 20, 3]], [[30], [13], [73, 3], [40, 20, 6]], [[30], [13], [40, 20], [73, 6, 3]], [[30], [13], [40, 6], [73, 20, 3]], [[30], [13], [40, 3], [73, 20, 6]], [[30], [13], [20, 6], [73, 40, 3]], [[30], [13], [20, 3], [73, 40, 6]], [[30], [13], [6, 3], [73, 40, 20]], [[30], [6], [3], [73, 40, 20, 13]], [[30], [6], [73, 40], [20, 13, 3]], [[30], [6], [73, 20], [40, 13, 3]], [[30], [6], [73, 13], [40, 20, 3]], [[30], [6], [73, 3], [40, 20, 13]], [[30], [6], [40, 20], [73, 13, 3]], [[30], [6], [40, 13], [73, 20, 3]], [[30], [6], [40, 3], [73, 20, 13]], [[30], [6], [20, 13], [73, 40, 3]], [[30], [6], [20, 3], [73, 40, 13]], [[30], [6], [13, 3], [73, 40, 20]], [[30], [3], [73, 40], [20, 13, 6]], [[30], [3], [73, 20], [40, 13, 6]], [[30], [3], [73, 13], [40, 20, 6]], [[30], [3], [73, 6], [40, 20, 13]], [[30], [3], [40, 20], [73, 13, 6]], [[30], [3], [40, 13], [73, 20, 6]], [[30], [3], [40, 6], [73, 20, 13]], [[30], [3], [20, 13], [73, 40, 6]], [[30], [3], [20, 6], [73, 40, 13]], [[30], [3], [13, 6], [73, 40, 20]], [[30], [73, 40], [20, 13], [6, 3]], [[30], [73, 40], [20, 6], [13, 3]], [[30], [73, 40], [20, 3], [13, 6]], [[30], [73, 20], [40, 13], [6, 3]], [[30], [73, 20], [40, 6], [13, 3]], [[30], [73, 20], [40, 3], [13, 6]], [[30], [73, 13], [40, 20], [6, 3]], [[30], [73, 13], [40, 6], [20, 3]], [[30], [73, 13], [40, 3], [20, 6]], [[30], [73, 6], [40, 20], [13, 3]], [[30], [73, 6], [40, 13], [20, 3]], [[30], [73, 6], [40, 3], [20, 13]], [[30], [73, 3], [40, 20], [13, 6]], [[30], [73, 3], [40, 13], [20, 6]], [[30], [73, 3], [40, 6], [20, 13]], [[20], [13], [6], [73, 40, 30, 3]], [[20], [13], [3], [73, 40, 30, 6]], [[20], [13], [73, 40], [30, 6, 3]], [[20], [13], [73, 30], [40, 6, 3]], [[20], [13], [73, 6], [40, 30, 3]], [[20], [13], [73, 3], [40, 30, 6]], [[20], [13], [40, 30], [73, 6, 3]], [[20], [13], [40, 6], [73, 30, 3]], [[20], [13], [40, 3], [73, 30, 6]], [[20], [13], [30, 6], [73, 40, 3]], [[20], [13], [30, 3], [73, 40, 6]], [[20], [13], [6, 3], [73, 40, 30]], [[20], [6], [3], [73, 40, 30, 13]], [[20], [6], [73, 40], [30, 13, 3]], [[20], [6], [73, 30], [40, 13, 3]], [[20], [6], [73, 13], [40, 30, 3]], [[20], [6], [73, 3], [40, 30, 13]], [[20], [6], [40, 30], [73, 13, 3]], [[20], [6], [40, 13], [73, 30, 3]], [[20], [6], [40, 3], [73, 30, 13]], [[20], [6], [30, 13], [73, 40, 3]], [[20], [6], [30, 3], [73, 40, 13]], [[20], [6], [13, 3], [73, 40, 30]], [[20], [3], [73, 40], [30, 13, 6]], [[20], [3], [73, 30], [40, 13, 6]], [[20], [3], [73, 13], [40, 30, 6]], [[20], [3], [73, 6], [40, 30, 13]], [[20], [3], [40, 30], [73, 13, 6]], [[20], [3], [40, 13], [73, 30, 6]], [[20], [3], [40, 6], [73, 30, 13]], [[20], [3], [30, 13], [73, 40, 6]], [[20], [3], [30, 6], [73, 40, 13]], [[20], [3], [13, 6], [73, 40, 30]], [[20], [73, 40], [30, 13], [6, 3]], [[20], [73, 40], [30, 6], [13, 3]], [[20], [73, 40], [30, 3], [13, 6]], [[20], [73, 30], [40, 13], [6, 3]], [[20], [73, 30], [40, 6], [13, 3]], [[20], [73, 30], [40, 3], [13, 6]], [[20], [73, 13], [40, 30], [6, 3]], [[20], [73, 13], [40, 6], [30, 3]], [[20], [73, 13], [40, 3], [30, 6]], [[20], [73, 6], [40, 30], [13, 3]], [[20], [73, 6], [40, 13], [30, 3]], [[20], [73, 6], [40, 3], [30, 13]], [[20], [73, 3], [40, 30], [13, 6]], [[20], [73, 3], [40, 13], [30, 6]], [[20], [73, 3], [40, 6], [30, 13]], [[13], [6], [3], [73, 40, 30, 20]], [[13], [6], [73, 40], [30, 20, 3]], [[13], [6], [73, 30], [40, 20, 3]], [[13], [6], [73, 20], [40, 30, 3]], [[13], [6], [73, 3], [40, 30, 20]], [[13], [6], [40, 30], [73, 20, 3]], [[13], [6], [40, 20], [73, 30, 3]], [[13], [6], [40, 3], [73, 30, 20]], [[13], [6], [30, 20], [73, 40, 3]], [[13], [6], [30, 3], [73, 40, 20]], [[13], [6], [20, 3], [73, 40, 30]], [[13], [3], [73, 40], [30, 20, 6]], [[13], [3], [73, 30], [40, 20, 6]], [[13], [3], [73, 20], [40, 30, 6]], [[13], [3], [73, 6], [40, 30, 20]], [[13], [3], [40, 30], [73, 20, 6]], [[13], [3], [40, 20], [73, 30, 6]], [[13], [3], [40, 6], [73, 30, 20]], [[13], [3], [30, 20], [73, 40, 6]], [[13], [3], [30, 6], [73, 40, 20]], [[13], [3], [20, 6], [73, 40, 30]], [[13], [73, 40], [30, 20], [6, 3]], [[13], [73, 40], [30, 6], [20, 3]], [[13], [73, 40], [30, 3], [20, 6]], [[13], [73, 30], [40, 20], [6, 3]], [[13], [73, 30], [40, 6], [20, 3]], [[13], [73, 30], [40, 3], [20, 6]], [[13], [73, 20], [40, 30], [6, 3]], [[13], [73, 20], [40, 6], [30, 3]], [[13], [73, 20], [40, 3], [30, 6]], [[13], [73, 6], [40, 30], [20, 3]], [[13], [73, 6], [40, 20], [30, 3]], [[13], [73, 6], [40, 3], [30, 20]], [[13], [73, 3], [40, 30], [20, 6]], [[13], [73, 3], [40, 20], [30, 6]], [[13], [73, 3], [40, 6], [30, 20]], [[6], [3], [73, 40], [30, 20, 13]], [[6], [3], [73, 30], [40, 20, 13]], [[6], [3], [73, 20], [40, 30, 13]], [[6], [3], [73, 13], [40, 30, 20]], [[6], [3], [40, 30], [73, 20, 13]], [[6], [3], [40, 20], [73, 30, 13]], [[6], [3], [40, 13], [73, 30, 20]], [[6], [3], [30, 20], [73, 40, 13]], [[6], [3], [30, 13], [73, 40, 20]], [[6], [3], [20, 13], [73, 40, 30]], [[6], [73, 40], [30, 20], [13, 3]], [[6], [73, 40], [30, 13], [20, 3]], [[6], [73, 40], [30, 3], [20, 13]], [[6], [73, 30], [40, 20], [13, 3]], [[6], [73, 30], [40, 13], [20, 3]], [[6], [73, 30], [40, 3], [20, 13]], [[6], [73, 20], [40, 30], [13, 3]], [[6], [73, 20], [40, 13], [30, 3]], [[6], [73, 20], [40, 3], [30, 13]], [[6], [73, 13], [40, 30], [20, 3]], [[6], [73, 13], [40, 20], [30, 3]], [[6], [73, 13], [40, 3], [30, 20]], [[6], [73, 3], [40, 30], [20, 13]], [[6], [73, 3], [40, 20], [30, 13]], [[6], [73, 3], [40, 13], [30, 20]], [[3], [73, 40], [30, 20], [13, 6]], [[3], [73, 40], [30, 13], [20, 6]], [[3], [73, 40], [30, 6], [20, 13]], [[3], [73, 30], [40, 20], [13, 6]], [[3], [73, 30], [40, 13], [20, 6]], [[3], [73, 30], [40, 6], [20, 13]], [[3], [73, 20], [40, 30], [13, 6]], [[3], [73, 20], [40, 13], [30, 6]], [[3], [73, 20], [40, 6], [30, 13]], [[3], [73, 13], [40, 30], [20, 6]], [[3], [73, 13], [40, 20], [30, 6]], [[3], [73, 13], [40, 6], [30, 20]], [[3], [73, 6], [40, 30], [20, 13]], [[3], [73, 6], [40, 20], [30, 13]], [[3], [73, 6], [40, 13], [30, 20]]])
    [[73], [40], [30, 6], [20, 13, 3]]

    >>> get_best_best_k_combination(k_combinations=[[[1], [2]], [[3], [4]]])
    [[1], [2]]

    >>> get_best_best_k_combination(k_combinations=[[[9], [9]], [[2], [6]], [[2], [4]], [[1], [2]]])
    [[9], [9]]

    >>> get_best_best_k_combination(k_combinations=[[[1], [2], [3]], [[9], [9], [4, 5]], [[5], [4]], [[6], [2]]])
    [[9], [9], [4, 5]]

    """
    best_combination = []
    minimum_diff = np.inf
    flag = True
    for k_combination in k_combinations:
        diff_sum = 0
        for combinations in itertools.combinations(k_combination, 2):
            if len(combinations[0]) == 0 or len(combinations[1]) == 0:
                flag = False
                break
            else:
                flag = True
            diff_sum += abs(sum(combinations[0]) - sum(combinations[1]))
        if flag and diff_sum < minimum_diff:
            minimum_diff = diff_sum
            best_combination = k_combination
    return best_combination


def get_sum_of_max_subset(combination):
    """
    This function returns the sum of the subset with the maximum sum in a combination of subsets (list of lists)

    Author: Kfir Goldfarb
    Date: 08/06/2022
    Email: kfir.goldfarb@msmail.ariel.ac.il

    >>> get_sum_of_max_subset(combination=[[0]])
    0

    >>> get_sum_of_max_subset(combination=[[5, 6], [1, 3], [2, 20]])
    22

    >>> get_sum_of_max_subset(combination=[[20, 50], [20, 48], [60, 2]])
    70

    >>> get_sum_of_max_subset(combination=[[0, 0, 0, 1], [0, 0, 0], [0, 0, 0]])
    1

    >>> get_sum_of_max_subset(combination=[[i for i in range(10)], [i for i in range(8)]])
    45

    """
    if len(combination) == 0:
        return 0
    max_subset = combination[0]
    max_sum = 0
    for combination_set in combination:
        if sum(combination_set) > max_sum:
            max_sum = sum(combination_set)
            max_subset = combination_set
    return sum(max_subset)


def get_largest_number(combination):
    """
    This function return the largest number in all the subsets in the given combination

    Author: Kfir Goldfarb
    Date: 08/06/2022
    Email: kfir.goldfarb@msmail.ariel.ac.il

    >>> get_largest_number(combination=[[10]])
    10

    >>> get_largest_number(combination=[[5, 6], [1, 3], [2, 20]])
    20

    >>> get_largest_number(combination=[[20, 50], [20, 48], [60, 2]])
    60

    >>> get_largest_number(combination=[[0, 0, 0, 1], [0, 0, 0], [0, 0, 0]])
    1

    >>> get_largest_number(combination=[[i for i in range(10)], [i for i in range(8)]])
    9

    """
    if len(combination) == 0:
        return 0
    max_number = 0
    for combination_set in combination:
        if max(combination_set) > max_number:
            max_number = max(combination_set)
    return max_number


def all_in(sub_items: list, items) -> bool:
    """
    This function check if all the items in sub_items are contains in the given items

    Author: Kfir Goldfarb
    Date: 08/06/2022
    Email: kfir.goldfarb@msmail.ariel.ac.il

    >>> all_in(sub_items=[[1],[2],[3]], items=[1,2,3])
    True

    >>> all_in(sub_items=[[1],[2]], items=[1,2,3])
    False

    """
    copy_items = deepcopy(items)
    for items in sub_items:
        for item in items:
            copy_items.remove(item)
    return len(copy_items) == 0


def is_all_lists_are_different(list_of_lists) -> bool:
    """
    This function return True if and only if all the given subsets has different items

    Author: Kfir Goldfarb
    Date: 08/06/2022
    Email: kfir.goldfarb@msmail.ariel.ac.il

    >>> is_all_lists_are_different([[1, 2], [2, 3]])
    False

    >>> is_all_lists_are_different([[1, 2], [3, 4]])
    True

    >>> is_all_lists_are_different([[1, 2], [3, 4], [5, 6]])
    True

    >>> is_all_lists_are_different([[1, 2], [3, 4], [5, 6], [7, 8]])
    True

    >>> is_all_lists_are_different([[1, 2], [3, 4], [5, 6, 1]])
    False

    >>> is_all_lists_are_different([[1, 2, 6], [3, 4, 6], [5, 6]])
    False

    >>> is_all_lists_are_different([[1], [9, 5, 1, 2], [3, 4, 5, 7, 8, 9, 9, 9, 9, 9, 1], [2, 2, 2, 2, 9, 1, 5, 5, 5, 5]])
    False

    >>> is_all_lists_are_different([[number for number in range(3)] for _ in range(random.randint(50, 100))])
    False

    >>> is_all_lists_are_different([[number for number in range(4)] for _ in range(random.randint(50, 100))])
    False

    >>> is_all_lists_are_different([[number for number in range(5)] for _ in range(random.randint(50, 100))])
    False

    """
    flag = True
    for combinations in itertools.combinations(list_of_lists, 2):
        flag = set.isdisjoint(set(combinations[0]), set(combinations[1]))
        if not flag:
            break
    return flag


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))