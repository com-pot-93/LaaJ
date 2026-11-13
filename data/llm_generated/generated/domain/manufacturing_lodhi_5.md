flowchart LR
se:startevent:((startevent))-->a1:task:(Receive production order)
a1:task:(Receive production order)-->a3:task:(Prepare production order)
a3:task:(Prepare production order)-->e1s:exclusivegateway:{x}
e1e:exclusivegateway:{x}-->|"true"|e1s:exclusivegateway:{x}
e1s:exclusivegateway:{x}-->a7:task:(Collect raw materials)
a7:task:(Collect raw materials)-->a9:task:(Cutting)
a9:task:(Cutting)-->e2s:parallelgateway:{AND}
e2s:parallelgateway:{AND}-->a13:task:(Stitching)
a13:task:(Stitching)-->e2e:parallelgateway:{AND}
e2s:parallelgateway:{AND}-->a15:task:(Printing)
a15:task:(Printing)-->e2e:parallelgateway:{AND}
e2e:parallelgateway:{AND}-->a21:task:(Complete production)
a21:task:(Complete production)-->a23:task:(Check quality)
a23:task:(Check quality)-->a25:task:(Create quality report)
a25:task:(Create quality report)-->e5s:exclusivegateway:{x}
e5s:exclusivegateway:{x}-->a31:task:(Send data to warehouse)
a31:task:(Send data to warehouse)-->e5e:exclusivegateway:{x}
e5s:exclusivegateway:{x}-->|"|"|a29:task:(Adjust settings)
a29:task:(Adjust settings)-->e5e:exclusivegateway:{x}
e5e:exclusivegateway:{x}-->e1e:exclusivegateway:{x}
e1e:exclusivegateway:{x}-->ee:endevent:((endevent))