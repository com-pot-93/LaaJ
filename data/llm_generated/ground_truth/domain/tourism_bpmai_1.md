flowchart LR
se:startevent:((startevent))-->a1:task:(Receive customer request)
a1:task:(Receive customer request)-->a2:task:(Check customer request)
a2:task:(Check customer request)-->g1s:exclusivegateway:{x}
g1s:exclusivegateway:{x}-->g2s:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->a5:task:(Manual registration)
a5:task:(Manual registration)-->g2e:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->a4:task:(Automatic registration)
a4:task:(Automatic registration)-->g2e:exclusivegateway:{x}
g2e:exclusivegateway:{x}-->g3s:exclusivegateway:{x}
g3s:exclusivegateway:{x}-->g3e:exclusivegateway:{x}
g3e:exclusivegateway:{x}-->|"true"|a14:task:(Search for attraction provider)
a14:task:(Search for attraction provider)-->g4s:exclusivegateway:{x}
g4s:exclusivegateway:{x}-->a10:task:(Book attraction)
a10:task:(Book attraction)-->g5s:exclusivegateway:{x}
g5s:exclusivegateway:{x}-->a13:task:(Receive rejection)
a13:task:(Receive rejection)-->g5e:exclusivegateway:{x}
g5s:exclusivegateway:{x}-->a12:task:(Receive booking confirmation)
a12:task:(Receive booking confirmation)-->a16:task:(Send confirmation to the customer)
a16:task:(Send confirmation to the customer)-->-1:escalate:((^))
-1:escalate:((^))-->g5e:exclusivegateway:{x}
g5e:exclusivegateway:{x}-->g4e:exclusivegateway:{x}
g4s:exclusivegateway:{x}-->-1:escalate:((^))
-1:escalate:((^))-->g4e:exclusivegateway:{x}
g4e:exclusivegateway:{x}-->g3s:exclusivegateway:{x}
g3e:exclusivegateway:{x}-->g1e:exclusivegateway:{x}
g1s:exclusivegateway:{x}-->a9:task:(Send notification to the customer)
a9:task:(Send notification to the customer)-->g1e:exclusivegateway:{x}
g1e:exclusivegateway:{x}-->ee:endevent:((endevent))