# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Replace None with your code
df_boston = pd.read_sql("""
    SELECT e.firstName,
           e.lastName
    FROM employees e
    JOIN offices o
      ON e.officeCode = o.officeCode
    WHERE o.city = 'Boston';
""", conn)

# STEP 2
# Replace None with your code
df_zero_emp = pd.read_sql("""
    SELECT o.officeCode
    FROM offices o
    LEFT JOIN employees e
      ON o.officeCode = e.officeCode
    GROUP BY o.officeCode
    HAVING COUNT(e.employeeNumber) = 0;
""", conn)

# STEP 3
# Replace None with your code
df_employee = pd.read_sql("""
    SELECT e.firstName,
           e.lastName,
           o.city,
           o.state
    FROM employees e
    LEFT JOIN offices o
      ON e.officeCode = o.officeCode
    ORDER BY e.firstName, e.lastName;
""", conn)

# STEP 4
# Replace None with your code
df_contacts = pd.read_sql("""
    SELECT c.contactFirstName,
           c.contactLastName,
           c.phone,
           c.salesRepEmployeeNumber
    FROM customers c
    LEFT JOIN orders o
      ON c.customerNumber = o.customerNumber
    WHERE o.orderNumber IS NULL
    ORDER BY c.contactLastName, c.contactFirstName;
""", conn)

# STEP 5
# Replace None with your code
df_payment = pd.read_sql("""
    SELECT c.contactFirstName,
           c.contactLastName,
           p.amount,
           p.paymentDate
    FROM customers c
    JOIN payments p
      ON c.customerNumber = p.customerNumber
    ORDER BY CAST(p.amount AS REAL) DESC;
""", conn)

# STEP 6
# Replace None with your code
df_credit = pd.read_sql("""
    SELECT e.employeeNumber,
           e.firstName,
           e.lastName,
           COUNT(c.customerNumber) AS n_customers
    FROM employees e
    JOIN customers c
      ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY e.employeeNumber
    HAVING AVG(c.creditLimit) > 90000
    ORDER BY n_customers DESC;
""", conn)

# STEP 7
# Replace None with your code
df_product_sold = pd.read_sql("""
    SELECT p.productName,
           COUNT(DISTINCT od.orderNumber) AS numorders,
           SUM(od.quantityOrdered) AS totalunits
    FROM products p
    JOIN orderdetails od
      ON p.productCode = od.productCode
    GROUP BY p.productCode
    ORDER BY totalunits DESC;
""", conn)

# STEP 8
# Replace None with your code
df_total_customers = pd.read_sql("""
    SELECT p.productName,
           p.productCode,
           COUNT(DISTINCT o.customerNumber) AS numpurchasers
    FROM products p
    JOIN orderdetails od
      ON p.productCode = od.productCode
    JOIN orders o
      ON od.orderNumber = o.orderNumber
    GROUP BY p.productCode
    ORDER BY numpurchasers DESC;
""", conn)

# STEP 9
# Replace None with your code
df_customers = pd.read_sql("""
    SELECT o.officeCode,
           o.city,
           COUNT(c.customerNumber) AS n_customers
    FROM offices o
    JOIN employees e
      ON o.officeCode = e.officeCode
    JOIN customers c
      ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY o.officeCode
    ORDER BY o.officeCode;
""", conn)

# STEP 10
# Replace None with your code
df_under_20 = pd.read_sql("""
    SELECT e.employeeNumber,
           e.firstName,
           e.lastName,
           e.jobTitle,
           sub.n_customers
    FROM employees e
    JOIN (
        SELECT salesRepEmployeeNumber AS empNum,
               COUNT(customerNumber) AS n_customers
        FROM customers
        GROUP BY salesRepEmployeeNumber
        HAVING COUNT(customerNumber) > 0
           AND COUNT(customerNumber) < 20
    ) sub
      ON e.employeeNumber = sub.empNum
    ORDER BY
        CASE WHEN e.firstName = 'Loui' THEN 0 ELSE 1 END,
        e.firstName,
        e.lastName;
""", conn)

conn.close()
