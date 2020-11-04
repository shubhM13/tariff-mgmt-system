CREATE TABLE user (
	uid VARCHAR(5) NOT NULL
	,pswd VARCHAR(45) NOT NULL
	,DATETIME DATETIME NOT NULL
	,role_id INTEGER NOT NULL
	,PRIMARY KEY (uid)
	);

CREATE TABLE customer (
	cid VARCHAR(5) NOT NULL
	,first_name VARCHAR(25) NOT NULL
	,last_name VARCHAR(25) NOT NULL
	,address TEXT NOT NULL
	,city VARCHAR(50) NOT NULL
	,STATE VARCHAR(50) NOT NULL
	,pincode INTEGER NOT NULL
	,email VARCHAR(50) NOT NULL
	,contact VARCHAR(10) NOT NULL
	,PRIMARY KEY (cid)
	);

CREATE TABLE tarrif_plan (
	pid VARCHAR(5) NOT NULL
	,name VARCHAR(50) NOT NULL
	,tarrif_call REAL NOT NULL
	,tarrif_data REAL NOT NULL
	,validity INTEGER NOT NULL
	,rental REAL
	,PRIMARY KEY (pid)
	);

CREATE TABLE subscription (
	sid VARCHAR(10) NOT NULL
	,cid VARCHAR(5) NOT NULL
	,pid VARCHAR(5) NOT NULL
	,subs_date DATETIME NOT NULL
	,last_billed DATETIME NOT NULL
	,PRIMARY KEY (sid)
	);

CREATE TABLE usage (
	sid VARCHAR(10) NOT NULL
	,voice INTEGER NOT NULL
	,data INTEGER NOT NULL
	,DATETIME DATETIME NOT NULL
	);

CREATE TABLE employee (
	eid VARCHAR(5) NOT NULL
	,first_name VARCHAR(25) NOT NULL
	,last_name VARCHAR(25) NOT NULL
	,role_id INTEGER NOT NULL
	,email VARCHAR(50) NOT NULL
	,contact VARCHAR(10) NOT NULL
	,PRIMARY KEY (eid)
	);

CREATE TABLE ROLE (
	rid INTEGER NOT NULL
	,ROLE VARCHAR(50) NOT NULL
	,PRIMARY KEY (rid)
	);

CREATE VIEW IF NOT EXISTS [subscriptions_by_customer]
AS
SELECT s.sid AS sid
	,s.subs_date AS subscribed_on
	,s.cid AS cid
	,p.pid AS pid
	,p.name AS name
	,p.tarrif_call AS tarrif_call
	,p.tarrif_data AS tarrif_data
	,p.validity AS validity
	,p.rental AS rental
FROM subscription s
INNER JOIN tarrif_plan p ON s.pid = p.pid
WHERE s.cid IN (
		SELECT cid
		FROM customer
		);

CREATE VIEW 
IF NOT EXISTS [aggregate_usage_current_billing_cycle]
AS
SELECT DISTINCT u.sid AS sid
	,SUM(u.voice) AS voice_usage
	,SUM(u.data) AS data_usage
FROM usage u
INNER JOIN subscription s ON u.sid = s.sid
WHERE u.datetime BETWEEN strftime('%Y-%m-%d', s.last_billed)
		AND strftime('%Y-%m-%d', DATE (
					'now'
					,'localtime'
					))
GROUP BY u.sid;

CREATE VIEW
IF NOT EXISTS [bill_details_per_sub] AS
	SELECT c.sid AS sid
		,c.cid AS cid
		,c.pid AS pid
		,c.name AS name
		,c.tarrif_call AS tarrif_call
		,c.tarrif_data AS tarrif_data
		,c.validity AS validity
		,c.rental AS rental
		,s.subs_date AS subscribed_on
		,s.last_billed AS last_billed
		,a.voice_usage AS voice_usage
		,a.data_usage AS data_usage
		,((voice_usage * tarrif_call) / 100) AS call_cost
		,((data_usage * tarrif_data) / 100) AS data_cost
		,((voice_usage * tarrif_call) / 100 + (data_usage * tarrif_data) / 100 + rental) AS total_cost
		,(
			CASE 
				WHEN (
						strftime('%Y', DATE (
								'now'
								,'localtime'
								)) = strftime('%Y', s.subs_date)
						)
					THEN (
							CASE 
								WHEN (
										strftime('%m', DATE (
												'now'
												,'localtime'
												)) = strftime('%m', s.subs_date)
										)
									THEN 1
								ELSE (
										CASE 
											WHEN (
													(strftime('%d', s.subs_date)) > (
														strftime('%d', DATE (
																'now'
																,'localtime'
																))
														)
													)
												THEN (
														strftime('%m', DATE (
																'now'
																,'localtime'
																)) - strftime('%m', s.subs_date)
														)
											ELSE (
													strftime('%m', DATE (
															'now'
															,'localtime'
															)) - strftime('%m', s.subs_date) + 1
													)
											END
										)
								END
							)
				ELSE (
						CASE 
							WHEN (
									(strftime('%d', s.subs_date)) > (
										strftime('%d', DATE (
												'now'
												,'localtime'
												))
										)
									)
								THEN (
										(
											(
												strftime('%m', DATE (
														'now'
														,'localtime'
														)) - strftime('%m', s.subs_date)
												) % 12
											) + (
											strftime('%Y', DATE (
													'now'
													,'localtime'
													)) - strftime('%Y', s.subs_date) - 1
											) * 12
										)
							ELSE (
									(
										(
											strftime('%m', DATE (
													'now'
													,'localtime'
													)) - strftime('%m', s.subs_date) + 1
											) % 12
										) + (
										strftime('%Y', DATE (
												'now'
												,'localtime'
												)) - strftime('%Y', s.subs_date) - 1
										) * 12
									)
							END
						)
				END
			) AS billing_cycle
		,(
			CASE 
				WHEN (
						(
							strftime('%d', s.subs_date) <= strftime('%d', DATE (
									'now'
									,'localtime'
									))
							)
						AND (
							(
								strftime('%m', DATE (
										'now'
										,'localtime'
										)) - strftime('%m', s.last_billed)
								) >= 1
							)
						)
					THEN (CAST(1 AS BIT))
				ELSE (CAST(0 AS BIT))
				END
			) AS not_billed
	FROM subscription s
	INNER JOIN [subscriptions_by_customer] c ON s.sid = c.sid
	INNER JOIN [aggregate_usage_current_billing_cycle] a ON c.sid = a.sid

CREATE TABLE customer_bill (
	sid VARCHAR(10) NOT NULL
	,cid VARCHAR(5) NOT NULL
	,pid VARCHAR(5) NOT NULL
	,name VARCHAR(50) NOT NULL
	,tarrif_call REAL NOT NULL
	,tarrif_data REAL NOT NULL
	,validity INTEGER NOT NULL
	,rental REAL
	,subs_date DATETIME NOT NULL
	,last_billed DATETIME NOT NULL
	,voice_usage INTEGER NOT NULL
	,data_usage INTEGER NOT NULL
	,call_cost REAL NOT NULL
	,data_cost REAL NOT NULL
	,total_cost REAL NOT NULL
	,billing_cycle INTEGER NOT NULL
	,payment_date DATETIME
	,amount_due REAL
	,PRIMARY KEY (sid)
	);