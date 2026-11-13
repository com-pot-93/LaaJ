flowchart LR
se:startevent:((startevent))-->e1s:parallelgateway:{AND}
e1s:parallelgateway:{AND}-->a3:task:(Add "profiling about logic involved, significance and envisaged consequences of processing")
a3:task:(Add "profiling about logic involved, significance and envisaged consequences of processing")-->e1e:parallelgateway:{AND}
e1s:parallelgateway:{AND}-->a5:task:(Check if it is possible to determine the period for which personal data will be stored)
a5:task:(Check if it is possible to determine the period for which personal data will be stored)-->e4s:exclusivegateway:{x}
e4s:exclusivegateway:{x}-->|"Yes"|a35:task:(Retrieve the criteria used to determine the period)
a35:task:(Retrieve the criteria used to determine the period)-->e4e:exclusivegateway:{x}
e4s:exclusivegateway:{x}-->|"No"|a37:task:(Retrieve the period)
a37:task:(Retrieve the period)-->e4e:exclusivegateway:{x}
e4e:exclusivegateway:{x}-->e1e:parallelgateway:{AND}
e1s:parallelgateway:{AND}-->a7:task:(Add "existence of the right to rectify of personal data")
a7:task:(Add "existence of the right to rectify of personal data")-->e1e:parallelgateway:{AND}
e1s:parallelgateway:{AND}-->a9:task:(Add "existence of the right to access personal data")
a9:task:(Add "existence of the right to access personal data")-->e1e:parallelgateway:{AND}
e1s:parallelgateway:{AND}-->a11:task:(Add "existence of the right to erase personal data")
a11:task:(Add "existence of the right to erase personal data")-->e1e:parallelgateway:{AND}
e1s:parallelgateway:{AND}-->a13:task:(Add "existence of the right to data portability")
a13:task:(Add "existence of the right to data portability")-->e1e:parallelgateway:{AND}
e1s:parallelgateway:{AND}-->a15:task:(Add "existence of the right to withdraw")
a15:task:(Add "existence of the right to withdraw")-->e1e:parallelgateway:{AND}
e1s:parallelgateway:{AND}-->a17:task:(Add "existence of the right to lodge a complaint to a supervisory authority")
a17:task:(Add "existence of the right to lodge a complaint to a supervisory authority")-->e1e:parallelgateway:{AND}
e1s:parallelgateway:{AND}-->a19:task:(Check if data has been obtained from Data Subject)
a19:task:(Check if data has been obtained from Data Subject)-->e14s:exclusivegateway:{x}
e14s:exclusivegateway:{x}-->|"Yes"|a45:task:(Retrieve the source from which personal data are originated)
a45:task:(Retrieve the source from which personal data are originated)-->e14e:exclusivegateway:{x}
e14s:exclusivegateway:{x}-->|"No"|a47:task:(Initialize empty source)
a47:task:(Initialize empty source)-->e14e:exclusivegateway:{x}
e14e:exclusivegateway:{x}-->e1e:parallelgateway:{AND}
e1s:parallelgateway:{AND}-->a21:task:(Check if personal data can be transferred internationally)
a21:task:(Check if personal data can be transferred internationally)-->e18s:exclusivegateway:{x}
e18s:exclusivegateway:{x}-->|"Yes"|a55:task:(Add "personal data will be transferred internationally")
a55:task:(Add "personal data will be transferred internationally")-->e18e:exclusivegateway:{x}
e18s:exclusivegateway:{x}-->|"No"|a57:task:(Initialize empty transfer info)
a57:task:(Initialize empty transfer info)-->e18e:exclusivegateway:{x}
e18e:exclusivegateway:{x}-->e1e:parallelgateway:{AND}
e1s:parallelgateway:{AND}-->a23:task:(Check if recipients are present)
a23:task:(Check if recipients are present)-->e22s:exclusivegateway:{x}
e22s:exclusivegateway:{x}-->|"Yes"|a65:task:(Retrieve recipients)
a65:task:(Retrieve recipients)-->e22e:exclusivegateway:{x}
e22s:exclusivegateway:{x}-->|"No"|a67:task:(Initialize empty recipients)
a67:task:(Initialize empty recipients)-->e22e:exclusivegateway:{x}
e22e:exclusivegateway:{x}-->e1e:parallelgateway:{AND}
e1s:parallelgateway:{AND}-->a25:task:(Check if legitimate interests are presents)
a25:task:(Check if legitimate interests are presents)-->e26s:exclusivegateway:{x}
e26s:exclusivegateway:{x}-->|"Yes"|a75:task:(Retrieve legitimate interests)
a75:task:(Retrieve legitimate interests)-->e26e:exclusivegateway:{x}
e26s:exclusivegateway:{x}-->|"No"|a77:task:(Initialize empty interests)
a77:task:(Initialize empty interests)-->e26e:exclusivegateway:{x}
e26e:exclusivegateway:{x}-->e1e:parallelgateway:{AND}
e1s:parallelgateway:{AND}-->a27:task:(Retrieve processing legal basis)
a27:task:(Retrieve processing legal basis)-->e1e:parallelgateway:{AND}
e1s:parallelgateway:{AND}-->a29:task:(Retrieve processing purposses)
a29:task:(Retrieve processing purposses)-->e1e:parallelgateway:{AND}
e1s:parallelgateway:{AND}-->e32s:parallelgateway:{AND}
e32s:parallelgateway:{AND}-->a83:task:(Retrieve identity and contact details)
a83:task:(Retrieve identity and contact details)-->e32e:parallelgateway:{AND}
e32s:parallelgateway:{AND}-->a85:task:(Ask DPO details)
a85:task:(Ask DPO details)-->a87:task:(Receive details From DPO)
a87:task:(Receive details From DPO)-->e32e:parallelgateway:{AND}
e32e:parallelgateway:{AND}-->e1e:parallelgateway:{AND}
e1e:parallelgateway:{AND}-->a123:task:(Collect consent information)
a123:task:(Collect consent information)-->a125:task:(Ask consent)
a125:task:(Ask consent)-->e35s:exclusivegateway:{x}
e35s:exclusivegateway:{x}-->|"Negation"|a129:task:(Receive negation)
a129:task:(Receive negation)-->e35e:exclusivegateway:{x}
e35s:exclusivegateway:{x}-->|"Consent"|a131:task:(Receive consent)
a131:task:(Receive consent)-->e35e:exclusivegateway:{x}
e35e:exclusivegateway:{x}-->ee:endevent:((endevent))