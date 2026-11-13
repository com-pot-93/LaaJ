flowchart LR
se:startevent:((startevent))-->a0:task:(Retrieve breached data)
a0:task:(Retrieve breached data)-->a1:task:(Retrieve breached subjects)
a1:task:(Retrieve breached subjects)-->g1s:parallelgateway:{AND}
g1s:parallelgateway:{AND}-->a7:task:(Data loss limitation)
a7:task:(Data loss limitation)-->g1e:parallelgateway:{AND}
g1s:parallelgateway:{AND}-->a3:task:(Notify national authority)
a3:task:(Notify national authority)-->a8:task:(Evaluate stolen data)
a8:task:(Evaluate stolen data)-->g2s:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->a20:task:(Send notification)
a20:task:(Send notification)-->g2e:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->|"|"|a11:task:(Evaluate security standard)
a11:task:(Evaluate security standard)-->g3s:exclusivegateway:{x}
g3s:exclusivegateway:{x}-->a19:task:(Send notification)
a19:task:(Send notification)-->g3e:exclusivegateway:{x}
g3s:exclusivegateway:{x}-->|"|"|a13:task:(Request if breached data has to be communicated to the data subject)
a13:task:(Request if breached data has to be communicated to the data subject)-->a17:task:(Receive notification for the request)
a17:task:(Receive notification for the request)-->g4s:exclusivegateway:{x}
g4s:exclusivegateway:{x}-->a18:task:(Send notification)
a18:task:(Send notification)-->g4e:exclusivegateway:{x}
g4s:exclusivegateway:{x}-->|"|"|g4e:exclusivegateway:{x}
g4e:exclusivegateway:{x}-->g3e:exclusivegateway:{x}
g3e:exclusivegateway:{x}-->g2e:exclusivegateway:{x}
g2e:exclusivegateway:{x}-->g1e:parallelgateway:{AND}
g1e:parallelgateway:{AND}-->ee:endevent:((endevent))