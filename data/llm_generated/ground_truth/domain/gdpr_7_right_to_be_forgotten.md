flowchart LR
se:startevent:((startevent))-->a9:task:(Receive data subject request)
a9:task:(Receive data subject request)-->a0:task:(Retrieve data)
a0:task:(Retrieve data)-->a1:task:(Check if received data is still relevant)
a1:task:(Check if received data is still relevant)-->g1s:exclusivegateway:{x}
g1s:exclusivegateway:{x}-->a3:task:(Explain why data is still relevant)
a3:task:(Explain why data is still relevant)-->g1e:exclusivegateway:{x}
g1s:exclusivegateway:{x}-->a6:task:(Eliminate data)
a6:task:(Eliminate data)-->a7:task:(Send notification about  elimination)
a7:task:(Send notification about  elimination)-->g1e:exclusivegateway:{x}
g1e:exclusivegateway:{x}-->ee:endevent:((endevent))