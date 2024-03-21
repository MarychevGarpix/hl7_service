from client import run_client


if __name__ == '__main__':
    try:
        run_client()
    except Exception as e:
        print(e)
        exit()

