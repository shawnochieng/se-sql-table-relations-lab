# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
df_boston = pd.read_sql("""
    SELECT 
        employees.firstName, 
        employees.lastName, 
        employees.jobTitle
    FROM 
        employees
    INNER JOIN 
        offices ON employees.officeCode = offices.officeCode
    WHERE 
        offices.city = 'Boston';
""", conn)

# STEP 2
df_zero_emp = pd.read_sql("""
    SELECT 
        offices.officeCode,
        offices.city
    FROM 
        offices
    LEFT JOIN 
        employees ON offices.officeCode = employees.officeCode
    GROUP BY 
        offices.officeCode
    HAVING 
        COUNT(employees.employeeNumber) = 0;
""", conn)

# STEP 3
df_employee = pd.read_sql("""
    SELECT 
        employees.firstName,
        employees.lastName,
        offices.city,
        offices.state
    FROM 
        employees
    LEFT JOIN 
        offices ON employees.officeCode = offices.officeCode
    ORDER BY 
        employees.firstName ASC,
        employees.lastName ASC;
""", conn)

# STEP 4
df_no_order = pd.read_sql("""
    SELECT 
        customers.contactFirstName,
        customers.contactLastName,
        customers.phone,
        customers.salesRepEmployeeNumber
    FROM 
        customers
    LEFT JOIN 
        orders ON customers.customerNumber = orders.customerNumber
    WHERE 
        orders.orderNumber IS NULL
    ORDER BY 
        customers.contactLastName ASC;
""", conn)

# STEP 5
df_payments = pd.read_sql("""
    SELECT 
        customers.contactFirstName,
        customers.contactLastName,
        payments.amount,
        payments.paymentDate
    FROM 
        customers
    INNER JOIN 
        payments ON customers.customerNumber = payments.customerNumber
    ORDER BY 
        CAST(payments.amount AS REAL) DESC;
""", conn)

# STEP 6
df_top_reps = pd.read_sql("""
    SELECT 
        employees.employeeNumber,
        employees.firstName,
        employees.lastName,
        COUNT(customers.customerNumber) AS num_customers
    FROM 
        employees
    INNER JOIN 
        customers ON employees.employeeNumber = customers.salesRepEmployeeNumber
    GROUP BY 
        employees.employeeNumber
    HAVING 
        AVG(customers.creditLimit) > 90000
    ORDER BY 
        num_customers DESC
    LIMIT 4;
""", conn)

# STEP 7
df_top_products = pd.read_sql("""
    SELECT 
        products.productName,
        COUNT(orderdetails.orderNumber) AS numorders,
        SUM(orderdetails.quantityOrdered) AS totalunits
    FROM 
        products
    INNER JOIN 
        orderdetails ON products.productCode = orderdetails.productCode
    GROUP BY 
        products.productCode
    ORDER BY 
        totalunits DESC;
""", conn)

# STEP 8
df_market_reach = pd.read_sql("""
    SELECT 
        products.productName,
        products.productCode,
        COUNT(DISTINCT orders.customerNumber) AS numpurchasers
    FROM 
        products
    INNER JOIN 
        orderdetails ON products.productCode = orderdetails.productCode
    INNER JOIN 
        orders ON orderdetails.orderNumber = orders.orderNumber
    GROUP BY 
        products.productCode
    ORDER BY 
        numpurchasers DESC;
""", conn)

# STEP 9
df_office_customers = pd.read_sql("""
    SELECT 
        COUNT(customers.customerNumber) AS n_customers,
        offices.officeCode,
        offices.city
    FROM 
        offices
    INNER JOIN 
        employees ON offices.officeCode = employees.officeCode
    INNER JOIN 
        customers ON employees.employeeNumber = customers.salesRepEmployeeNumber
    GROUP BY 
        offices.officeCode;
""", conn)

# STEP 10
df_low_performers = pd.read_sql("""
    SELECT DISTINCT
        employees.employeeNumber,
        employees.firstName,
        employees.lastName,
        offices.city,
        offices.officeCode
    FROM 
        employees
    INNER JOIN 
        offices ON employees.officeCode = offices.officeCode
    INNER JOIN 
        customers ON employees.employeeNumber = customers.salesRepEmployeeNumber
    INNER JOIN 
        orders ON customers.customerNumber = orders.customerNumber
    INNER JOIN 
        orderdetails ON orders.orderNumber = orderdetails.orderNumber
    WHERE 
        orderdetails.productCode IN (
            SELECT 
                orderdetails.productCode
            FROM 
                orderdetails
            INNER JOIN 
                orders ON orderdetails.orderNumber = orders.orderNumber
            GROUP BY 
                orderdetails.productCode
            HAVING 
                COUNT(DISTINCT orders.customerNumber) < 20
        );
""", conn)

conn.close()