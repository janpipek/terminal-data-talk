for high in range(16):
    print("  ", end="")
    for low in range(16):
        colour = low + high * 16
        print(f"\033[48;5;{colour}m {colour:3} \033[0m", end="")
    print()
