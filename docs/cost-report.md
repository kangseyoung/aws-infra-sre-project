# Cost Management and Cleanup Template

## Cost Tracking Summary
- Project period:
- AWS account / environment:
- Owner:
- Last updated:

## Daily Resource Review
| Date | Resource Type | Resource Name / ID | Purpose | Still Needed? | Notes |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## Estimated Cost Watchlist
Pay extra attention to:

- Application Load Balancer
- NAT Gateway
- EC2 running hours
- EBS volumes and snapshots
- Elastic IP
- CloudWatch log retention

## Budget / Alert Notes
- Billing alarm configured:
- Alert threshold:
- Notification channel:
- Owner:

## Cleanup Checklist
- [ ] Stop or terminate unused EC2 instances
- [ ] Delete unused ALB and Target Groups
- [ ] Delete unused EBS volumes and snapshots
- [ ] Release unused Elastic IP addresses
- [ ] Delete NAT Gateway if no longer needed
- [ ] Review Security Groups that are no longer attached
- [ ] Review CloudWatch log groups and retention settings
- [ ] Remove test resources created during practice

## Final Deletion Verification
| Item | Checked By | Date | Notes |
| --- | --- | --- | --- |
| EC2 |  |  |  |
| ALB |  |  |  |
| Target Group |  |  |  |
| EBS |  |  |  |
| Elastic IP |  |  |  |
| NAT Gateway |  |  |  |
| CloudWatch |  |  |  |

## Lessons Learned
- Which resource created the most unexpected cost?
- Which daily review habit was most useful?
- What should be automated or checked earlier next time?

