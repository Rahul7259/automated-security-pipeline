# Access Control Policy Enforcement
# Enforces least privilege and role-based access policies

import json
import sys
from datetime import datetime

# Define access control policies
ACCESS_POLICIES = {
    "developers": {
        "can_deploy": True,
        "environments": ["development", "staging"],
        "requires_approval": False
    },
    "senior_developers": {
        "can_deploy": True,
        "environments": ["development", "staging", "production"],
        "requires_approval": True
    },
    "viewers": {
        "can_deploy": False,
        "environments": [],
        "requires_approval": False
    }
}

def check_access(user_role, target_environment):
    """
    Enforce least privilege access control
    Returns True if access is permitted, False otherwise
    """
    if user_role not in ACCESS_POLICIES:
        print(f" Unknown role: {user_role}")
        return False
    
    policy = ACCESS_POLICIES[user_role]
    
    if not policy["can_deploy"]:
        print(f" Role {user_role} is not permitted to deploy")
        return False
    
    if target_environment not in policy["environments"]:
        print(f" Role {user_role} cannot deploy to {target_environment}")
        return False
    
    print(f" Access granted: {user_role} can deploy to {target_environment}")
    return True

def log_access_decision(user, role, environment, decision):
    """
    Maintain audit trail of all access decisions
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user": user,
        "role": role,
        "environment": environment,
        "decision": "GRANTED" if decision else "DENIED",
        "policy": "least-privilege-rbac"
    }
    
    # Append to audit log
    with open("logs/access_audit.log", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    
    print(f"📝 Access decision logged: {log_entry}")

if __name__ == "__main__":
    user = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    role = sys.argv[2] if len(sys.argv) > 2 else "viewers"
    environment = sys.argv[3] if len(sys.argv) > 3 else "production"
    
    decision = check_access(role, environment)
    log_access_decision(user, role, environment, decision)
    
    sys.exit(0 if decision else 1)
