flowchart LR
se:startevent:((startevent))-->a1:task:(Receive data subject request)
a1:task:(Receive data subject request)-->a3:task:(Check if withdrawn data are relevant)
a3:task:(Check if withdrawn data are relevant)-->e1s:exclusivegateway:{x}
e1s:exclusivegateway:{x}-->|"Relevant"|a7:task:(Stop using withdrawn data)
a7:task:(Stop using withdrawn data)-->a9:task:(Communicate the withdraw)
a9:task:(Communicate the withdraw)-->e1e:exclusivegateway:{x}
e1s:exclusivegateway:{x}-->|"Not Relevant"|a13:task:(Inform the user that the withdraw will stop all running BPs)
a13:task:(Inform the user that the withdraw will stop all running BPs)-->a15:task:(Receive the notification about continuation)
a15:task:(Receive the notification about continuation)-->e4s:exclusivegateway:{x}
e4s:exclusivegateway:{x}-->|"Continue"|a19:task:(Stop running BPs using withdrawn data)
a19:task:(Stop running BPs using withdrawn data)-->a21:task:(Stop using withdrawn data)
a21:task:(Stop using withdrawn data)-->a23:task:(Communicate the withdraw)
a23:task:(Communicate the withdraw)-->e4e:exclusivegateway:{x}
e4s:exclusivegateway:{x}-->|"Abort"|e4e:exclusivegateway:{x}
e4e:exclusivegateway:{x}-->e1e:exclusivegateway:{x}
e1e:exclusivegateway:{x}-->ee:endevent:((endevent))