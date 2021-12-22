from itertools import islice
import math
import time
from typing import Iterator, List, Optional, Set
import multiprocessing as mp
from sympy import isprime
import logging
from primify import console

logger = logging.getLogger(__file__)


class NextPrimeFinder:
    def __init__(self, value: int, n_workers: int = 1):
        self.value = int(value)
        self.n_workers = n_workers
        self.expected_n_primality_tests = max(10, int(math.log(value)))

    def prime_candidates(self) -> Iterator[int]:
        candidate = self.value
        while True:
            if candidate % 6 in [1, 5]:
                yield candidate
            candidate += 1

    @staticmethod
    def is_prime_worker(candidate: int, found_prime) -> Optional[int]:
        if not found_prime.is_set():
            if isprime(candidate):
                logger.info(f"{candidate} is prime!")
                found_prime.set()
                return candidate

        logger.debug(
            f"Checking of {candidate} skipped since we already found the next prime"
        )
        return

    def find_next_prime(self) -> int:

        with mp.Pool(self.n_workers) as pool:
            manager = mp.Manager()
            found_prime = manager.Event()
            candidate_iter = (
                (candidate, found_prime) for candidate in self.prime_candidates()
            )

            results: Set[Optional[int]] = set()
            search_start = time.time()
            while not found_prime.is_set():
                console.log(
                    f"Performing batch of ~{self.expected_n_primality_tests} primality tests. We rarely need more than one batch.",
                )
                result = pool.starmap(
                    NextPrimeFinder.is_prime_worker,
                    islice(candidate_iter, self.expected_n_primality_tests),
                )

                results |= set(result)

            console.log(
                f"Got one! Next prime was found within {int(time.time()- search_start) + 1}s"
            )
            pool.terminate()

            for result in results:
                # all but the prime are None
                if result is not None:
                    return result
        return -1
