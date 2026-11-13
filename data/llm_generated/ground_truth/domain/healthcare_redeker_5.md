flowchart LR
se:startevent:((startevent))-->a1:task:(arrive to the hospital)
a1:task:(arrive to the hospital)-->a6:task:(prepare room for the surgery)
a6:task:(prepare room for the surgery)-->a8:task:(perform surgery)
a8:task:(perform surgery)-->g1s:parallelgateway:{AND}
g1s:parallelgateway:{AND}-->a9:task:(discharge patient)
a9:task:(discharge patient)-->g1e:parallelgateway:{AND}
g1s:parallelgateway:{AND}-->a12:task:(sanitize room for the surgery)
a12:task:(sanitize room for the surgery)-->g1e:parallelgateway:{AND}
g1e:parallelgateway:{AND}-->a7:task:(fill the report)
a7:task:(fill the report)-->g2s:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->a2:task:(pay the bill)
a2:task:(pay the bill)-->g2e:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->g2e:exclusivegateway:{x}
g2e:exclusivegateway:{x}-->ee:endevent:((endevent))