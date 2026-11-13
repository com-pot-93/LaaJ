flowchart LR
se:startevent:((startevent))-->a1:task:(Search for a customer)
a1:task:(Search for a customer)-->a3:task:(Make customer an offer)
a3:task:(Make customer an offer)-->e1s:exclusivegateway:{x}
e1s:exclusivegateway:{x}-->|"Branch 2"|e1e:exclusivegateway:{x}
e1s:exclusivegateway:{x}-->a7:task:(Receive additional request)
a7:task:(Receive additional request)-->a9:task:(Provide details)
a9:task:(Provide details)-->e3s:exclusivegateway:{x}
e3s:exclusivegateway:{x}-->|"Branch 2"|e3e:exclusivegateway:{x}
e3s:exclusivegateway:{x}-->a15:task:(Receive booking request)
a15:task:(Receive booking request)-->a17:task:(Send the bill)
a17:task:(Send the bill)-->e5s:exclusivegateway:{x}
e5s:exclusivegateway:{x}-->e5e:exclusivegateway:{x}
e5e:exclusivegateway:{x}-->|"true"|a21:task:(Receive payment)
a21:task:(Receive payment)-->e6s:exclusivegateway:{x}
e6s:exclusivegateway:{x}-->|"Branch 1"|a25:task:(Contact customer)
a25:task:(Contact customer)-->e6e:exclusivegateway:{x}
e6s:exclusivegateway:{x}-->|"Branch 2"|a27:task:(Book travel)
a27:task:(Book travel)-->a29:task:(Send booking confirmation)
a29:task:(Send booking confirmation)-->e6e:exclusivegateway:{x}
e6e:exclusivegateway:{x}-->e5s:exclusivegateway:{x}
e5e:exclusivegateway:{x}-->e3e:exclusivegateway:{x}
e3e:exclusivegateway:{x}-->e1e:exclusivegateway:{x}
e1e:exclusivegateway:{x}-->ee:endevent:((endevent))