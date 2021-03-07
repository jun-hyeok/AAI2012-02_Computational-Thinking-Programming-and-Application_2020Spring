""" 제곱수 출력 : 0부터 시작하여 입력한 수 만큼의 제곱수를 한 줄 씩 반환 """
# 숫자 입력
num = int(input("Enter an integer: "))

"""(optional/replace) 숫자 입력에 제한 및 입력 반복
# 입력 조건 미 충족시 입력 반복
while True:
    # 숫자 입력
    num = int(input("Enter an integer: "))
    # 입력한 숫자가 음이 아닌 정수(non-negative integer)가 아닐 경우
    if num < 0:
        # 경고문 출력
        print(f"{num} is not non-negative. Try agin")
        # 반복문 계속
        continue
    # 입력한 숫자가 음이 아닌 정수(non-negative integer)인 경우
    else:
        # 반복문 통과
        break
"""
# 제곱수 출력 (0², 1², ..., {num}²)
# range(num) = [0, 1, ..., num]
for i in range(num):
    print(i ** 2)

"""(optional) 동일한 제곱수 출력 코드
i = 0
while i < num:
    print(i ** 2)
    i = i + 1
"""
