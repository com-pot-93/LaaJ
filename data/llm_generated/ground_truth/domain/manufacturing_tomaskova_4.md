flowchart LR
se:startevent:((startevent))-->g1s:exclusivegateway:{x}
g1e:exclusivegateway:{x}-->|"true"|g1s:exclusivegateway:{x}
g1s:exclusivegateway:{x}-->a1:task:(Production planning)
a1:task:(Production planning)-->a2:task:(Assign workers)
a2:task:(Assign workers)-->a3:task:(Production design)
a3:task:(Production design)-->a4:task:(Product delivery)
a4:task:(Product delivery)-->a5:task:(Production logout)
a5:task:(Production logout)-->a6:task:(Quality control)
a6:task:(Quality control)-->g1e:exclusivegateway:{x}
g1e:exclusivegateway:{x}-->g2s:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->a11:task:(Register to the finished stock)
a11:task:(Register to the finished stock)-->a13:task:(Stock to the finished goods)
a13:task:(Stock to the finished goods)-->g2e:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->a10:task:(Register to the semi-finished stock)
a10:task:(Register to the semi-finished stock)-->a12:task:(Load to the semi-finished stock)
a12:task:(Load to the semi-finished stock)-->g2e:exclusivegateway:{x}
g2e:exclusivegateway:{x}-->ee:endevent:((endevent))