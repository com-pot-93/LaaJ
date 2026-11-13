flowchart LR
se:startevent:((startevent))-->a1:task:(Receive production order)
a1:task:(Receive production order)-->a3:task:(Prepare materrials)
a3:task:(Prepare materrials)-->a5:task:(Assemble door)
a5:task:(Assemble door)-->e1s:exclusivegateway:{x}
e1e:exclusivegateway:{x}-->|"true"|e1s:exclusivegateway:{x}
e1s:exclusivegateway:{x}-->a9:task:(Send inquiry for quality check)
a9:task:(Send inquiry for quality check)-->a11:task:(Receive inquiry for quality check)
a11:task:(Receive inquiry for quality check)-->a13:task:(Check quality)
a13:task:(Check quality)-->a15:task:(Send quality report)
a15:task:(Send quality report)-->a17:task:(Receive quality report)
a17:task:(Receive quality report)-->e2s:exclusivegateway:{x}
e2s:exclusivegateway:{x}-->|"Fix required"|a21:task:(Fix door)
a21:task:(Fix door)-->e2e:exclusivegateway:{x}
e2s:exclusivegateway:{x}-->|"Quality passed"|a23:task:(Release door)
a23:task:(Release door)-->e2e:exclusivegateway:{x}
e2e:exclusivegateway:{x}-->e1e:exclusivegateway:{x}
e1e:exclusivegateway:{x}-->ee:endevent:((endevent))