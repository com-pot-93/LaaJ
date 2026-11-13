flowchart LR
se:startevent:((startevent))-->a11:task:(Receive shipment request)
a11:task:(Receive shipment request)-->a10:task:(Check product availability)
a10:task:(Check product availability)-->g1s:exclusivegateway:{x}
g1s:exclusivegateway:{x}-->a12:task:(Check shipment address)
a12:task:(Check shipment address)-->g2s:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->a7:task:(Assemble inbound shipment)
a7:task:(Assemble inbound shipment)-->a8:task:(Send inbound shipment)
a8:task:(Send inbound shipment)-->a1:task:(Receive inbound
 shipment)
a1:task:(Receive inbound
 shipment)-->a2:task:(Check inbound
 shipment)
a2:task:(Check inbound
 shipment)-->a3:task:(Prepare products for   shipment 
to particular service station)
a3:task:(Prepare products for   shipment 
to particular service station)-->g2e:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->a13:task:(Prepare products for regional  shipment)
a13:task:(Prepare products for regional  shipment)-->g2e:exclusivegateway:{x}
g2e:exclusivegateway:{x}-->g1e:exclusivegateway:{x}
g1s:exclusivegateway:{x}-->a4:task:(Prepare products for   shipment 
to particular service station)
a4:task:(Prepare products for   shipment 
to particular service station)-->g1e:exclusivegateway:{x}
g1e:exclusivegateway:{x}-->ee:endevent:((endevent))