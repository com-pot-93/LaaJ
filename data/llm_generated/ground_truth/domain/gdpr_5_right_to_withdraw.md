flowchart LR
se:startevent:((startevent))-->a11:task:(Receive data subject request)
a11:task:(Receive data subject request)-->a1:task:(Check if withdrawn data are relevant)
a1:task:(Check if withdrawn data are relevant)-->g1s:exclusivegateway:{x}
g1s:exclusivegateway:{x}-->a9:task:(Stop using withdrawn data)
a9:task:(Stop using withdrawn data)-->a5:task:(Communicate the withdraw)
a5:task:(Communicate the withdraw)-->g1e:exclusivegateway:{x}
g1s:exclusivegateway:{x}-->a0:task:(Inform the user that the withdraw will stop all running BPs)
a0:task:(Inform the user that the withdraw will stop all running BPs)-->a7:task:(Receive the notification about continuation)
a7:task:(Receive the notification about continuation)-->g2s:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->a8:task:(Stop running BPs using withdrawn data)
a8:task:(Stop running BPs using withdrawn data)-->b0:task:(Stop using withdrawn data)
b0:task:(Stop using withdrawn data)-->a6:task:(Communicate the withdraw)
a6:task:(Communicate the withdraw)-->g2e:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->g2e:exclusivegateway:{x}
g2e:exclusivegateway:{x}-->g1e:exclusivegateway:{x}
g1e:exclusivegateway:{x}-->ee:endevent:((endevent))