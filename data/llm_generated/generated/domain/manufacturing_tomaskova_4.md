flowchart LR
se:startevent:((startevent))-->e1s:exclusivegateway:{x}
e1s:exclusivegateway:{x}-->e1e:exclusivegateway:{x}
e1e:exclusivegateway:{x}-->|"true"|a3:task:(Production planning)
a3:task:(Production planning)-->a5:task:(Assign workers)
a5:task:(Assign workers)-->a7:task:(Production design)
a7:task:(Production design)-->a9:task:(Product delivery)
a9:task:(Product delivery)-->a11:task:(Production logout)
a11:task:(Production logout)-->a13:task:(Quality control)
a13:task:(Quality control)-->e1s:exclusivegateway:{x}
e1e:exclusivegateway:{x}-->e2s:exclusivegateway:{x}
e2s:exclusivegateway:{x}-->a25:task:(Register to the semi-finished stock)
a25:task:(Register to the semi-finished stock)-->a27:task:(Load to the semi-finished stock)
a27:task:(Load to the semi-finished stock)-->e2e:exclusivegateway:{x}
e2s:exclusivegateway:{x}-->|"|"|a19:task:(Register to the finished stock)
a19:task:(Register to the finished stock)-->a21:task:(Stock to the finished goods)
a21:task:(Stock to the finished goods)-->e2e:exclusivegateway:{x}
e2e:exclusivegateway:{x}-->ee:endevent:((endevent))