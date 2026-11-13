flowchart LR
se:startevent:((startevent))-->a1:task:(Get travel request)
a1:task:(Get travel request)-->a2:task:(Prepare the tour plan)
a2:task:(Prepare the tour plan)-->a3:task:(Send the tour  plan)
a3:task:(Send the tour  plan)-->a4:task:(Receive response)
a4:task:(Receive response)-->g1s:exclusivegateway:{x}
g1s:exclusivegateway:{x}-->a7:task:(Book the tour)
a7:task:(Book the tour)-->g2s:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->g2e:exclusivegateway:{x}
g2e:exclusivegateway:{x}-->|"true"|a6:task:(Charge  customer)
a6:task:(Charge  customer)-->g3s:exclusivegateway:{x}
g3s:exclusivegateway:{x}-->a9:task:(Contact customer)
a9:task:(Contact customer)-->g3e:exclusivegateway:{x}
g3s:exclusivegateway:{x}-->a13:task:(Send the bill)
a13:task:(Send the bill)-->a11:task:(Send booking confirmation)
a11:task:(Send booking confirmation)-->-1:escalate:((^))
-1:escalate:((^))-->g3e:exclusivegateway:{x}
g3e:exclusivegateway:{x}-->g2s:exclusivegateway:{x}
g2e:exclusivegateway:{x}-->g1e:exclusivegateway:{x}
g1s:exclusivegateway:{x}-->g1e:exclusivegateway:{x}
g1e:exclusivegateway:{x}-->ee:endevent:((endevent))