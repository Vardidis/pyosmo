from master import *

def main():
    ts = Tokens()
    for i in ts.token_list:
        print(i)
    obj = Assets()
    print(obj.get_balance('OSMO'))


if __name__ == '__main__':
    main()