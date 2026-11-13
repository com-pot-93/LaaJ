flowchart LR
se:startevent:((startevent))-->a1:task:(Receive customer order)
a1:task:(Receive customer order)-->a3:task:(Pick stock items)
a3:task:(Pick stock items)-->a5:task:(Pack items into parcels)
a5:task:(Pack items into parcels)-->a7:task:(Weight parcels)
a7:task:(Weight parcels)-->a9:task:(Print shipping labels)
a9:task:(Print shipping labels)-->e1s:parallelgateway:{AND}
e1s:parallelgateway:{AND}-->a13:task:(Move parcels to loading dock)
a13:task:(Move parcels to loading dock)-->e1e:parallelgateway:{AND}
e1s:parallelgateway:{AND}-->a15:task:(Check parcel count)
a15:task:(Check parcel count)-->e1e:parallelgateway:{AND}
e1s:parallelgateway:{AND}-->a17:task:(inspect packing quality)
a17:task:(inspect packing quality)-->e1e:parallelgateway:{AND}
e1e:parallelgateway:{AND}-->e5s:parallelgateway:{AND}
e5s:parallelgateway:{AND}-->a27:task:(Load parcels on truck)
a27:task:(Load parcels on truck)-->a31:task:(Send delivery instructions to transporter)
a31:task:(Send delivery instructions to transporter)-->e5e:parallelgateway:{AND}
e5s:parallelgateway:{AND}-->a29:task:(Update order status)
a29:task:(Update order status)-->a35:task:(Update stock levels)
a35:task:(Update stock levels)-->e5e:parallelgateway:{AND}
e5e:parallelgateway:{AND}-->ee:endevent:((endevent))