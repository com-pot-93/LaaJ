flowchart LR
se:startevent:((startevent))-->a1:task:(Request booking)
a1:task:(Request booking)-->a3:task:(Get booking request)
a3:task:(Get booking request)-->a5:task:(Check availability)
a5:task:(Check availability)-->e1s:exclusivegateway:{x}
e1s:exclusivegateway:{x}-->|"Alternative needed"|a9:task:(Propose alternative time)
a9:task:(Propose alternative time)-->e1e:exclusivegateway:{x}
e1s:exclusivegateway:{x}-->|"Available"|e1e:exclusivegateway:{x}
e1e:exclusivegateway:{x}-->a15:task:(Send notification)
a15:task:(Send notification)-->a17:task:(Get response)
a17:task:(Get response)-->e4s:exclusivegateway:{x}
e4s:exclusivegateway:{x}-->|"Accept"|e4e:exclusivegateway:{x}
e4s:exclusivegateway:{x}-->|"Reject"|a23:task:(Send the bill)
a23:task:(Send the bill)-->a25:task:(Confirm booking)
a25:task:(Confirm booking)-->e4e:exclusivegateway:{x}
e4e:exclusivegateway:{x}-->ee:endevent:((endevent))