/*
File: RLS-and-DynamicDataMasking.sql
Description: This script sets up role-based security and dynamic data masking for a specific table in the database.
Author: Achraf Cherki
Date: 27-08-2024

Roles:
- ADMIN: Has access to all fields in the table, with all fields masked except identifiers.
- ROLE1: Has access to all fields in the table, with no masking applied.
- ROLE1_MASKED: Has access to all sensitive fields in the table, with all sensitive fields masked except the code field.

Security Groups:
- AD_ADMIN: Active Directory group for ADMIN role.
- AD_ROLE1: Active Directory group for ROLE1 role.
- AD_ROLE1_MASKED: Active Directory group for ROLE1_MASKED role.

Schema:
- Security: Schema to hold the security functions and policies.

Security Functions:
- Security.fin_securitypredicate_role1(): Returns a table with a single column (securitypredicate_result) that is used as a filter predicate for ROLE_MASKED security policy. It checks if the current user is a member of ROLE1_MASKED role.

Security Policies:
- ROLE_MASKED: A security policy applied to the specified table. It uses the fin_securitypredicate_role1() function as a filter predicate to restrict access to ROLE1_MASKED role.

Dynamic Data Masking:
- The COL1 and COL2 columns in the specified table are altered to add default masking functions.

Permissions:
- The UNMASK permission is granted to ROLE1 on the specified table.

Note: Replace <tablename> with the actual table name in the script.
*/
-- Reference to roles needed 

--ADMIN				ALL			MASKED - All fields masked except identifiers
--ROLE1		    	ALL			No
--ROLE1_MASKED	    ALL			MASKED - All sensitive fields masked (Except code)

-- CREATE ROLES

CREATE ROLE [ADMIN];
CREATE ROLE [ROLE1];
CREATE ROLE [ROLE1_MASKED];

GO
-- ADD Entra ID Groups
-- Assuming security groups are named as follows  AD_ADMIN , AD_ROLE1 ... 

ALTER ROLE [ADMIN] ADD MEMBER [AD_ADMIN];
ALTER ROLE [ROLE1] ADD MEMBER [AD_ROLE1];
ALTER ROLE [ROLE1_MASKED] ADD MEMBER [AD_ROLE1_MASKED];
GO

-- CREATE Schema to hold RLS settings
CREATE Schema Security;
GO

-- CREATE SECURITY FUNCTIONS
-- This security function can be adjusted by filtering using the value of a field, for example to limit only to a team

CREATE FUNCTION Security.fin_securitypredicate_role1()
    RETURNS TABLE
WITH SCHEMABINDING
AS
    RETURN SELECT 1 AS securitypredicate_result
WHERE
(IS_MEMBER('ROLE1_MASKED') = 1 );
GO

-- CREATE FUNCTION Security.fin_securitypredicate_team1(@team AS varchar(10))
--     RETURNS TABLE
-- WITH SCHEMABINDING
-- AS
--     RETURN SELECT 1 AS securitypredicate_result
-- WHERE
-- (IS_MEMBER('ROLE_TEAM1_MASKED') = 1 AND TRIM(@team) = 'TEAM1');
-- GO

-- CREATE FUNCTION Security.fin_securitypredicate_(@team AS varchar(10))
CREATE SECURITY POLICY ROLE_MASKED
ADD FILTER PREDICATE Security.fin_securitypredicate_role1()
ON [dbo].[<tablename>]
-- ,ADD FILTER PREDICATE Security.fin_securitypredicate_team1(TEAM)
-- ON [dbo].[<tablename>],
WITH (STATE = ON, SCHEMABINDING=ON);
GO


-- DYNAMIC DATA MASKING 

ALTER TABLE [dbo].[<tablename>] ALTER COLUMN [COL1] ADD MASKED WITH (FUNCTION = 'default()');
ALTER TABLE [dbo].[<tablename>] ALTER COLUMN [COL2] ADD MASKED WITH (FUNCTION = 'default()');
GO

-- Grant UNMASK

GRANT UNMASK ON [dbo].[<tablename>] TO [ROLE1];
GO


-- Column Level Security
 
-- CREATE Demo table
-- CREATE TABLE [dbo].[<tablename>] (
--     [ID] INT IDENTITY(1,1) PRIMARY KEY,
--     [COL1] NVARCHAR(50),
--     [COL2] NVARCHAR(50),
--     [COL3] NVARCHAR(50),
--     [COL4] NVARCHAR(50),
--     [COL5] NVARCHAR(50),
--     [COL6] NVARCHAR(50),
--     [COL7] NVARCHAR(50),
--     [COL8] NVARCHAR(50),
--     [COL9] NVARCHAR(50),
--     [COL10] NVARCHAR(50)
-- );

GRANT SELECT ON [dbo].[<tablename>](COL1, COL2, COL2) TO [ROLE1];