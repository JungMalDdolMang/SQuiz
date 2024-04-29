N, K = map(int, input().split())
arr = [int(input()) for _ in range(N)]
ans = 0

p_index = 0
for i in range(N-1,-1,-1):
    if arr[i] <= K:
        p_index = i
        break

for j in range(i,-1,-1):
    if K // arr[j] != 0:
        ans += K // arr[j]
        K = K % arr[j]
        continue

print(ans)
