import sys
from bisect import bisect_left

def main():
    data = sys.stdin.read().strip().split()
    it = iter(data)
    N = int(next(it))

    # fesztiválok: (start, end, revenue, original_id)
    festivals = []
    for i in range(N):
        s = int(next(it)); e = int(next(it)); w = int(next(it))
        festivals.append((s, e, w, i + 1))  # eredeti index 1-alapú

    # 1) Rendezés zárónap (end) szerint növekvőbe
    festivals.sort(key=lambda t: (t[1], t[0]))

    # 2) Külön tömbök a könnyebb kezeléshez
    starts = [f[0] for f in festivals]
    ends   = [f[1] for f in festivals]
    W      = [f[2] for f in festivals]
    IDs    = [f[3] for f in festivals]

    # 3) p(i): legnagyobb j < i, ahol ends[j] < starts[i]
    # bisect_left(ends, starts[i]) -> első index, ahol ends[idx] >= starts[i]
    # így p(i) = pos - 1
    p = [-1] * N
    for i in range(N):
        pos = bisect_left(ends, starts[i], 0, i)  # csak a korábbiakat nézzük
        p[i] = pos - 1  # lehet -1 is, ha nincs kompatibilis előd

    # 4) DP: dp[i] = max bevétel az első i+1 (0..i) fesztiválból
    dp = [0] * N
    take = [False] * N

    for i in range(N):
        use  = W[i] + (dp[p[i]] if p[i] != -1 else 0)
        skip = dp[i-1] if i > 0 else 0
        if use >= skip:
            dp[i] = use
            take[i] = True
        else:
            dp[i] = skip
            take[i] = False

    # 5) Visszafejtés: mely fesztiválokat vettük
    chosen = []
    i = N - 1
    while i >= 0:
        if take[i]:
            chosen.append(IDs[i])
            i = p[i]  # ugorjunk a kompatibilis elődre
        else:
            i -= 1

    # A feladat szerint a sorrend tetszőleges; ha szeretnéd, megfordíthatod:
    # chosen.reverse()

    # 6) Kiírás
    max_revenue = dp[N-1] if N > 0 else 0
    print(max_revenue)
    print(len(chosen), *chosen)

if __name__ == "__main__":
    main()
