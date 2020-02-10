from random import randrange, shuffle
# Function takes width and height arguments, 10x10 for 100 rooms


def make_maze(w=10, h=10):
    # Visited
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    # Vertical
    ver = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
    # Horizontal
    hor = [["+--"] * w + ['+'] for _ in range(h + 1)]
    # Traverse through grid and mark cells

    def walk(x, y):
        vis[y][x] = 1
        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]:
                continue
            if xx == x:
                hor[max(y, yy)][x] = "+  "
            if yy == y:
                ver[y][max(x, xx)] = "   "
            walk(xx, yy)
    walk(randrange(w), randrange(h))
    s = ""
    for (a, b) in zip(hor, ver):
        s += ''.join(a + ['\n'] + b + ['\n'])
    return s


# Print random maze in terminal
if __name__ == '__main__':
    print(make_maze())
