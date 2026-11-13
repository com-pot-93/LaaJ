flowchart LR
se:startevent:((startevent))-->a1:task:(Receive production order)
a1:task:(Receive production order)-->a2:task:(Prepare materrials)
a2:task:(Prepare materrials)-->a3:task:(Assemble door)
a3:task:(Assemble door)-->g1s:exclusivegateway:{x}
g1s:exclusivegateway:{x}-->g1e:exclusivegateway:{x}
g1e:exclusivegateway:{x}-->|"true"|a5:task:(Send inquiry for quality check)
a5:task:(Send inquiry for quality check)-->a11:task:(Receive inquiry for quality check)
a11:task:(Receive inquiry for quality check)-->a12:task:(Check quality)
a12:task:(Check quality)-->a13:task:(Send quality report)
a13:task:(Send quality report)-->a6:task:(Receive quality report)
a6:task:(Receive quality report)-->g2s:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->a10:task:(Fix door)
a10:task:(Fix door)-->g2e:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->a8:task:(Release door)
a8:task:(Release door)-->-1:escalate:((^))
-1:escalate:((^))-->g2e:exclusivegateway:{x}
g2e:exclusivegateway:{x}-->g1s:exclusivegateway:{x}
g1e:exclusivegateway:{x}-->ee:endevent:((endevent))