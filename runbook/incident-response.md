# Incident Response Template - ALB to MiniPEP

## Incident Summary
- Incident title:
- Date / time detected:
- Severity:
- Reporter:
- Owner:

## Situation
- What happened:
- User impact:
- Affected component:

## Symptoms
- ALB DNS 접속 실패:
- `http://ALB-DNS/health` 응답 코드:
- Target Group health 상태:
- EC2 내부 `curl -i http://localhost/health` 결과:
- Docker / MiniPEP log 증상:

## Triage Order
1. Confirm current impact and scope
2. Check ALB DNS, Listener, and forwarding rule
3. Check Target Group registration and Target Health
4. Check EC2 instance state and status checks
5. Check Security Groups
   - ALB SG: inbound HTTP 80 from external users
   - EC2 SG: inbound HTTP 80 only from ALB SG
   - EC2 SG: inbound SSH 22 only from operator My IP
6. Check port and health check contract
   - ALB Listener: HTTP 80
   - Target Group: HTTP 80
   - EC2 host: HTTP 80
   - Docker container: 8000
   - Health Check Path: `/health`
   - Success Code: `200`
7. Check Docker and MiniPEP application status
8. Run EC2 internal checks
   - `curl -i http://localhost/health`
   - `curl http://localhost/api/equipment`
   - `curl http://localhost/api/jobs`
9. Review Docker stdout and MiniPEP Application Log
10. Check CloudWatch basic metrics and Target Health
11. Review recent changes

## Investigation Notes
- Timeline:
- Metrics observed:
- Logs observed:
- Configuration changes:

## Resolution
- Immediate mitigation:
- Permanent fix:

## Recovery Verification
- [ ] ALB DNS is reachable
- [ ] `http://ALB-DNS/health` returns HTTP 200
- [ ] Target Group is Healthy
- [ ] EC2 internal `/health` returns HTTP 200
- [ ] Docker container is running
- [ ] MiniPEP dashboard or API responds
- [ ] Monitoring stable
- [ ] Team informed

## Record Items
- Root cause:
- Start time:
- End time:
- Total duration:
- Follow-up tasks:
