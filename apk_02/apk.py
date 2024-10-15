# coding: utf-8

def fact(n):
    "Vrátí faktoriál čísla n"
    if n == 1:
        return 1
    else:
        return n*fact(n-1)

def matem(a, pricti=0, vynasob=1):
    'Vezme číslo a ke kterému přičte parametr pricti a vysledek vynásobí parametrem vynasob'
    return (a+pricti)*vynasob