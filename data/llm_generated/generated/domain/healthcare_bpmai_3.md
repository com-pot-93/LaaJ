flowchart LR
se:startevent:((startevent))-->a1:task:(Call to the hospital)
a1:task:(Call to the hospital)-->a3:task:(Decision about patient acceptance)
a3:task:(Decision about patient acceptance)-->e1s:exclusivegateway:{x}
e1s:exclusivegateway:{x}-->a7:task:(Add to list of patients)
a7:task:(Add to list of patients)-->a13:task:(Patient control)
a13:task:(Patient control)-->e3s:exclusivegateway:{x}
e3s:exclusivegateway:{x}-->e3e:exclusivegateway:{x}
e3e:exclusivegateway:{x}-->|"Loop"|a14:task:(Patient control)
a14:task:(Patient control)-->e3s:exclusivegateway:{x}
e3e:exclusivegateway:{x}-->a19:task:(Call patient to hospital)
a19:task:(Call patient to hospital)-->a21:task:(Patient hospitalization)
a21:task:(Patient hospitalization)-->a23:task:(Child birth)
a23:task:(Child birth)-->e4s:exclusivegateway:{x}
e4s:exclusivegateway:{x}-->|"Post-hospitalization"|a27:task:(Patient post-hospitalization)
a27:task:(Patient post-hospitalization)-->e4e:exclusivegateway:{x}
e4s:exclusivegateway:{x}-->|"Special case"|a29:task:(Special treatment)
a29:task:(Special treatment)-->e4e:exclusivegateway:{x}
e4e:exclusivegateway:{x}-->e1e:exclusivegateway:{x}
e1s:exclusivegateway:{x}-->|"Reject"|e1e:exclusivegateway:{x}
e1e:exclusivegateway:{x}-->ee:endevent:((endevent))