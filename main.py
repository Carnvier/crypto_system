def triangle():
    for i in range(1, 6):
        t=0
        while t < i:
            print('*', end= '')
            t += 1
        print('')
triangle()