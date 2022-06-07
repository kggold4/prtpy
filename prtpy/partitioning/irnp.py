"""
    Partition the numbers using the improved recursive number partitioning algorithm
    Taken help from:

    Taken from the "A Hybrid Recursive Multi-Way Number Partitioning Algorithm (2011)" Paper
    By Richard E. Korf,
    Algorithm number in Paper: 3.0
    Paper link:
        http://citeseerx.ist.psu.edu/viewdoc/download?rep=rep1&type=pdf&doi=10.1.1.208.2132
    Author: Kfir Goldfarb
    Date: 26/04/2022
    Email: kfir.goldfarb@msmail.ariel.ac.il
"""
import copy
import threading
import time
from typing import Callable, List
from prtpy import Bins
from prtpy.bins import BinsKeepingContents
from prtpy.partitioning.ckk import ckk
from prtpy.partitioning.rnp import rnp
from prtpy.utils import base_check_bins, max_largest, get_best_partition


def irnp(bins: Bins, items: List[any], valueof: Callable = lambda x: x, with_threads: bool = False):
    """
    Partition the numbers using the improved recursive number partitioning algorithm

    """
    k = bins.num
    bins, flag = base_check_bins(bins=bins, items=items, valueof=valueof)
    if flag:
        return bins
    items.sort(reverse=True, key=valueof)
    max_largest_bins = max_largest(bins=copy.deepcopy(bins), items=items, valueof=valueof)

    if with_threads:

        rnp_bins = copy.deepcopy(bins)
        t1 = threading.Thread(target=rnp, args=[rnp_bins, items, valueof])

        ckk_bins = copy.deepcopy(bins)
        t2 = threading.Thread(target=ckk, args=[ckk_bins, items, valueof])

        start1 = time.time()
        t1.start()

        start2 = time.time()
        t2.start()

        t1.join()
        end1 = time.time()

        t2.join()
        end2 = time.time()

        print(f"time for thread1: {end1 - start1}")
        print(f"time for thread2: {end2 - start2}")
        print(f"total time: {end2 - start1}")

        perfect_solution = get_best_partition([max_largest_bins, rnp_bins, ckk_bins], k)
        return perfect_solution, end1 - start1, end2 - start2, end2 - start1

    else:
        start1 = time.time()
        rnp_bins = rnp(bins=copy.deepcopy(bins), items=items, valueof=valueof)
        ckk_bins = ckk(bins=copy.deepcopy(bins), items=items, valueof=valueof)
        end1 = time.time()
        print(f"total time: {end1 - start1}")
        perfect_solution = get_best_partition([max_largest_bins, rnp_bins, ckk_bins], k)
        return perfect_solution, end1 - start1


if __name__ == "__main__":
    irnp(BinsKeepingContents(5), items=[i for i in range(1, 8)], with_threads=True)
