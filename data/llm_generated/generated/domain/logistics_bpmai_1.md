flowchart LR
se:startevent:((startevent))-->a1:task:(Receive shipment request)
a1:task:(Receive shipment request)-->a3:task:(Check product availability)
a3:task:(Check product availability)-->e1s:exclusivegateway:{x}
e1s:exclusivegateway:{x}-->|"Direct"|a20:task:(Prepare products for shipment to particular service station)
a20:task:(Prepare products for shipment to particular service station)-->e1e:exclusivegateway:{x}
e1s:exclusivegateway:{x}-->|"|"|a7:task:(Check shipment address)
a7:task:(Check shipment address)-->e3s:exclusivegateway:{x}
e3s:exclusivegateway:{x}-->|"Assemble"|a11:task:(Assemble inbound shipment)
a11:task:(Assemble inbound shipment)-->a13:task:(Send inbound shipment)
a13:task:(Send inbound shipment)-->a15:task:(Receive inbound shipment)
a15:task:(Receive inbound shipment)-->a17:task:(Check inbound shipment)
a17:task:(Check inbound shipment)-->a19:task:(Prepare products for shipment to particular service station)
a19:task:(Prepare products for shipment to particular service station)-->e3e:exclusivegateway:{x}
e3s:exclusivegateway:{x}-->|"Regional"|a21:task:(Prepare products for regional shipment)
a21:task:(Prepare products for regional shipment)-->e3e:exclusivegateway:{x}
e3e:exclusivegateway:{x}-->e1e:exclusivegateway:{x}
e1e:exclusivegateway:{x}-->ee:endevent:((endevent))