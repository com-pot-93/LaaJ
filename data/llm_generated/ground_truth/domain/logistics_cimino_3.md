flowchart LR
se:startevent:((startevent))-->a1:task:(Receive shipment request)
a1:task:(Receive shipment request)-->g1s:parallelgateway:{AND}
g1s:parallelgateway:{AND}-->a14:task:(Package goods)
a14:task:(Package goods)-->g1e:parallelgateway:{AND}
g1s:parallelgateway:{AND}-->a4:task:(Select kind of shipment)
a4:task:(Select kind of shipment)-->g2s:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->a6:task:(Request quotes from carriers)
a6:task:(Request quotes from carriers)-->a7:task:(Assign a carrier)
a7:task:(Assign a carrier)-->a8:task:(Prepare paperwork)
a8:task:(Prepare paperwork)-->g2e:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->a10:task:(Fill in a post label)
a10:task:(Fill in a post label)-->a11:task:(Check insuarance)
a11:task:(Check insuarance)-->g3s:exclusivegateway:{x}
g3s:exclusivegateway:{x}-->g3e:exclusivegateway:{x}
g3s:exclusivegateway:{x}-->a0:task:(Take out extra insuarance)
a0:task:(Take out extra insuarance)-->g3e:exclusivegateway:{x}
g3e:exclusivegateway:{x}-->g2e:exclusivegateway:{x}
g2e:exclusivegateway:{x}-->g1e:parallelgateway:{AND}
g1e:parallelgateway:{AND}-->a16:task:(Add paperwork)
a16:task:(Add paperwork)-->a17:task:(Move package to pickup area)
a17:task:(Move package to pickup area)-->ee:endevent:((endevent))