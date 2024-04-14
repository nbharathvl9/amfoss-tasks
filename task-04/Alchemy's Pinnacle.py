t = int(input())  # Number of test cases

for _ in range(t):
    num1_str, num2_str = input().split()
    num1_list = list(num1_str)
    num2_list = list(num2_str)
    num1_len, num2_len = len(num1_list), len(num2_list)

    # Pad the shorter number with zeros at the front to make them of the same length
    if num1_len > num2_len:
        num2_list = ['0'] * (num1_len - num2_len) + num2_list
    elif num2_len > num1_len:
        num1_list = ['0'] * (num2_len - num1_len) + num1_list

    # Scan for the first difference and adjust all subsequent digits
    b_flag, b_index = False, 0
    for i in range(len(num1_list)):
        if num1_list[i] != num2_list[i]:
            b_flag = True
            b_index = i
            break

    if b_flag:
        # Adjust numbers from the first difference point
        for i in range(b_index + 1, len(num1_list)):
            num1_list[i] = '9'  # Maximize num1
            num2_list[i] = '0'  # Minimize num2

    updated_num1_str = "".join(num1_list)
    updated_num2_str = "".join(num2_list)
    updated_num1 = int(updated_num1_str)
    updated_num2 = int(updated_num2_str)

    # Calculate sum of digit-wise absolute differences
    s = 0
    while updated_num1 > 0 or updated_num2 > 0:
        rem1 = updated_num1 % 10
        rem2 = updated_num2 % 10
        s += abs(rem1 - rem2)
        updated_num1 //= 10
        updated_num2 //= 10

    print(s)

