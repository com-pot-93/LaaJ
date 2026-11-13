flowchart LR
se:startevent:((startevent))-->a6:task:(Receive data subject request)
a6:task:(Receive data subject request)-->a7:task:(Send request to the third party)
a7:task:(Send request to the third party)-->a8:task:(Receive third party request)
a8:task:(Receive third party request)-->g1s:parallelgateway:{AND}
g1s:parallelgateway:{AND}-->a3:task:(Retrieve elaborations)
a3:task:(Retrieve elaborations)-->g1e:parallelgateway:{AND}
g1s:parallelgateway:{AND}-->a4:task:(Retrieve available data of the data subject)
a4:task:(Retrieve available data of the data subject)-->g1e:parallelgateway:{AND}
g1e:parallelgateway:{AND}-->a2:task:(Communicate data and elaborations to the third party)
a2:task:(Communicate data and elaborations to the third party)-->a9:task:(Communicate data and elaborations to the data subject)
a9:task:(Communicate data and elaborations to the data subject)-->ee:endevent:((endevent))