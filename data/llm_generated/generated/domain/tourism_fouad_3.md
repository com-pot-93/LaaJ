flowchart LR
se:startevent:((startevent))-->a1:task:(Get travel request)
a1:task:(Get travel request)-->a3:task:(Prepare the tour plan)
a3:task:(Prepare the tour plan)-->a5:task:(Send the tour plan)
a5:task:(Send the tour plan)-->a7:task:(Receive response)
a7:task:(Receive response)-->e1s:exclusivegateway:{x}
e1s:exclusivegateway:{x}-->|"Branch 1"|a11:task:(Book the tour)
a11:task:(Book the tour)-->e3s:exclusivegateway:{x}
e3e:exclusivegateway:{x}-->|"true"|e3s:exclusivegateway:{x}
e3s:exclusivegateway:{x}-->a15:task:(Charge customer)
a15:task:(Charge customer)-->e4s:exclusivegateway:{x}
e4s:exclusivegateway:{x}-->|"Branch 1"|a19:task:(Contact customer)
a19:task:(Contact customer)-->e4e:exclusivegateway:{x}
e4s:exclusivegateway:{x}-->|"Branch 2"|a21:task:(Send the bill)
a21:task:(Send the bill)-->e4e:exclusivegateway:{x}
e4e:exclusivegateway:{x}-->a27:task:(Send booking confirmation)
a27:task:(Send booking confirmation)-->e3e:exclusivegateway:{x}
e3e:exclusivegateway:{x}-->e1e:exclusivegateway:{x}
e1s:exclusivegateway:{x}-->|"Branch 2"|e1e:exclusivegateway:{x}
e1e:exclusivegateway:{x}-->ee:endevent:((endevent))