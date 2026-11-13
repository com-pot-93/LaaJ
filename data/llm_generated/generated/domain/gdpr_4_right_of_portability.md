flowchart LR
se:startevent:((startevent))-->a1:task:(Receive data subject request)
a1:task:(Receive data subject request)-->a3:task:(Send request to the third party)
a3:task:(Send request to the third party)-->a5:task:(Receive third party request)
a5:task:(Receive third party request)-->e1s:parallelgateway:{AND}
e1s:parallelgateway:{AND}-->a9:task:(Retrieve elaborations)
a9:task:(Retrieve elaborations)-->e1e:parallelgateway:{AND}
e1s:parallelgateway:{AND}-->a11:task:(Retrieve available data of the data subject)
a11:task:(Retrieve available data of the data subject)-->e1e:parallelgateway:{AND}
e1e:parallelgateway:{AND}-->a17:task:(Communicate data and elaborations to the third party)
a17:task:(Communicate data and elaborations to the third party)-->a19:task:(Communicate data and elaborations to the data subject)
a19:task:(Communicate data and elaborations to the data subject)-->ee:endevent:((endevent))