flowchart LR
se:startevent:((startevent))-->a1:task:(Come to the hospital)
a1:task:(Come to the hospital)-->a3:task:(Stay the front)
a3:task:(Stay the front)-->a5:task:(Visit the nurse)
a5:task:(Visit the nurse)-->a7:task:(Check insurance)
a7:task:(Check insurance)-->e1s:exclusivegateway:{x}
e1s:exclusivegateway:{x}-->|"Branch 1"|a11:task:(Check patients state)
a11:task:(Check patients state)-->e3s:exclusivegateway:{x}
e3s:exclusivegateway:{x}-->|"Branch 1"|a15:task:(Send patient home)
a15:task:(Send patient home)-->e3e:exclusivegateway:{x}
e3s:exclusivegateway:{x}-->|"Branch 2"|a19:task:(Examine the patient)
a19:task:(Examine the patient)-->e6s:exclusivegateway:{x}
e6s:exclusivegateway:{x}-->|"Branch 1"|a23:task:(Hospitalize)
a23:task:(Hospitalize)-->a25:task:(Book patient for doctor)
a25:task:(Book patient for doctor)-->e6e:exclusivegateway:{x}
e6s:exclusivegateway:{x}-->|"Branch 2"|a29:task:(Send patient to pharmacy)
a29:task:(Send patient to pharmacy)-->a31:task:(Visit pharmacy)
a31:task:(Visit pharmacy)-->a33:task:(Order medicine)
a33:task:(Order medicine)-->a35:task:(Pay medicine)
a35:task:(Pay medicine)-->a37:task:(Receive medicine)
a37:task:(Receive medicine)-->e6e:exclusivegateway:{x}
e6s:exclusivegateway:{x}-->|"Branch 3"|a41:task:(Send patient home)
a41:task:(Send patient home)-->e6e:exclusivegateway:{x}
e6e:exclusivegateway:{x}-->e3e:exclusivegateway:{x}
e3e:exclusivegateway:{x}-->e1e:exclusivegateway:{x}
e1s:exclusivegateway:{x}-->a51:task:(Check if patient is registered in hospital)
a51:task:(Check if patient is registered in hospital)-->e11s:exclusivegateway:{x}
e11s:exclusivegateway:{x}-->|"Branch 1"|a55:task:(Register patient)
a55:task:(Register patient)-->e11e:exclusivegateway:{x}
e11s:exclusivegateway:{x}-->|"Branch 2"|e11e:exclusivegateway:{x}
e11e:exclusivegateway:{x}-->a61:task:(Pay fee)
a61:task:(Pay fee)-->e14s:exclusivegateway:{x}
e14s:exclusivegateway:{x}-->e14e:exclusivegateway:{x}
e14e:exclusivegateway:{x}-->|"true"|a65:task:(Book patient for doctor)
a65:task:(Book patient for doctor)-->a67:task:(Examine the patient)
a67:task:(Examine the patient)-->e15s:exclusivegateway:{x}
e15s:exclusivegateway:{x}-->|"Branch 1"|a71:task:(Hospitalize)
a71:task:(Hospitalize)-->e15e:exclusivegateway:{x}
e15s:exclusivegateway:{x}-->|"Branch 2"|a75:task:(Send patient to pharmacy)
a75:task:(Send patient to pharmacy)-->a77:task:(Visit pharmacy)
a77:task:(Visit pharmacy)-->a79:task:(Order medicine)
a79:task:(Order medicine)-->a81:task:(Pay medicine)
a81:task:(Pay medicine)-->a83:task:(Receive medicine)
a83:task:(Receive medicine)-->e15e:exclusivegateway:{x}
e15s:exclusivegateway:{x}-->|"Branch 3"|a87:task:(Send patient home)
a87:task:(Send patient home)-->e15e:exclusivegateway:{x}
e15e:exclusivegateway:{x}-->e14s:exclusivegateway:{x}
e14e:exclusivegateway:{x}-->e1e:exclusivegateway:{x}
e1e:exclusivegateway:{x}-->ee:endevent:((endevent))