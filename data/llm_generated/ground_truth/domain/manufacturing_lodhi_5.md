flowchart LR
se:startevent:((startevent))-->a5:task:(Receive production order)
a5:task:(Receive production order)-->a16:task:(Prepare production order)
a16:task:(Prepare production order)-->g1s:exclusivegateway:{x}
g1s:exclusivegateway:{x}-->g1e:exclusivegateway:{x}
g1e:exclusivegateway:{x}-->|"true"|a6:task:(Collect raw materials)
a6:task:(Collect raw materials)-->a7:task:(Cutting)
a7:task:(Cutting)-->g2s:parallelgateway:{AND}
g2s:parallelgateway:{AND}-->a9:task:(Stitching)
a9:task:(Stitching)-->g2e:parallelgateway:{AND}
g2s:parallelgateway:{AND}-->a10:task:(Printing)
a10:task:(Printing)-->g2e:parallelgateway:{AND}
g2e:parallelgateway:{AND}-->a12:task:(Complete production)
a12:task:(Complete production)-->a0:task:(Check quality)
a0:task:(Check quality)-->a1:task:(Create quality report)
a1:task:(Create quality report)-->g3s:exclusivegateway:{x}
g3s:exclusivegateway:{x}-->a3:task:(Adjust  settings)
a3:task:(Adjust  settings)-->g3e:exclusivegateway:{x}
g3s:exclusivegateway:{x}-->a13:task:(Send data to warehouse)
a13:task:(Send data to warehouse)-->-1:escalate:((^))
-1:escalate:((^))-->g3e:exclusivegateway:{x}
g3e:exclusivegateway:{x}-->g1s:exclusivegateway:{x}
g1e:exclusivegateway:{x}-->ee:endevent:((endevent))