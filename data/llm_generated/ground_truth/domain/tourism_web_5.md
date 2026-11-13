flowchart LR
se:startevent:((startevent))-->a12:task:(Request booking)
a12:task:(Request booking)-->a0:task:(Get booking request)
a0:task:(Get booking request)-->a1:task:(Check availability)
a1:task:(Check availability)-->g1s:exclusivegateway:{x}
g1s:exclusivegateway:{x}-->a4:task:(Propose alternative time)
a4:task:(Propose alternative time)-->g1e:exclusivegateway:{x}
g1s:exclusivegateway:{x}-->g1e:exclusivegateway:{x}
g1e:exclusivegateway:{x}-->a5:task:(Send notification)
a5:task:(Send notification)-->a6:task:(Get response)
a6:task:(Get response)-->g2s:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->g2e:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->a10:task:(Send the bill)
a10:task:(Send the bill)-->a8:task:(Confirm booking)
a8:task:(Confirm booking)-->g2e:exclusivegateway:{x}
g2e:exclusivegateway:{x}-->ee:endevent:((endevent))