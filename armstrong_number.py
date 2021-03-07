print("Armstrong numbers in three-digit are as follows:")
for num in range(100, 1000):
    cube_sum = 0
    arm_num = num
    while num > 0:
        digit = num % 10
        cube_sum += digit ** 3
        num //= 10
    if cube_sum == arm_num:
        print(arm_num)
