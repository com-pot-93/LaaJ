flowchart LR
se:startevent:((startevent))-->a1:task:(Diagnose Non-
Specific Low
Back Pain)
a1:task:(Diagnose Non-
Specific Low
Back Pain)-->g1s:exclusivegateway:{x}
g1s:exclusivegateway:{x}-->a3:task:(Apply
Superficial
Heat or other
Nonpharmocol.
Treatments)
a3:task:(Apply
Superficial
Heat or other
Nonpharmocol.
Treatments)-->g2s:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->a7:task:(Prescribe
NSAID or SMR)
a7:task:(Prescribe
NSAID or SMR)-->g2e:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->g2e:exclusivegateway:{x}
g2e:exclusivegateway:{x}-->g1e:exclusivegateway:{x}
g1s:exclusivegateway:{x}-->a4:task:(Apply Exercise
or other
Nonpharmacol.
Treatments)
a4:task:(Apply Exercise
or other
Nonpharmacol.
Treatments)-->g3s:exclusivegateway:{x}
g3s:exclusivegateway:{x}-->a10:task:(Prescribe
NSAID)
a10:task:(Prescribe
NSAID)-->g4s:exclusivegateway:{x}
g4s:exclusivegateway:{x}-->a14:task:(Prescribe
Opioid)
a14:task:(Prescribe
Opioid)-->g4e:exclusivegateway:{x}
g4s:exclusivegateway:{x}-->g4e:exclusivegateway:{x}
g4e:exclusivegateway:{x}-->g3e:exclusivegateway:{x}
g3s:exclusivegateway:{x}-->g3e:exclusivegateway:{x}
g3e:exclusivegateway:{x}-->g1e:exclusivegateway:{x}
g1e:exclusivegateway:{x}-->ee:endevent:((endevent))