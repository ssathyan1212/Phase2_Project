def log(message):
    with open("output/logs.txt", "a") as f:
        f.write(message + "\n")