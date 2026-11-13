flowchart LR
se:startevent:((startevent))-->a1:task:(arrive to the hospital)
a1:task:(arrive to the hospital)-->a3:task:(prepare room for the surgery)
a3:task:(prepare room for the surgery)-->a5:task:(perform surgery)
a5:task:(perform surgery)-->e1s:parallelgateway:{AND}
e1s:parallelgateway:{AND}-->a9:task:(discharge patient)
a9:task:(discharge patient)-->e1e:parallelgateway:{AND}
e1s:parallelgateway:{AND}-->a11:task:(sanitize room for the surgery)
a11:task:(sanitize room for the surgery)-->e1e:parallelgateway:{AND}
e1e:parallelgateway:{AND}-->a17:task:(fill the report)
a17:task:(fill the report)-->e4s:exclusivegateway:{x}
e4s:exclusivegateway:{x}-->|"Pay"|a21:task:(pay the bill)
a21:task:(pay the bill)-->e4e:exclusivegateway:{x}
e4s:exclusivegateway:{x}-->|"No Pay"|e4e:exclusivegateway:{x}
e4e:exclusivegateway:{x}-->ee:endevent:((endevent))