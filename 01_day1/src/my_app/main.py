# src/my_app/main.py
def helper():
    print("[helper] running helper logic")

def main():
    print("[main] start")
    helper()
    print("[main] end")

if __name__ == "__main__":
    print("[__name__ guard] file executed directly")
    main()
