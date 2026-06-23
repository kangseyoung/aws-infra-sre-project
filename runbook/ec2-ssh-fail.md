# Runbook: EC2 SSH Failure

## Scenario
SSH access to the EC2 instance does not work.

## Symptoms
- SSH timeout
- Connection refused
- Permission denied

## Check Order
1. Confirm EC2 instance is running
2. Confirm public IP or access path is correct
3. Verify security group inbound rule for port 22
4. Confirm the correct key pair is being used
5. Check route table and subnet internet reachability

## Resolution Steps
- Correct the SSH command and username
- Fix security group rules for SSH access
- Confirm the `.pem` file permissions and correct key pair
- Reboot instance only if needed after basic checks

## Record Items
- Detection time:
- Instance ID:
- SSH source IP:
- Root cause:
- Resolution time:

