flowchart LR
se:startevent:((startevent))-->a1:task:(Receive customer request)
a1:task:(Receive customer request)-->a3:task:(Check customer request)
a3:task:(Check customer request)-->e1s:exclusivegateway:{x}
e1s:exclusivegateway:{x}-->e3s:exclusivegateway:{x}
e3s:exclusivegateway:{x}-->|"Branch 1"|a9:task:(Manual registration)
a9:task:(Manual registration)-->e3e:exclusivegateway:{x}
e3s:exclusivegateway:{x}-->|"Branch 2"|a11:task:(Automatic registration)
a11:task:(Automatic registration)-->e3e:exclusivegateway:{x}
e3e:exclusivegateway:{x}-->e6s:exclusivegateway:{x}
e6s:exclusivegateway:{x}-->e6e:exclusivegateway:{x}
e6e:exclusivegateway:{x}-->|"Loop"|a19:task:(Search for attraction provider)
a19:task:(Search for attraction provider)-->e7s:exclusivegateway:{x}
e7s:exclusivegateway:{x}-->|"Loop"|a23:task:(Book attraction)
a23:task:(Book attraction)-->e9s:exclusivegateway:{x}
e9s:exclusivegateway:{x}-->|"Branch 1"|a27:task:(Receive rejection)
a27:task:(Receive rejection)-->e9e:exclusivegateway:{x}
e9s:exclusivegateway:{x}-->|"Branch 2"|a29:task:(Receive booking confirmation)
a29:task:(Receive booking confirmation)-->e9e:exclusivegateway:{x}
e9e:exclusivegateway:{x}-->a31:task:(Send confirmation to the customer)
a31:task:(Send confirmation to the customer)-->e12s:exclusivegateway:{x}
e12s:exclusivegateway:{x}-->|"Loop"|e12e:exclusivegateway:{x}
e12s:exclusivegateway:{x}-->|"Exit"|-1:escalate:((^))
-1:escalate:((^))-->e12e:exclusivegateway:{x}
e12e:exclusivegateway:{x}-->e7e:exclusivegateway:{x}
e7s:exclusivegateway:{x}-->|"Branch 2"|-1:escalate:((^))
-1:escalate:((^))-->e7e:exclusivegateway:{x}
e7e:exclusivegateway:{x}-->e6s:exclusivegateway:{x}
e6e:exclusivegateway:{x}-->e1e:exclusivegateway:{x}
e1s:exclusivegateway:{x}-->|"Branch 2"|a45:task:(Send notification to the customer)
a45:task:(Send notification to the customer)-->e1e:exclusivegateway:{x}
e1e:exclusivegateway:{x}-->ee:endevent:((endevent))