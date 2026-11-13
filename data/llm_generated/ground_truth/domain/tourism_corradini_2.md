flowchart LR
se:startevent:((startevent))-->a1:task:(Search for a customer)
a1:task:(Search for a customer)-->a2:task:(Make customer an offer)
a2:task:(Make customer an offer)-->g1s:exclusivegateway:{x}
g1s:exclusivegateway:{x}-->a4:task:(Receive additional request)
a4:task:(Receive additional request)-->a6:task:(Provide details)
a6:task:(Provide details)-->g2s:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->g2e:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->a8:task:(Receive booking request)
a8:task:(Receive booking request)-->a11:task:(Send the bill)
a11:task:(Send the bill)-->g3s:exclusivegateway:{x}
g3s:exclusivegateway:{x}-->g3e:exclusivegateway:{x}
g3e:exclusivegateway:{x}-->|"true"|a13:task:(Receive payment)
a13:task:(Receive payment)-->g4s:exclusivegateway:{x}
g4s:exclusivegateway:{x}-->a17:task:(Contact customer)
a17:task:(Contact customer)-->g4e:exclusivegateway:{x}
g4s:exclusivegateway:{x}-->a10:task:(Book travel)
a10:task:(Book travel)-->a14:task:(Send booking confirmation)
a14:task:(Send booking confirmation)-->-1:escalate:((^))
-1:escalate:((^))-->g4e:exclusivegateway:{x}
g4e:exclusivegateway:{x}-->g3s:exclusivegateway:{x}
g3e:exclusivegateway:{x}-->g2e:exclusivegateway:{x}
g2e:exclusivegateway:{x}-->g1e:exclusivegateway:{x}
g1s:exclusivegateway:{x}-->g1e:exclusivegateway:{x}
g1e:exclusivegateway:{x}-->ee:endevent:((endevent))