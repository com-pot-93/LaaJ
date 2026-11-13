flowchart LR
se:startevent:((startevent))-->a1:task:(Receive shipment request)
a1:task:(Receive shipment request)-->e1s:parallelgateway:{AND}
e1s:parallelgateway:{AND}-->a5:task:(Package goods)
a5:task:(Package goods)-->e1e:parallelgateway:{AND}
e1s:parallelgateway:{AND}-->a7:task:(Select kind of shipment)
a7:task:(Select kind of shipment)-->e4s:exclusivegateway:{x}
e4s:exclusivegateway:{x}-->|"Option 1"|a13:task:(Request quotes from carriers)
a13:task:(Request quotes from carriers)-->a15:task:(Assign a carrier)
a15:task:(Assign a carrier)-->a17:task:(Prepare paperwork)
a17:task:(Prepare paperwork)-->e4e:exclusivegateway:{x}
e4s:exclusivegateway:{x}-->|"|"|a21:task:(Fill in a post label)
a21:task:(Fill in a post label)-->a23:task:(Check insuarance)
a23:task:(Check insuarance)-->e7s:exclusivegateway:{x}
e7s:exclusivegateway:{x}-->|"Extra"|a27:task:(Take out extra insuarance)
a27:task:(Take out extra insuarance)-->e7e:exclusivegateway:{x}
e7s:exclusivegateway:{x}-->|"No Extra"|e7e:exclusivegateway:{x}
e7e:exclusivegateway:{x}-->e4e:exclusivegateway:{x}
e4e:exclusivegateway:{x}-->e1e:parallelgateway:{AND}
e1e:parallelgateway:{AND}-->a35:task:(Add paperwork)
a35:task:(Add paperwork)-->a37:task:(Move package to pickup area)
a37:task:(Move package to pickup area)-->ee:endevent:((endevent))