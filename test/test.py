import time
import random

choices = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
vals = [0]*36

g = ""

# start_time = time.time_ns()
# for i in range(36):
#     g+=str(random.choice(choices))
# time.sleep(1)
# print(time.time_ns()-start_time)

repetitions = 5

iterations = 100

t_v = []

for i in range(repetitions):
    print("Running")
    s = 0
    for i in range(iterations):
        start_time = time.time_ns()
        time.sleep(1)
        s += time.time_ns()-start_time
    t_v.append(s/iterations)

print(t_v)
print(t_v-1)
print(sum(t_v)/len(t_v))
print(sum(t_v)/len(t_v)-1)
# print(g)