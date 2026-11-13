flowchart LR
se:startevent:((startevent))-->a19:task:(Come to the hospital)
a19:task:(Come to the hospital)-->a22:task:(Stay the front)
a22:task:(Stay the front)-->a24:task:(Visit the nurse)
a24:task:(Visit the nurse)-->a7:task:(Check insurance)
a7:task:(Check insurance)-->g1s:exclusivegateway:{x}
g1s:exclusivegateway:{x}-->a1:task:(Check patients state)
a1:task:(Check patients state)-->g2s:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->a3:task:(Send patient home)
a3:task:(Send patient home)-->g2e:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->g3s:exclusivegateway:{x}
g3s:exclusivegateway:{x}-->g3e:exclusivegateway:{x}
g3e:exclusivegateway:{x}-->|"true"|a18:task:(Examine the patient)
a18:task:(Examine the patient)-->g4s:exclusivegateway:{x}
g4s:exclusivegateway:{x}-->a15:task:(Hospitalize)
a15:task:(Hospitalize)-->a10:task:(Book patient for doctor)
a10:task:(Book patient for doctor)-->g4e:exclusivegateway:{x}
g4s:exclusivegateway:{x}-->a12:task:(Send patient to pharmacy)
a12:task:(Send patient to pharmacy)-->a23:task:(Visit pharmacy)
a23:task:(Visit pharmacy)-->a26:task:(Order medicine)
a26:task:(Order medicine)-->a27:task:(Pay medicine)
a27:task:(Pay medicine)-->a25:task:(Receive medicine)
a25:task:(Receive medicine)-->-1:escalate:((^))
-1:escalate:((^))-->g4e:exclusivegateway:{x}
g4s:exclusivegateway:{x}-->a13:task:(Send patient home)
a13:task:(Send patient home)-->-1:escalate:((^))
-1:escalate:((^))-->g4e:exclusivegateway:{x}
g4e:exclusivegateway:{x}-->g3s:exclusivegateway:{x}
g3e:exclusivegateway:{x}-->g2e:exclusivegateway:{x}
g2e:exclusivegateway:{x}-->g1e:exclusivegateway:{x}
g1s:exclusivegateway:{x}-->a4:task:(Check if patient is registered in hospital)
a4:task:(Check if patient is registered in hospital)-->g7s:exclusivegateway:{x}
g7s:exclusivegateway:{x}-->a5:task:(Register patient)
a5:task:(Register patient)-->g7e:exclusivegateway:{x}
g7s:exclusivegateway:{x}-->g7e:exclusivegateway:{x}
g7e:exclusivegateway:{x}-->a21:task:(Pay fee)
a21:task:(Pay fee)-->g8s:exclusivegateway:{x}
g8s:exclusivegateway:{x}-->g8e:exclusivegateway:{x}
g8e:exclusivegateway:{x}-->|"true"|a11:task:(Book patient for doctor)
a11:task:(Book patient for doctor)-->a20:task:(Examine the patient)
a20:task:(Examine the patient)-->g9s:exclusivegateway:{x}
g9s:exclusivegateway:{x}-->a16:task:(Hospitalize)
a16:task:(Hospitalize)-->g9e:exclusivegateway:{x}
g9s:exclusivegateway:{x}-->a14:task:(Send patient to pharmacy)
a14:task:(Send patient to pharmacy)-->a28:task:(Visit pharmacy)
a28:task:(Visit pharmacy)-->a29:task:(Order medicine)
a29:task:(Order medicine)-->a30:task:(Pay medicine)
a30:task:(Pay medicine)-->a31:task:(Receive medicine)
a31:task:(Receive medicine)-->-1:escalate:((^))
-1:escalate:((^))-->g9e:exclusivegateway:{x}
g9s:exclusivegateway:{x}-->a17:task:(Send patient home)
a17:task:(Send patient home)-->-1:escalate:((^))
-1:escalate:((^))-->g9e:exclusivegateway:{x}
g9e:exclusivegateway:{x}-->g8s:exclusivegateway:{x}
g8e:exclusivegateway:{x}-->g1e:exclusivegateway:{x}
g1e:exclusivegateway:{x}-->ee:endevent:((endevent))