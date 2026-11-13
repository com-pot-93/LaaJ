flowchart LR
se:startevent:((startevent))-->a1:task:(Assess patient conditions)
a1:task:(Assess patient conditions)-->g1s:parallelgateway:{AND}
g1s:parallelgateway:{AND}-->a3:task:(Perform physical examination)
a3:task:(Perform physical examination)-->g1e:parallelgateway:{AND}
g1s:parallelgateway:{AND}-->a11:task:(Draw blood samples)
a11:task:(Draw blood samples)-->a12:task:(Send analysis to the lab)
a12:task:(Send analysis to the lab)-->a13:task:(Receive analysis from the lab)
a13:task:(Receive analysis from the lab)-->g1e:parallelgateway:{AND}
g1e:parallelgateway:{AND}-->a5:task:(Make diagnosis)
a5:task:(Make diagnosis)-->g2s:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->a7:task:(Surgical intervention)
a7:task:(Surgical intervention)-->g2e:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->a14:task:(Plan surgery)
a14:task:(Plan surgery)-->g2e:exclusivegateway:{x}
g2e:exclusivegateway:{x}-->a9:task:(Discharge patient)
a9:task:(Discharge patient)-->ee:endevent:((endevent))