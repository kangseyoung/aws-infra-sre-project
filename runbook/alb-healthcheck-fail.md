# Runbook: ALB Health Check Failure

## Scenario
ALB target health shows unhealthy or the service is not reachable through the load balancer.

## Symptoms
- Target Group shows unhealthy targets
- Browser access to ALB fails
- CloudWatch alarm for unhealthy hosts triggers

## Check Order
1. Confirm the target is registered in the correct Target Group
2. Verify the health check path and port
3. Confirm EC2 security group allows traffic from ALB security group
4. Check whether Nginx is serving the expected page on the target port
5. Review ALB listener and forwarding rule

## Resolution Steps
- Fix health check path if it is wrong
- Update security group rules if ALB cannot reach EC2
- Restart Nginx container if the service is down
- Re-register target if instance association is incorrect

## Record Items
- Detection time:
- Failing target ID:
- Health check path / port:
- Root cause:
- Resolution time:

