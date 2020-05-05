from typing import List


def task_1_add_new_record_to_db(con) -> None:
    """
    Add a record for a new customer from Singapore
    {
        'customer_name': 'Thomas',
        'contactname': 'David',
        'address': 'Some Address',
        'city': 'London',
        'postalcode': '774',
        'country': 'Singapore',
    }

    Args:
        con: psycopg connection

    Returns: 92 records

    """
    try:
        cur = con.cursor()
        Query = "INSERT INTO Customers(CustomerName,ContactName,Address,City,PostalCode,Country) VALUES (%s, %s, %s, %s, %s,%s);"
        cur.execute(Query, ('Thomas', 'David', 'Some Address', 'London', '774', 'Singapore'))
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)


def task_2_list_all_customers(cur) -> list:
    """
    Get all records from table Customers

    Args:
        cur: psycopg cursor

    Returns: 91 records

    """
    L = []
    try:
        Query = "SELECT * FROM Customers;"
        cur.execute (Query)
        customer_records = cur.fetchall()
        for i in customer_records:
            L.append(i)
        return L
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)


def task_3_list_customers_in_germany(cur) -> list:
    """
    List the customers in Germany

    Args:
        cur: psycopg cursor

    Returns: 11 records
    """
    L = []
    try:
        Query = "SELECT * FROM Customers where Country = 'Germany'"
        cur.execute (Query)
        customer_records = cur.fetchall()
        for i in customer_records:
            L.append(i)
        return L
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)


def task_4_update_customer(con):
    """
    Update first customer's name (Set customername equal to  'Johnny Depp')
    Args:
        cur: psycopg cursor

    Returns: 91 records with updated customer

    """
    try:
        cur = con.cursor()
        Query = "UPDATE customers SET customername = %s WHERE customerid = %s"
        cur.execute(Query, ("Johnny Depp", 1))
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)


def task_5_delete_the_last_customer(con) -> None:
    """
    Delete the last customer

    Args:
        con: psycopg connection
    """
    try:
        cur = con.cursor()
        Query = "DELETE FROM customers WHERE customerid=(SELECT MAX(customerid) from customers)"
        cur.execute(Query, ())
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)


def task_6_list_all_supplier_countries(cur) -> list:
    """
    List all supplier countries

    Args:
        cur: psycopg cursor

    Returns: 29 records

    """
    L = []
    try:
        Query = "SELECT country FROM suppliers"
        cur.execute(Query)
        supplier_records = cur.fetchall()
        for i in supplier_records:
            L.append(i)
        return L
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)


def task_7_list_supplier_countries_in_desc_order(cur) -> list:
    """
    List all supplier countries in descending order

    Args:
        cur: psycopg cursor

    Returns: 29 records in descending order

    """
    L = []
    try:
        Query = "SELECT country FROM suppliers ORDER BY country desc"
        cur.execute(Query)
        supplier_records = cur.fetchall()
        for i in supplier_records:
            L.append(i)
        return L
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)


def task_8_count_customers_by_city(cur):
    """
    List the number of customers in each city

    Args:
        cur: psycopg cursor

    Returns: 69 records in descending order

    """
    L = []
    try:
        Query = "select city,count(city) from (select * from customers order by customername) " \
                "as nested group by city order by count(*) desc,city asc"
        cur.execute(Query)
        customers_city_records = cur.fetchall()
        for i in customers_city_records:
            L.append(i)
        return L
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)


def task_9_count_customers_by_country_with_than_10_customers(cur):
    """
    List the number of customers in each country. Only include countries with more than 10 customers.

    Args:
        cur: psycopg cursor

    Returns: 3 records
    """
    L = []
    try:
        Query = "select count(country),country from customers group by country having count(country)>10"
        cur.execute(Query)
        country_records = cur.fetchall()
        for i in country_records:
            L.append(i)
        return L
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)


def task_10_list_first_10_customers(cur):
    """
    List first 10 customers from the table

    Results: 10 records
    """
    L = []
    try:
        Query = "select * from customers limit 10"
        cur.execute(Query)
        customers_records = cur.fetchall()
        for i in customers_records:
            L.append(i)
        return L
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)


def task_11_list_customers_starting_from_11th(cur):
    """
    List all customers starting from 11th record

    Args:
        cur: psycopg cursor

    Returns: 11 records
    """
    L = []
    try:
        Query = "select * from customers offset 11"
        cur.execute(Query)
        customers_records = cur.fetchall()
        for i in customers_records:
            L.append(i)
        return L
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)


def task_12_list_suppliers_from_specified_countries(cur):
    """
    List all suppliers from the USA, UK, OR Japan

    Args:
        cur: psycopg cursor

    Returns: 8 records
    """
    L = []
    try:
        Query = "select supplierid,suppliername,contactname,city,country from suppliers " \
                "where (country=%s) or (country=%s) or (country=%s);"
        cur.execute(Query, ('USA', 'UK', 'Japan'))
        suppliers_records = cur.fetchall()
        for i in suppliers_records:
            L.append(i)
        return L
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)


def task_13_list_products_from_sweden_suppliers(cur):
    """
    List products with suppliers from Sweden.

    Args:
        cur: psycopg cursor

    Returns: 3 records
    """
    L = []
    try:
        Query = "select productname from products where supplierid=(select supplierid from suppliers where country=%s)"
        cur.execute(Query, ('Sweden',))
        suppliers_records = cur.fetchall()
        for i in suppliers_records:
            L.append(i)
        return L
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)


def task_14_list_products_with_supplier_information(cur):
    """
    List all products with supplier information

    Args:
        cur: psycopg cursor

    Returns: 77 records
    """
    L = []
    try:
        Query = "select productid,productname,unit,price,suppliers.country,suppliers.city,suppliers.suppliername " \
                "from products inner join suppliers on products.supplierid=suppliers.supplierid"
        cur.execute(Query, ())
        suppliers_records = cur.fetchall()
        for i in suppliers_records:
            L.append(i)
        return L
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)


def task_15_list_customers_with_any_order_or_not(cur):
    """
    List all customers, whether they placed any order or not.

    Args:
        cur: psycopg cursor

    Returns: 213 records
    """
    L = []
    try:
        Query = "select customername,contactname,country,orders.orderid " \
                "from customers inner join orders on orders.customerid=customers.customerid"
        cur.execute(Query, ())
        suppliers_records = cur.fetchall()
        for i in suppliers_records:
            L.append(i)
        return L
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)


def task_16_match_all_customers_and_suppliers_by_country(cur):
    """
    Match all customers and suppliers by country

    Args:
        cur: psycopg cursor

    Returns: 194 records
    """
    L = []
    try:
        Query = "select customername,customers.address,customers.country AS customercountry,suppliers.country " \
                "AS suppliercountry,suppliers.suppliername from customers full outer join suppliers " \
                "on customers.country=suppliers.country order by customercountry,suppliercountry"
        cur.execute(Query, ())
        suppliers_records = cur.fetchall()
        for i in suppliers_records:
            L.append(i)
        return L
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
