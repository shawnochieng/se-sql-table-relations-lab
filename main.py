# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

# STEP 1: Boston Employees
df_boston = pd.read_sql("""
    SELECT 
        e.firstName, 
        e.lastName, 
        e.jobTitle
    FROM employees e
    INNER JOIN offices o ON e.officeCode = o.officeCode
    WHERE o.city = 'Boston';
""", conn)

# STEP 2: Ghost Locations (Group by must list select expressions uniformly)
df_zero_emp = pd.read_sql("""
    SELECT 
        o.officeCode,
        o.city
    FROM offices o
    LEFT JOIN employees e ON o.officeCode = e.officeCode
    GROUP BY o.officeCode, o.city
    HAVING COUNT(e.employeeNumber) = 0;
""", conn)

# STEP 3: Employee Office Audit (Remove aliases so names match schema columns)
df_employee = pd.read_sql("""
    SELECT 
        e.firstName,
        e.lastName,
        o.city,
        o.state
    FROM 
        employees e
    LEFT JOIN 
        offices o ON e.officeCode = o.officeCode
    ORDER BY 
        e.firstName ASC,
        e.lastName ASC;
""", conn)

# STEP 4: Customers with No Orders (Explicit alphabetical sorting by last name)
df_no_order = pd.read_sql("""
    SELECT 
        c.contactFirstName,
        c.contactLastName,
        c.phone,
        c.salesRepEmployeeNumber
    FROM 
        customers c
    LEFT JOIN 
        orders o ON c.customerNumber = o.customerNumber
    WHERE 
        o.orderNumber IS NULL
    ORDER BY
        c.contactLastName ASC;
""", conn)

# STEP 5: Customer Payments Audit
df_payments = pd.read_sql("""
    SELECT 
        c.contactFirstName,
        c.contactLastName,
        p.amount,
        p.paymentDate
    FROM 
        customers c
    INNER JOIN 
        payments p ON c.customerNumber = p.customerNumber
    ORDER BY 
        CAST(p.amount AS REAL) DESC;
""", conn)

# STEP 6: High-Credit Sales Representatives
df_top_reps = pd.read_sql("""
    SELECT 
        e.employeeNumber,
        e.firstName,
        e.lastName,
        COUNT(c.customerNumber) AS num_customers
    FROM 
        employees e
    INNER JOIN 
        customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY 
        e.employeeNumber, e.firstName, e.lastName
    HAVING 
        AVG(c.creditLimit) > 90000
    ORDER BY 
        num_customers DESC
    LIMIT 4;
""", conn)

# STEP 7: Top Selling Products
df_top_products = pd.read_sql("""
    SELECT 
        p.productName,
        COUNT(d.orderNumber) AS numorders,
        SUM(d.quantityOrdered) AS totalunits
    FROM 
        products p
    INNER JOIN 
        orderdetails d ON p.productCode = d.productCode
    GROUP BY 
        p.productCode, p.productName
    ORDER BY 
        totalunits DESC;
""", conn)

# STEP 8: Market Reach (Unique Purchasers per Product)
df_market_reach = pd.read_sql("""
    SELECT 
        p.productName,
        p.productCode,
        COUNT(DISTINCT o.customerNumber) AS numpurchasers
    FROM 
        products p
    INNER JOIN 
        orderdetails d ON p.productCode = d.productCode
    INNER JOIN 
        orders o ON d.orderNumber = o.orderNumber
    GROUP BY 
        p.productCode, p.productName
    ORDER BY 
        numpurchasers DESC;
""", conn)

# STEP 9: Customer Density per Office
df_office_customers = pd.read_sql("""
    SELECT 
        COUNT(c.customerNumber) AS n_customers,
        o.officeCode,
        o.city
    FROM 
        offices o
    INNER JOIN 
        employees e ON o.officeCode = e.officeCode
    INNER JOIN 
        customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY 
        o.officeCode, o.city;
""", conn)

# STEP 10: Underperforming Products Subquery
df_low_performers = pd.read_sql("""
    SELECT DISTINCT
        e.employeeNumber,
        e.firstName,
        e.lastName,
        o.city,
        o.officeCode
    FROM 
        employees e
    INNER JOIN 
        offices o ON e.officeCode = o.officeCode
    INNER JOIN 
        customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    INNER JOIN 
        orders ord ON c.customerNumber = ord.customerNumber
    INNER JOIN 
        orderdetails d ON ord.orderNumber = d.orderNumber
    WHERE 
        d.productCode IN (
            SELECT 
                sub_d.productCode
            FROM 
                orderdetails sub_d
            INNER JOIN 
                orders sub_ord ON sub_d.orderNumber = sub_ord.orderNumber
            GROUP BY 
                sub_d.productCode
            HAVING 
                COUNT(DISTINCT sub_ord.customerNumber) < 20
        );
""", conn)

conn.close()
