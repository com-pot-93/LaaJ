flowchart LR
se:startevent:((startevent))-->a1:task:(Receive trip request)
a1:task:(Receive trip request)-->g1s:parallelgateway:{AND}
g1s:parallelgateway:{AND}-->a2:task:(Send price request to the airlines)
a2:task:(Send price request to the airlines)-->a3:task:(Collect responses from the airlines)
a3:task:(Collect responses from the airlines)-->a4:task:(Select airline)
a4:task:(Select airline)-->g1e:parallelgateway:{AND}
g1s:parallelgateway:{AND}-->a5:task:(Send price request to the hotels)
a5:task:(Send price request to the hotels)-->a6:task:(Collect responses from the hotels)
a6:task:(Collect responses from the hotels)-->a7:task:(Select hotel)
a7:task:(Select hotel)-->g1e:parallelgateway:{AND}
g1e:parallelgateway:{AND}-->a10:task:(Prepare the tour plan)
a10:task:(Prepare the tour plan)-->a11:task:(Send the tour plan to the customer)
a11:task:(Send the tour plan to the customer)-->ee:endevent:((endevent))