flowchart LR
se:startevent:((startevent))-->a1:task:(Package product)
a1:task:(Package product)-->a2:task:(Ship product)
a2:task:(Ship product)-->g1s:exclusivegateway:{x}
g1s:exclusivegateway:{x}-->a4:task:(Deliver to door)
a4:task:(Deliver to door)-->g2s:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->a7:task:(Print pick-up receipt)
a7:task:(Print pick-up receipt)-->a8:task:(Post pick-up receipt)
a8:task:(Post pick-up receipt)-->a12:task:(Reroute to the closest station)
a12:task:(Reroute to the closest station)-->g2e:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->g2e:exclusivegateway:{x}
g2e:exclusivegateway:{x}-->g1e:exclusivegateway:{x}
g1s:exclusivegateway:{x}-->a5:task:(Deliver to station)
a5:task:(Deliver to station)-->g1e:exclusivegateway:{x}
g1e:exclusivegateway:{x}-->g3s:exclusivegateway:{x}
g3s:exclusivegateway:{x}-->g3e:exclusivegateway:{x}
g3s:exclusivegateway:{x}-->a13:task:(Receive the product back)
a13:task:(Receive the product back)-->g3e:exclusivegateway:{x}
g3e:exclusivegateway:{x}-->ee:endevent:((endevent))