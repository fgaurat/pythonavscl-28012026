from CustomerDAO import CustomerDAO



def filterMale(stream):

    for elem in stream:
        if elem.gender == "Male":
            yield elem
    
def main():
    
    dao = CustomerDAO("customers.db")
    customers = dao.findAll()
    # customers = list(customers)

    # print(customers)
    # c1 = next(customers)
    # c2 = next(customers)

    l =[]
    for customer in filterMale(customers):
        l.append(customer)



if __name__=='__main__':
    main()
