
import numpy as np
def getTrack(distance):
    print('independent getTrack')
    a1 = .25 + np.random.random()*.25
    a2 = .5 + np.random.random()*.25
    a3 = 1 - a1 - a2
    print(a1, a2, a3, sum([a1, a2, a3]))
    n1 = np.random.randint(5, 10)
    n2 = np.random.randint(10, 15)
    n3 = np.random.randint(4, 8)
    alpha = np.linspace(-np.pi/2, np.pi/2, n1)
    beta = np.linspace(-np.pi/2, np.pi/2, n2)
    gama= np.linspace(-np.pi/2, np.pi/2, n3)
    y1 = np.round(np.cos(alpha), 3)
    y2 = np.round(np.cos(beta), 3)
    y3 = np.round(np.cos(gama), 3)
    print(y1, y2, y3, sep='\n')
    print('*-'*30)
    y1 = np.round(a1 * y1 / np.sum(y1), 3)
    y2 = np.round(a2 * y2 / np.sum(y2), 3)
    y3 = np.round(a3 * y3 / np.sum(y3), 3)
    print(y1, y2, y3, sep='\n')
    print('*='*30)
    y = np.hstack([y1, y2, y3])
    print(np.sum(y))
    y = np.round(y * distance, 3)
    return y

if __name__ == '__main__':
    distance = 50
    track = getTrack(distance)
    print(np.sum(track), '; length = ', len(track))
    print(track)
    







