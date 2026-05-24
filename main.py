# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Select first and last names and job titles of employees who work in the Boston office
df_boston = pd.read_sql("""
    SELECT e.firstName,
           e.lastName,
           e.jobTitle
    FROM employees e
    JOIN offices o
      ON e.officeCode = o.officeCode
    WHERE o.city = 'Boston';
""", conn)

# STEP 2
# Find offices that have zero employees (if any)
df_zero_emp = pd.read_sql("""
    SELECT o.officeCode
    FROM offices o
    LEFT JOIN employees e
      ON o.officeCode = e.officeCode
    GROUP BY o.officeCode
    HAVING COUNT(e.employeeNumber) = 0;
""", conn)

# STEP 3
# Select employees with their office city and state (if available), sorted by first and last name
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
# Select contact info for customers who have not placed any orders
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
# List customer contacts with their payment amounts and dates, sorted by payment amount descending
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
# Find employees whose customers have an average credit limit greater than 90000 (Alias must be num_customers)
df_credit = pd.read_sql("""
    SELECT e.employeeNumber,
           e.firstName,
           e.lastName,
           COUNT(c.customerNumber) AS num_customers
    FROM employees e
    JOIN customers c
      ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY e.employeeNumber
    HAVING AVG(c.creditLimit) > 90000
    ORDER BY num_customers DESC;
""", conn)

# STEP 7
# Show how many orders and total units were sold for each product
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
# Show how many distinct customers purchased each product
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
# Count how many customers belong to each office
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
# Find employees who sold products ordered by fewer than 20 unique customers using a subquery on productCode
df_under_20 = pd.read_sql("""
    SELECT DISTINCT e.employeeNumber,
           e.firstName,
           e.lastName,
           o.city,
           o.officeCode
    FROM employees e
    JOIN offices o ON e.officeCode = o.officeCode
    JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    JOIN orders ord ON c.customerNumber = ord.customerNumber
    JOIN orderdetails od ON ord.orderNumber = od.orderNumber
    WHERE od.productCode IN (
        SELECT sub_od.productCode
        FROM orderdetails sub_od
        JOIN orders sub_o ON sub_od.orderNumber = sub_o.orderNumber
        GROUP BY sub_od.productCode
        HAVING COUNT(DISTINCT sub_o.customerNumber) < 20
    );
""", conn)

conn.close()
