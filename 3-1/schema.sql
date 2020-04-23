create database JNTUH;
use JNTUH;
CREATE TABLE results_31 (
    rollno varchar(10) PRIMARY KEY,
    name varchar(40) NOT NULL,
    `13508` ENUM ('O','A+','A','B+','B','C','F') NOT NULL,
    `13510` ENUM ('O','A+','A','B+','B','C','F') NOT NULL,
    `13534` ENUM ('O','A+','A','B+','B','C','F') NOT NULL,
    `13537` ENUM ('O','A+','A','B+','B','C','F') NOT NULL,
    `135AE` ENUM ('O','A+','A','B+','B','C','F') NOT NULL,
    `135AF` ENUM ('O','A+','A','B+','B','C','F') NOT NULL,
    `135AR` ENUM ('O','A+','A','B+','B','C','F') NOT NULL,
    `135BM` ENUM ('O','A+','A','B+','B','C','F') NOT NULL,
    `135CX` ENUM ('O','A+','A','B+','B','C','F') NOT NULL,
    grade varchar(4) default NULL
 );