def check_number(num):
    if num[0] == '+':
        num = num[2::]
    elif num[0] == '8':
        num = num[1::]
    elif num[0] == '7':
        num = num[1::]
    try:
        num = [int(i) for i in range(list(num))]
        if len(num) == 10 and num[0] == 9:
            return True
    except Exception:
        pass
    return False