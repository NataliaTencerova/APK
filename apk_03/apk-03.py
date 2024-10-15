# -*- coding: utf-8 -*-

import datetime as dt
import multiprocessing

def simple_sieve(limit):
    '''Generate all prime numbers up to the limit using the sieve of Eratosthenes'''
    is_prime = [True] * (limit + 1)
    is_prime[0:2] = [False, False]  # 0 and 1 are not prime
    for i in range(2, int(limit ** 0.5) + 1):
        if is_prime[i]:
            is_prime[i * i:limit + 1:i] = [False] * len(range(i * i, limit + 1, i))
    primes = [i for i, prime in enumerate(is_prime) if prime]
    return primes

def segmented_sieve_count(args):
    '''Count the number of primes in a given interval using the segmented sieve algorithm'''
    low, high, primes = args
    size = high - low
    is_prime = [True] * size

    for p in primes:
        # Find the minimum number in [low, high) that is a multiple of p
        start = max(p * p, ((low + p - 1) // p) * p)
        for multiple in range(start, high, p):
            is_prime[multiple - low] = False

    # Adjust for low values less than 2
    count = sum(1 for i in range(size) if is_prime[i] and (low + i) >= 2)
    return count

if __name__ == '__main__':

    # Optimized input data intervals with smaller ranges
    data = [
        (0, 1000),
        (1000, 5000),
        (5000, 10000),
        (10000, 50000),
        (50000, 100000),
        (100000, 500000),
        (500000, 1000000)
    ]

    # Determine the maximum value to set the limit for the sieve
    max_do = max(do for _, do in data)
    limit = int(max_do ** 0.5) + 1

    # Generate small primes up to sqrt(max_do) for use in the segmented sieve
    t0 = dt.datetime.now()
    small_primes = simple_sieve(limit)
    t1 = dt.datetime.now()
    print('Time to generate small primes:', t1 - t0)

    # Determine the number of available CPU cores for optimal thread usage
    num_processes = multiprocessing.cpu_count()
    print(f'Using {num_processes} processes')

    # Prepare arguments for the multiprocessing pool
    pool_args = [(od, do, small_primes) for od, do in data]

    # Count primes in intervals using multiprocessing and the segmented sieve
    t0 = dt.datetime.now()
    with multiprocessing.Pool(num_processes) as pool:
        results = pool.map(segmented_sieve_count, pool_args)
    t1 = dt.datetime.now()
    print('Time to count primes in intervals:', t1 - t0)

    # Sum the results from all intervals
    total_primes = sum(results)
    print('Number of primes:', total_primes)
