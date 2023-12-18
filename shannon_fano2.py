
from common import *

# Driver code
if __name__ == '__main__':
    total = 0

    alphabet = [(' ', 0.34963325183374083),
                (',', 0.029339853300733496),
                ('.', 0.019559902200488997),
                ('А', 0.16136919315403422),
                ('Г', 0.019559902200488997),
                ('Л', 0.05623471882640587),
                ('Ж', 0.007334963325183374),
                ('Е', 0.10513447432762836),
                ('У', 0.044009779951100246),
                ('М', 0.10268948655256724),
                ('Ц', 0.007334963325183374),
                ('Р', 0.097799511002445)]
    p = []
    for symbol, probability in alphabet:
        n = node()
        n.pro = probability
        n.sym = symbol
        n.top = -1
        p.append(n)
    n = len(p)
    sortByProbability(n, p)

    # Find the shannon code
    shannon(0, n - 1, p)

    # Display the codes
    display(n, p)
