flowchart LR
se:startevent:((startevent))-->a1:task:(Package product)
a1:task:(Package product)-->a3:task:(Ship product)
a3:task:(Ship product)-->e1s:exclusivegateway:{x}
e1s:exclusivegateway:{x}-->|"Deliver to door"|a7:task:(Deliver to door)
a7:task:(Deliver to door)-->e3s:exclusivegateway:{x}
e3s:exclusivegateway:{x}-->|"Print receipt"|a13:task:(Print pick-up receipt)
a13:task:(Print pick-up receipt)-->a17:task:(Post pick-up receipt)
a17:task:(Post pick-up receipt)-->a19:task:(Reroute to the closest station)
a19:task:(Reroute to the closest station)-->e3e:exclusivegateway:{x}
e3s:exclusivegateway:{x}-->|"Skip receipt"|e3e:exclusivegateway:{x}
e3e:exclusivegateway:{x}-->e1e:exclusivegateway:{x}
e1s:exclusivegateway:{x}-->|"Deliver to station"|a9:task:(Deliver to station)
a9:task:(Deliver to station)-->e1e:exclusivegateway:{x}
e1e:exclusivegateway:{x}-->e7s:exclusivegateway:{x}
e7s:exclusivegateway:{x}-->|"Return"|a29:task:(Receive the product back)
a29:task:(Receive the product back)-->e7e:exclusivegateway:{x}
e7s:exclusivegateway:{x}-->|"No return"|e7e:exclusivegateway:{x}
e7e:exclusivegateway:{x}-->ee:endevent:((endevent))