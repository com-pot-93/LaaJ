flowchart LR
se:startevent:((startevent))-->a1:task:(Assess patient conditions)
a1:task:(Assess patient conditions)-->e1s:parallelgateway:{AND}
e1s:parallelgateway:{AND}-->a5:task:(Perform physical examination)
a5:task:(Perform physical examination)-->e1e:parallelgateway:{AND}
e1s:parallelgateway:{AND}-->a7:task:(Draw blood samples)
a7:task:(Draw blood samples)-->a9:task:(Send analysis to the lab)
a9:task:(Send analysis to the lab)-->a11:task:(Receive analysis from the lab)
a11:task:(Receive analysis from the lab)-->e1e:parallelgateway:{AND}
e1e:parallelgateway:{AND}-->a17:task:(Make diagnosis)
a17:task:(Make diagnosis)-->e4s:exclusivegateway:{x}
e4s:exclusivegateway:{x}-->|"Surgical intervention required"|a21:task:(Surgical intervention)
a21:task:(Surgical intervention)-->e4e:exclusivegateway:{x}
e4s:exclusivegateway:{x}-->|"Surgery planning required"|a23:task:(Plan surgery)
a23:task:(Plan surgery)-->e4e:exclusivegateway:{x}
e4e:exclusivegateway:{x}-->a29:task:(Discharge patient)
a29:task:(Discharge patient)-->ee:endevent:((endevent))