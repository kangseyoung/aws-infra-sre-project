# Runbook: Cost Cleanup

## Scenario
The project is ending or unused resources need to be removed to avoid ongoing AWS charges.

## Symptoms
- Resources remain running after the project
- Billing estimate is higher than expected
- Team is unsure what can be deleted safely

## Check Order
1. Review EC2 instances
2. Review ALB and Target Groups
3. Review EBS volumes and snapshots
4. Review Elastic IP addresses
5. Review NAT Gateway
6. Review CloudWatch log groups and alarms

## Cleanup Steps
- Stop or terminate EC2 instances that are no longer needed
- Delete ALB and Target Groups
- Delete unattached EBS volumes and unnecessary snapshots
- Release unused Elastic IP addresses
- Delete NAT Gateway if created for this project
- Remove unused CloudWatch resources

## Record Items
- Cleanup date:
- Checked by:
- Deleted resources:
- Remaining resources:
- Final billing check note:

