# Select Queries Here

# 1) user table
select_user_by_id = "SELECT * FROM user WHERE uid=?"
select_all_users = "SELECT * FROM user"
login = """SELECT u.role_id, c.first_name FROM user u INNER JOIN customer c ON u.uid = c.cid WHERE u.uid=? AND u.pswd=? 
        UNION SELECT u.role_id, e.first_name FROM user u INNER JOIN employee e ON u.uid = e.eid WHERE u.uid=? AND u.pswd=?"""
# 2) customer table
select_cust_by_id = "SELECT * FROM customer WHERE cid=?"
select_all_cust = "SELECT * FROM customer"


# 3) employee table
select_emp_by_id = "SELECT * FROM employee WHERE eid=?"
select_all_emp = "SELECT * FROM employee"


# 4) role table
select_role_by_id = "SELECT * FROM role WHERE rid=?"
select_all_role = "SELECT * FROM role"


# 5) subscription table
select_subs_by_id = "SELECT * FROM subscription WHERE sid=?"
select_all_subs = "SELECT * FROM subscription"


# 6) tarrif_plan table
select_plan_by_id = "SELECT * FROM tarrif_plan WHERE pid=?"
select_all_plan = "SELECT * FROM tarrif_plan"
select_all_plan_cid = "SELECT * FROM tarrif_plan WHERE pid NOT IN (SELECT pid FROM subscription WHERE cid = ?)"
can_delete = """SELECT CASE 
                        WHEN (julianday('now') - julianday(s.subs_date) >= 90)
                                THEN CAST(1 AS BIT)
                        ELSE CAST(0 AS BIT)
                        END
        FROM subscription s
        WHERE sid=?"""


# 7) usage table
select_usage_by_id = "SELECT * FROM usage WHERE sid=?"
select_all_usage="SELECT * FROM usage"

# 8) customer_bill table
select_bill_by_sid = "SELECT * FROM customer_bill WHERE sid=?"
select_bill_by_cid = """SELECT *
                        FROM customer_bill
                        WHERE cid=? AND sid IN (
                                        SELECT b.sid
                                        FROM customer_bill b
                                        WHERE 1 = (
                                                        CASE 
                                                                WHEN b.payment_date IS NOT NULL
                                                                        THEN (
                                                                                        CASE 
                                                                                                WHEN b.payment_date < b.last_billed
                                                                                                        THEN CAST(1 AS BIT)
                                                                                                ELSE CAST(0 AS BIT)
                                                                                                END
                                                                                        )
                                                                ELSE (
                                                                                CASE 
                                                                                        WHEN b.billing_cycle > 1
                                                                                                THEN CAST(1 AS BIT)
                                                                                        ELSE CAST(0 AS BIT)
                                                                                        END
                                                                                )
                                                                END
                                                        )
                                        )"""
total_bill_cost_for_cid = "SELECT SUM(total_cost) FROM customer_bill WHERE cid=?"
is_defaulter = """SELECT (
                                CASE 
                                        WHEN b.payment_date IS NOT NULL
                                                THEN (
                                                                CASE 
                                                                        WHEN b.payment_date < b.last_billed
                                                                                THEN CAST(1 AS BIT)
                                                                        ELSE CAST(0 AS BIT)
                                                                        END
                                                                )
                                        ELSE (
                                                        CASE 
                                                                WHEN b.billing_cycle > 1
                                                                        THEN CAST(1 AS BIT)
                                                                ELSE CAST(0 AS BIT)
                                                                END
                                                        )
                                        END
                                )
                FROM customer_bill b
                WHERE b.sid = ?"""
is_bill_present = """SELECT CASE 
                     WHEN EXISTS (
                             SELECT *
                             FROM customer_bill
                             WHERE sid = ?
                             )
                         THEN CAST(1 AS BIT)
                     ELSE CAsT(0 AS BIT)
                     END"""
select_due_amount_for_defaulter = """SELECT (IFNULL(b.total_cost, 0) + IFNULL(b.amount_due, 0))
                                     FROM customer_bill b
                                     WHERE sid = ?"""

# 9) VIEW : [subscription_by_customer] usage details - for customer
select_all_subs_details = "SELECT * FROM [subscriptions_by_customer]"
select_subs_details_by_sid = "SELECT * FROM [subscriptions_by_customer] where sid=?"
select_subs_details_by_cid = "SELECT * FROM [subscriptions_by_customer] where cid=?"

# 10) VIEW: [bill_details_per_sub]subscription details  - for operator
select_all_usage_details = "SELECT * FROM [bill_details_per_sub]"
select_usage_details_by_sid = "SELECT * FROM bill_details_per_sub where sid=?"
select_usage_details_by_cid= "SELECT * FROM bill_details_per_sub where cid=?"


