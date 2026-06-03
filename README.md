## Access Control Enforcement

This pipeline enforces role-based access control 
using both Python and PowerShell:

### How It Works
1. Developer pushes code
2. Pipeline verifies deployer is in authorized users list (PowerShell)
3. Python script enforces role-based deployment policies
4. All access decisions logged to audit trail
5. Audit logs uploaded as pipeline artifacts

### Access Roles
- developers: Can deploy to development and staging
- senior_developers: Can deploy to all environments
- viewers: Read only access

### Audit Trail
Every deployment attempt is logged with:
- Timestamp
- User identity
- Role
- Target environment  
- Access decision (GRANTED/DENIED)

See docs/provisioning_procedures.md for full SOP.
