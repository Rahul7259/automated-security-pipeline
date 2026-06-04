# Access Control Provisioning Procedures

## Overview
This document defines the standard procedures for 
provisioning access to the DevSecOps pipeline,
following least privilege and RBAC principles.

## Access Roles

| Role | Permissions | Environments |
|------|------------|--------------|
| developers | Deploy | Development, Staging |
| senior_developers | Deploy + Approve | All environments |
| viewers | Read only | None |

## Provisioning Process

### Adding a New Developer
1. Submit access request via GitHub Issues
2. Manager approves request
3. Senior developer adds user to authorized_users.txt
4. Pull request created and reviewed
5. Access granted after PR merged
6. Access logged in audit trail

### Revoking Access (Leaver Process)
1. HR notifies team of departure
2. User immediately removed from authorized_users.txt
3. Pull request created and merged
4. Access revocation logged in audit trail
5. Historical audit logs preserved per retention policy

### Access Review Schedule
- Monthly review of authorized_users.txt
- Quarterly entitlement report generated
- Annual full access audit performed

## Audit Trail
All access decisions are logged to logs/access_audit.log
Format: timestamp, user, role, environment, decision
Retention: 12 months minimum
