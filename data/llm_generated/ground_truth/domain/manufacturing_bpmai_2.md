flowchart LR
se:startevent:((startevent))-->a2:task:(Receive customer order)
a2:task:(Receive customer order)-->a1:task:(Processing customer demand)
a1:task:(Processing customer demand)-->a5:task:(Determine demanded components according to planning)
a5:task:(Determine demanded components according to planning)-->g1s:exclusivegateway:{x}
g1s:exclusivegateway:{x}-->a8:task:(Purchase missing parts and put on stock)
a8:task:(Purchase missing parts and put on stock)-->g1e:exclusivegateway:{x}
g1s:exclusivegateway:{x}-->g1e:exclusivegateway:{x}
g1e:exclusivegateway:{x}-->a9:task:(Perform production)
a9:task:(Perform production)-->a10:task:(Perform 
quality checks)
a10:task:(Perform 
quality checks)-->g2s:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->g2e:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->a15:task:(Perform follow-up production)
a15:task:(Perform follow-up production)-->g2e:exclusivegateway:{x}
g2e:exclusivegateway:{x}-->a12:task:(Fill product 
into a 
packaging)
a12:task:(Fill product 
into a 
packaging)-->a13:task:(Pack and label product)
a13:task:(Pack and label product)-->a14:task:(Transport product to the warehouse)
a14:task:(Transport product to the warehouse)-->a3:task:(Send product to customer)
a3:task:(Send product to customer)-->ee:endevent:((endevent))