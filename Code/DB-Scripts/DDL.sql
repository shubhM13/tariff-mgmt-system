CREATE TABLE login ( 
	uid VARCHAR(5) NOT NULL,
	pswd VARCHAR(45) NOT NULL,
	datetime DATETIME NOT NULL,
	role INTEGER NOT NULL,
	PRIMARY KEY (uid) );
	
CREATE TABLE customer (
	cid VARCHAR(5) NOT NULL, 
	first_name VARCHAR(25) NOT NULL,
	last_name VARCHAR(25) NOT NULL, 
	address TEXT NOT NULL, 
	city VARCHAR(50) NOT NULL,
	state VARCHAR(50) NOT NULL, 
	pincode INTEGER NOT NULL, 
	email VARCHAR(50) NOT NULL, 
	contact VARCHAR(10) NOT NULL, 
	PRIMARY KEY (cid) 
	);
	
CREATE TABLE tarrif_plan (
	pid VARCHAR(5) NOT NULL,
	name VARCHAR(50) NOT NULL,
	type INTEGER NOT NULL CHECK(type IN(0,1)),
	tarrif REAL NOT NULL,
	validity INTEGER NOT NULL,
	rental REAL,
	PRIMARY KEY (pid)
	);
	
CREATE TABLE subscription (
	sid VARCHAR(10) NOT NULL,
	cid VARCHAR(5) NOT NULL,
	pid VARCHAR(5) NOT NULL,
	PRIMARY KEY(sid)
	);

CREATE TABLE usage (
	sid VARCHAR(10) NOT NULL,
	utilization INTEGER NOT NULL,
	datetime DATETIME NOT NULL
	);

CREATE TABLE employee (
	eid VARCHAR(5) NOT NULL, 
	first_name VARCHAR(25) NOT NULL,
	last_name VARCHAR(25) NOT NULL, 
	department VARCHAR(50) NOT NULL, 
	designation VARCHAR(50) NOT NULL ,
	email VARCHAR(50) NOT NULL, 
	contact VARCHAR(10) NOT NULL,
	PRIMARY KEY (eid) 
	);

CREATE TABLE roles(
	rid INTEGER NOT NULL,
	role VARCHAR(50) NOT NULL,
	PRIMARY KEY(rid)
	);