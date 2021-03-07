## This is (yearly) compound interest calculator
# Set target deposit.
TARGET = 20000000

# Receives annual interest rate as a percentage from the user.
annual_interest_rate = int(input("Enter an annual interest rate(%): "))

# receive the user's deposit from the user.
deposit = int(input("Enter your deposit: "))

# 'yrs' means the time it takes for the 'deposit' to reach the 'TARGET'.
yrs = 0  # Initialize 'yrs' to zero

# Iterate the loop until 'deposit' reaches 'TARGET'
while deposit < TARGET:
    # Interest calculated on compound interest is added to the deposit.
    # In the compound interest formula A = P(1+r)ⁿ, the power n is 'yrs',
    # so it can be interpreted as multiplying (1 + r) by the deposit that is updated for each loop.
    # P is initial deposit, A is updated deposit and r is annual interest rate in digit.
    deposit *= 1 + annual_interest_rate / 100
    # 'yrs' is n, ie the number of loop iterations.
    yrs += 1

# Result
print(f"It takes {yrs} years")
