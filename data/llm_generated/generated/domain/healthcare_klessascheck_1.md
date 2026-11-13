flowchart LR
se:startevent:((startevent))-->a1:task:(Diagnose Non Specific Low Back Pain)
a1:task:(Diagnose Non Specific Low Back Pain)-->e1s:exclusivegateway:{x}
e1s:exclusivegateway:{x}-->|"Branch 1"|a5:task:(Apply Superficial Heat or other Nonpharmocol. Treatments)
a5:task:(Apply Superficial Heat or other Nonpharmocol. Treatments)-->e3s:exclusivegateway:{x}
e3s:exclusivegateway:{x}-->|"Prescribe"|a9:task:(Prescribe NSAID or SMR)
a9:task:(Prescribe NSAID or SMR)-->e3e:exclusivegateway:{x}
e3s:exclusivegateway:{x}-->|"No Prescription"|e3e:exclusivegateway:{x}
e3e:exclusivegateway:{x}-->e1e:exclusivegateway:{x}
e1s:exclusivegateway:{x}-->|"Branch 2"|a15:task:(Apply Exercise or other Nonpharmacol. Treatments)
a15:task:(Apply Exercise or other Nonpharmacol. Treatments)-->e7s:exclusivegateway:{x}
e7s:exclusivegateway:{x}-->|"No NSAID"|e7e:exclusivegateway:{x}
e7s:exclusivegateway:{x}-->|"|"|a19:task:(Prescribe NSAID)
a19:task:(Prescribe NSAID)-->e9s:exclusivegateway:{x}
e9s:exclusivegateway:{x}-->|"Prescribe Opioid"|a23:task:(Prescribe Opioid)
a23:task:(Prescribe Opioid)-->e9e:exclusivegateway:{x}
e9s:exclusivegateway:{x}-->|"No Opioid"|e9e:exclusivegateway:{x}
e9e:exclusivegateway:{x}-->e7e:exclusivegateway:{x}
e7e:exclusivegateway:{x}-->e1e:exclusivegateway:{x}
e1e:exclusivegateway:{x}-->ee:endevent:((endevent))