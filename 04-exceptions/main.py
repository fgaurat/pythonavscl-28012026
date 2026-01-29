


def div(a,b):
    return a/b


def call_div(a,b):
    r = 0
    try:
        print("OPEN LOG")
        r = div(a,b)
    finally:
        print("CLOSE LOG")
    return r


def main():


    try:

        a = 2
        b = 2
        # c = a/b

        c = call_div(a,b)
        print(c)

    except ZeroDivisionError as e:
        print("Erreur",e)
    except TypeError as e:
        print("Erreur",e)
    except Exception as e:
        print("Erreur",e)
    else:
        print("else pas d'erreur")


    print("la fin du code")

if __name__=='__main__':
    main()
