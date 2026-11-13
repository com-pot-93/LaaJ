flowchart LR
se:startevent:((startevent))-->a1:task:(Receive customer order)
a1:task:(Receive customer order)-->a3:task:(Processing customer demand)
a3:task:(Processing customer demand)-->a5:task:(Determine demanded components according to planning)
a5:task:(Determine demanded components according to planning)-->e1s:exclusivegateway:{x}
e1s:exclusivegateway:{x}-->|"Missing parts"|a9:task:(Purchase missing parts and put on stock)
a9:task:(Purchase missing parts and put on stock)-->e1e:exclusivegateway:{x}
e1s:exclusivegateway:{x}-->|"Parts available"|e1e:exclusivegateway:{x}
e1e:exclusivegateway:{x}-->a15:task:(Perform production)
a15:task:(Perform production)-->a17:task:(Perform quality checks)
a17:task:(Perform quality checks)-->e4s:exclusivegateway:{x}
e4s:exclusivegateway:{x}-->|"Quality failed"|a21:task:(Perform follow-up production)
a21:task:(Perform follow-up production)-->e4e:exclusivegateway:{x}
e4s:exclusivegateway:{x}-->|"Quality passed"|e4e:exclusivegateway:{x}
e4e:exclusivegateway:{x}-->a27:task:(Fill product into a packaging)
a27:task:(Fill product into a packaging)-->a29:task:(Pack and label product)
a29:task:(Pack and label product)-->a31:task:(Transport product to the warehouse)
a31:task:(Transport product to the warehouse)-->a33:task:(Send product to customer)
a33:task:(Send product to customer)-->ee:endevent:((endevent))