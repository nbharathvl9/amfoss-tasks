def destination(n, t_t):
    min_time = min(t_t)
    count_min_time = t_t.count(min_time)
    if count_min_time == 1:
        return t_t.index(min_time) + 1
    else:
        return "Still Aetheria"
n = int(input())
t_t = list(map(int, input().split()))
destination = destination(n, t_t)
print(destination)
