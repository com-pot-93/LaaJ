flowchart LR
se:startevent:((startevent))-->a1:task:(Receive customer order)
a1:task:(Receive customer order)-->a2:task:(Pick stock items)
a2:task:(Pick stock items)-->a3:task:(Pack items into parcels)
a3:task:(Pack items into parcels)-->a4:task:(Weight parcels)
a4:task:(Weight parcels)-->a5:task:(Print shipping labels)
a5:task:(Print shipping labels)-->g1s:parallelgateway:{AND}
g1s:parallelgateway:{AND}-->a7:task:(Move parcels to loading dock)
a7:task:(Move parcels to loading dock)-->g1e:parallelgateway:{AND}
g1s:parallelgateway:{AND}-->a8:task:(Check parcel count)
a8:task:(Check parcel count)-->g1e:parallelgateway:{AND}
g1s:parallelgateway:{AND}-->a10:task:(inspect packing quality)
a10:task:(inspect packing quality)-->g1e:parallelgateway:{AND}
g1e:parallelgateway:{AND}-->g2s:parallelgateway:{AND}
g2s:parallelgateway:{AND}-->a12:task:(Load parcels on truck)
a12:task:(Load parcels on truck)-->a13:task:(Send delivery instructions to transporter)
a13:task:(Send delivery instructions to transporter)-->g2e:parallelgateway:{AND}
g2s:parallelgateway:{AND}-->a14:task:(Update order status)
a14:task:(Update order status)-->a15:task:(Update stock levels)
a15:task:(Update stock levels)-->g2e:parallelgateway:{AND}
g2e:parallelgateway:{AND}-->ee:endevent:((endevent))