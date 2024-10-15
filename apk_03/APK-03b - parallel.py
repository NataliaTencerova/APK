# -*- coding: utf-8 -*-

# Import modulu datetime pro stopování času
import datetime as dt

# Funkce pro počítání prvočísel
def je_prvocislo(num):
    '''Vrati True, pokud num je prvocislo'''
    for i in range(2, int(num**0.5)+1):
        if num % i == 0:
            return False
    return True

def pocet_prvocisel(od, do):
    '''Vrati pocet prvocisel v intervalu <od, do)'''
    pocet = 0
    for num in range(od, do):
        if je_prvocislo(num):
            pocet += 1
    #print od,do, '-', pocet
    return pocet


from joblib import Parallel, delayed
paralelni_pocet = delayed(pocet_prvocisel)


from multiprocessing import Pool
def pocet_prvocisel2(argument):
    od, do = argument
    return pocet_prvocisel(od, do)


if __name__ == '__main__':

    # Vstupní data
    data = [(0, 1000), (1000, 10000), (10000, 100000), (100000, 1000000), (1000000, 3000000)]

    # Prostý výpočet
    print('\nProstý výpočet')
    t0 = dt.datetime.now()
    prvocisla = [pocet_prvocisel(od, do) for od, do in data]
    print ('pocet prvocisel', sum(prvocisla))
    t1 = dt.datetime.now()
    print ('cas', t1-t0)

    # Příklad pomocí knihovny joblib https://pypi.python.org/pypi/joblib
    print('\njoblib')
    t0 = dt.datetime.now()
    prvocisla = Parallel(n_jobs=4)(paralelni_pocet(od, do) for od, do in data)
    print ('pocet prvocisel', sum(prvocisla))
    t1 = dt.datetime.now()
    print( 'cas', t1-t0)

    # Výpočet pomocí multiprocessing.Pool https://docs.python.org/2/library/multiprocessing.html
    print('\nmultiprocessing')
    t0 = dt.datetime.now()
    p = Pool(4)
    prvocisla = p.map(pocet_prvocisel2, data)
    print( 'pocet prvocisel', sum(prvocisla))
    t1 = dt.datetime.now()
    print( 'cas', t1-t0)

