# 2026-07-03 공부기록 - 권태욱

## 1. 담당 파트

Observability / Platform / IaC 보조 / Compute 보조

## 2. 오늘 공부한 개념

오늘은 Observability의 세부 구성 요소인 Metric, Log, Alert에 대해 공부했습니다.

지난 공부에서는 Observability가 서비스와 인프라의 상태를 확인하고 장애 원인을 찾기 위한 개념이라는 것을 배웠습니다. 오늘은 실제로 운영 상태를 확인할 때 어떤 정보를 보는지 중심으로 공부했습니다.

Metric은 CPU 사용률, Memory 사용량, Disk 사용량, 네트워크 트래픽처럼 숫자로 표현되는 운영 지표입니다. 예를 들어 EC2 서버의 CPU 사용률이 90% 이상으로 계속 유지된다면 서버에 부하가 많이 걸리고 있다고 판단할 수 있습니다.

Log는 서비스나 서버에서 발생한 이벤트 기록입니다. 예를 들어 애플리케이션 에러 메시지, 접속 기록, 배포 중 발생한 오류 등이 로그에 남을 수 있습니다. Metric이 “현재 상태를 숫자로 보여주는 것”이라면, Log는 “무슨 일이 있었는지 기록으로 보여주는 것”이라고 이해했습니다.

Alert는 특정 조건이 발생했을 때 운영자에게 알려주는 기능입니다. 예를 들어 CPU 사용률이 80%를 넘거나, 에러 로그가 많이 발생하거나, 서버 응답 시간이 길어지면 알림을 보내도록 설정할 수 있습니다.

## 3. 내가 이해한 내용

제가 이해한 Metric, Log, Alert의 관계는 다음과 같습니다.

Metric은 서비스 상태를 숫자로 확인하는 정보입니다.
Log는 문제가 발생했을 때 원인을 찾기 위한 기록입니다.
Alert는 문제가 발생했거나 발생할 가능성이 있을 때 알려주는 장치입니다.

예를 들어 웹 서비스가 느려졌다고 가정하면 먼저 CPU, Memory, Network 같은 Metric을 확인할 수 있습니다. CPU 사용률이 높다면 서버 부하가 원인일 수 있습니다. 하지만 왜 CPU 사용률이 높아졌는지는 Metric만으로 정확히 알기 어렵습니다.

이때 Log를 확인하면 특정 API에서 에러가 반복되고 있는지, 특정 요청이 너무 많이 들어오고 있는지, 애플리케이션 내부에서 어떤 문제가 발생했는지 확인할 수 있습니다.

그리고 이런 문제가 사람이 직접 확인하기 전에 발견되도록 Alert를 설정할 수 있습니다. 예를 들어 CPU 사용률이 80% 이상으로 5분 이상 유지되면 알림을 보내도록 설정하면 장애를 더 빨리 인지할 수 있습니다.

결국 Observability는 Metric, Log, Alert 같은 정보를 이용해서 서비스 상태를 확인하고 문제 원인을 찾는 과정이라고 이해했습니다.

## 4. GPT에게 물어본 질문

* Metric이 무엇인지
* Log가 무엇인지
* Alert가 무엇인지
* Metric과 Log의 차이가 무엇인지
* Observability에서 Metric, Log, Alert가 각각 어떤 역할을 하는지
* AWS CloudWatch에서 Metric, Log, Alarm이 어떻게 연결되는지

## 5. 새로 알게 된 점

오늘 새로 알게 된 점은 Metric과 Log가 역할이 다르다는 점입니다.

처음에는 둘 다 서버 상태를 확인하는 정보라고만 생각했습니다. 하지만 공부해보니 Metric은 숫자로 현재 상태를 빠르게 확인하는 데 유용하고, Log는 문제가 발생했을 때 구체적인 원인을 찾는 데 유용하다는 차이가 있었습니다.

또한 Alert는 단순히 알림을 보내는 기능이 아니라, 운영자가 문제를 빨리 인지하고 대응할 수 있게 도와주는 중요한 운영 장치라는 것을 알게 되었습니다.

AWS에서는 CloudWatch를 사용해서 Metric을 확인하고, CloudWatch Logs를 사용해서 로그를 수집하고, CloudWatch Alarm을 사용해서 특정 조건이 발생했을 때 알림을 설정할 수 있다는 것도 알게 되었습니다.

## 6. Must / Optional 후보


## 7. 아직 헷갈리는 부분

아직 Metric과 Log를 실제 AWS 콘솔에서 어떻게 확인하는지는 직접 실습해봐야 더 명확하게 이해할 수 있을 것 같습니다.

또한 Alert 조건을 설정할 때 CPU 사용률을 몇 퍼센트로 잡아야 적절한지, 몇 분 동안 지속될 때 알림을 보내야 하는지 같은 기준은 아직 더 공부가 필요합니다.

## 8. 내일 할 일

오늘 공부한 Metric, Log, Alert 개념을 바탕으로 AWS CloudWatch를 더 자세히 공부할 예정입니다.

* CloudWatch Metric 확인 방법
* CloudWatch Logs 구조
* CloudWatch Alarm 설정 방식
* EC2 CPU 사용률 기준 Alarm 예시 정리

## 9. 참고한 자료

* AWS 공식 문서 - Metrics in Amazon CloudWatch
* AWS 공식 문서 - Amazon CloudWatch Logs concepts
* AWS 공식 문서 - Using Amazon CloudWatch alarms
