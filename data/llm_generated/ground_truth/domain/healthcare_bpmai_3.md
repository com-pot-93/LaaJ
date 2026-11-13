flowchart LR
se:startevent:((startevent))-->a1:task:(Call to the hospital)
a1:task:(Call to the hospital)-->a2:task:(Decision about patient acceptance)
a2:task:(Decision about patient acceptance)-->g1s:exclusivegateway:{x}
g1s:exclusivegateway:{x}-->|"true"|a13:task:(Add to list of patients)
a13:task:(Add to list of patients)-->g2s:exclusivegateway:{x}
g2e:exclusivegateway:{x}-->|"true"|g2s:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->a4:task:(Patient control)
a4:task:(Patient control)-->g2e:exclusivegateway:{x}
g2e:exclusivegateway:{x}-->a14:task:(Call patient to hospital)
a14:task:(Call patient to hospital)-->a15:task:(Patient hospitalization)
a15:task:(Patient hospitalization)-->a6:task:(Child birth)
a6:task:(Child birth)-->g3s:exclusivegateway:{x}
g3s:exclusivegateway:{x}-->a16:task:(Patient post-hospitalization)
a16:task:(Patient post-hospitalization)-->g3e:exclusivegateway:{x}
g3s:exclusivegateway:{x}-->a8:task:(Special treatment)
a8:task:(Special treatment)-->g3e:exclusivegateway:{x}
g3e:exclusivegateway:{x}-->g1e:exclusivegateway:{x}
g1s:exclusivegateway:{x}-->g1e:exclusivegateway:{x}
g1e:exclusivegateway:{x}-->ee:endevent:((endevent))