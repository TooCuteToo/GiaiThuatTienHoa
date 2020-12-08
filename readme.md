###THUẬT TOÁN DI TRUYỀN (GENETIC ALGORITHM)

---

####<ins>Chú thích</ins>:

- Passcode: [1, 4, 2, 3, 5, 8, 9].
- Chromosome: Mật khẩu hoặc những mật khẩu thử.
- Gene: Mỗi số trong passcode.

- Population: Tập hợp của các mật khẩu thử.

  - Population I: được tạo random từ các Chromosome.

  - Population tiếp theo: được tạo ra từ sự luật tiến hóa.

- Generation: Mỗi lần lặp lại của một quần thể mới.

- Fitness: Thang đánh giá.

- Parents: Những Chromosome có Fitness cao trong Population hiện tại.

- Crossover: Quá trình giao phối giữa Parents.

- Children: Kết quả của quá trình giao phối.

  - Những cá thể Children này sẽ định hình Population mới cho thế hệ tiếp theo.

- Elitism: Qúa trình đưa số lượng nhỏ Parents có điểm Fitness cao sang thế hệ tiếp theo.

- Mutation: Chọn ngẫu nhiên Gene và thay đổi sang một cái mới. - Chỉ có 10% Children bị thay đổi.

---

####<ins>CÀI ĐẶT</ins>:

- Python 3.9.0
- Visual studio code
- Thư viện sử dụng:

  ```python
  import random
  import numpy as np
  import matplotlib.pyplot as plt
  import time
  import matplotlib.animation as animation
  ```

####<ins>CODE</ins>:

- Các biến cần thiết cho thuật toán:

```python
# passcode length
passcode_length = 8

# min number
passcode_lower_bound = 0

# max number
passcode_upper_bound = 9

# the number chromosomes that will be in the population
population_size = 10

# number of parents selected from the population each iteration
num_parents = 5

# number of the population that will be kept as is
elite_size = 2
```

- Khởi tạo password bằng thuật toán ngẫu nhiên:

```python
# create secret password
secret_passcode = []
for x in range(passcode_length):
    secret_passcode.append(
        int(round(random.uniform(passcode_lower_bound, passcode_upper_bound), 0)))

print(secret_passcode)
```

- Khởi tạo quần thể đầu tiên:

```python
population = []
for i in range(population_size):
    chromosome = []
    for x in range(passcode_length):
        chromosome.append(
            int(round(random.uniform(passcode_lower_bound, passcode_upper_bound), 0)))
    population.append(chromosome)
```

- Hàm thực thi thuật toán GA:

```python
success = []
fitness_tracker = []
generations = 0
t0 = time.time()
while True:

    fitness_scores = fitness(population)
    fitness_tracker.append(max([i[1] for i in fitness_scores]))
    success.append([i[0] for i in fitness_scores if i[1] == max(
        [i[1] for i in fitness_scores])][0])
    if max([i[1] for i in fitness_scores]) == passcode_length:
        print("Cracked in {} generations, and {} seconds! \nSecret passcode = {} \nDiscovered passcode = {}".format(
            generations, time.time() - t0, secret_passcode, [i[0] for i in fitness_scores if i[1] == passcode_length][0]))
        break
    parents = select_parents(fitness_scores)
    children = create_children(parents)
    population = mutation(children)
    generations += 1
```

- Trực quan hóa điểm đánh giá của từng thế hệ:

```python
fig = plt.figure()
plt.plot(list(range(generations+1)), fitness_tracker)
fig.suptitle('Fitness Score by Generation', fontsize=14, fontweight='bold')
ax = fig.add_subplot(111)
ax.set_xlabel('Generation')
ax.set_ylabel('Fitness Score')
plt.show()
```

- Thực hiện mô phỏng quá trình thuật toán chạy:

```python
x = list(range(len(success)))
y = list(range(len(success)))


def update_line(num, data, line):
    line.set_data(data[..., :num])
    solution_text.set_text(success[num])
    secret_passcode_str = "".join(map(str, secret_passcode))
    generation_text.set_text(
        "Passcode: {} -- Generation: {}" .format(secret_passcode_str, num))
    return line


fig, ax = plt.subplots(figsize=(12, 6))
data = np.array([x, y])

ax.set_facecolor("black")
fig.patch.set_facecolor('black')
l, = plt.plot([], [], 'r-', color="black")
ax.set_xlim(0, 7000)
ax.set_ylim(0, 200)
ax.set_yticklabels([])
ax.set_xticklabels([])
ax.tick_params(axis=u'both', which=u'both', length=0)
solution_text = ax.text(3500, 100, "", fontsize=30, color="white",
                        horizontalalignment='center', verticalalignment='center')
generation_text = ax.text(100, 170, "", fontsize=20, color="white")
line_ani = animation.FuncAnimation(fig, update_line, len(
    success) + 1, fargs=(data, l), interval=20, repeat_delay=400)
plt.show()
```
