flowchart LR
se:startevent:((startevent))-->a1:task:(Retrieve breached data)
a1:task:(Retrieve breached data)-->a3:task:(Retrieve breached subjects)
a3:task:(Retrieve breached subjects)-->e1s:parallelgateway:{AND}
e1s:parallelgateway:{AND}-->a7:task:(Data loss limitation)
a7:task:(Data loss limitation)-->e1e:parallelgateway:{AND}
e1s:parallelgateway:{AND}-->a9:task:(Notify national authority)
a9:task:(Notify national authority)-->e1e:parallelgateway:{AND}
e1e:parallelgateway:{AND}-->a15:task:(Evaluate stolen data)
a15:task:(Evaluate stolen data)-->e4s:exclusivegateway:{x}
e4s:exclusivegateway:{x}-->a23:task:(Send notification)
a23:task:(Send notification)-->e4e:exclusivegateway:{x}
e4s:exclusivegateway:{x}-->|"|"|a19:task:(Evaluate security standard)
a19:task:(Evaluate security standard)-->e6s:exclusivegateway:{x}
e6s:exclusivegateway:{x}-->a22:task:(Send notification)
a22:task:(Send notification)-->e6e:exclusivegateway:{x}
e6s:exclusivegateway:{x}-->|"|"|a25:task:(Request if breached data has to be communicated to the data subject)
a25:task:(Request if breached data has to be communicated to the data subject)-->a29:task:(Receive notification for the request)
a29:task:(Receive notification for the request)-->e8s:exclusivegateway:{x}
e8s:exclusivegateway:{x}-->a21:task:(Send notification)
a21:task:(Send notification)-->e8e:exclusivegateway:{x}
e8s:exclusivegateway:{x}-->|"|"|a33:task:(Send notification)
a33:task:(Send notification)-->e8e:exclusivegateway:{x}
e8e:exclusivegateway:{x}-->e6e:exclusivegateway:{x}
e6e:exclusivegateway:{x}-->e4e:exclusivegateway:{x}
e4e:exclusivegateway:{x}-->ee:endevent:((endevent))