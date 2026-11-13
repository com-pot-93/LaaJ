flowchart LR
se:startevent:((startevent))-->a1:task:(Receive data subject request)
a1:task:(Receive data subject request)-->a3:task:(Retrieve data)
a3:task:(Retrieve data)-->a5:task:(Check if received data is still relevant)
a5:task:(Check if received data is still relevant)-->e1s:exclusivegateway:{x}
e1s:exclusivegateway:{x}-->|"Relevant"|a9:task:(Explain why data is still relevant)
a9:task:(Explain why data is still relevant)-->e1e:exclusivegateway:{x}
e1s:exclusivegateway:{x}-->|"Not Relevant"|a11:task:(Eliminate data)
a11:task:(Eliminate data)-->a13:task:(Send notification about elimination)
a13:task:(Send notification about elimination)-->e1e:exclusivegateway:{x}
e1e:exclusivegateway:{x}-->ee:endevent:((endevent))