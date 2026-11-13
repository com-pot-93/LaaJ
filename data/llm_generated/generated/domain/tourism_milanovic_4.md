flowchart LR
se:startevent:((startevent))-->a1:task:(Receive trip request)
a1:task:(Receive trip request)-->e1s:parallelgateway:{AND}
e1s:parallelgateway:{AND}-->a5:task:(Send price request to the airlines)
a5:task:(Send price request to the airlines)-->a7:task:(Collect responses from the airlines)
a7:task:(Collect responses from the airlines)-->a9:task:(Select airline)
a9:task:(Select airline)-->e1e:parallelgateway:{AND}
e1s:parallelgateway:{AND}-->a13:task:(Send price request to the hotels)
a13:task:(Send price request to the hotels)-->a15:task:(Collect responses from the hotels)
a15:task:(Collect responses from the hotels)-->a17:task:(Select hotel)
a17:task:(Select hotel)-->e1e:parallelgateway:{AND}
e1e:parallelgateway:{AND}-->a21:task:(Prepare the tour plan)
a21:task:(Prepare the tour plan)-->a23:task:(Send the tour plan to the customer)
a23:task:(Send the tour plan to the customer)-->ee:endevent:((endevent))