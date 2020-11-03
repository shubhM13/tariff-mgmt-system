# 1) User table
insert_user = "INSERT INTO user VALUES (?,?,?,?)"
update_user_by_id = "UPDATE user SET pswd=?, datetime=?, role_id=? WHERE uid=?"
delete_user_by_id = "DELETE FROM user WHERE uid=?"


# 2) Customer table
insert_cust = "INSERT INTO customer VALUES (?,?,?,?,?,?,?,?,?)"
update_cust_by_id = "UPDATE customer SET first_name=?,last_name=?,address=?,city=?,state=?,pincode=?,email=?,contact=? WHERE cid=?"
delete_cust_by_id = "DELETE FROM customer WHERE cid=?"


# 3) Employee table
insert_emp = "INSERT INTO employee VALUES (?,?,?,?,?,?)"
update_emp_by_id = "UPDATE employee SET first_name=?,last_name=?,role_id=?,email=?,contact=? WHERE eid=?"
delete_emp_by_id = "DELETE FROM employee WHERE eid=?"


# 4) Role table
insert_role = "INSERT INTO role VALUES (?,?)"
delete_role_by_id = "DELETE FROM role WHERE rid=?"


# 5) Subscription table
insert_subs = "INSERT INTO subscription VALUES (?,?,?,?,?)"
update_subs_by_id = "UPDATE subscription SET cid=?, pid=?, subs_date=?, last_billed=? WHERE sid=?"
update_last_billed_date = "UPDATE subscription SET last_billed=? WHERE sid=?"
delete_subs_by_id = "DELETE FROM subscription WHERE sid=?"



# 6) Tarrif_Plan table
insert_plan = "INSERT INTO tarrif_plan VALUES (?,?,?,?,?,?)"
update_plan_by_id = "UPDATE tarrif_plan SET name=?,tarrif_call=?,tarrif_data=?,validity=?,rental=? WHERE pid=?"
delete_plan_by_id = "DELETE FROM tarrif_plan WHERE pid=?"


# 7) Usage table
insert_usage = "INSERT INTO usage VALUES (?,?,?,?)"
update_usage_by_id = "UPDATE usage SET voice=?,data=?,datetime=? WHERE sid=?"
delete_usage_by_id = "DELETE FROM usage WHERE sid=?"

# 8) Bill table
insert_bill_by_sid = "INSERT INTO customer_bill VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
update_bill_by_sid = """UPDATE customer_bill
                          SET cid = ?
                              ,pid = ?
                              ,name = ?
                              ,tarrif_call = ?
                              ,tarrif_data = ?
                              ,validity = ?
                              ,rental = ?
                              ,subs_date = ?
                              ,last_billed = ?
                              ,voice_usage = ?
                              ,data_usage = ?
                              ,call_cost = ?
                              ,data_cost = ?
                              ,total_cost = ?
                              ,billing_cycle = ?
                          WHERE sid = ?"""
delete_bill_by_sid = "DELETE FROM customer_bill WHERE sid=?"
