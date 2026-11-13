flowchart LR
se:startevent:((startevent))-->g1s:parallelgateway:{AND}
g1s:parallelgateway:{AND}-->a2:task:(Add "profiling about logic involved, significance and envisaged consequences of processing")
a2:task:(Add "profiling about logic involved, significance and envisaged consequences of processing")-->g1e:parallelgateway:{AND}
g1s:parallelgateway:{AND}-->a4:task:(Check if it is possible to determine the period for which personal data will be stored)
a4:task:(Check if it is possible to determine the period for which personal data will be stored)-->g2s:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->a7:task:(Retrieve the period)
a7:task:(Retrieve the period)-->g2e:exclusivegateway:{x}
g2s:exclusivegateway:{x}-->|"|"|a6:task:(Retrieve the criteria used to determine the period)
a6:task:(Retrieve the criteria used to determine the period)-->g2e:exclusivegateway:{x}
g2e:exclusivegateway:{x}-->g1e:parallelgateway:{AND}
g1s:parallelgateway:{AND}-->a9:task:(Add "existence of the right to rectify of personal data")
a9:task:(Add "existence of the right to rectify of personal data")-->g1e:parallelgateway:{AND}
g1s:parallelgateway:{AND}-->a10:task:(Add "existence of the right to access personal data")
a10:task:(Add "existence of the right to access personal data")-->g1e:parallelgateway:{AND}
g1s:parallelgateway:{AND}-->a11:task:(Add "existence of the right to erase personal data")
a11:task:(Add "existence of the right to erase personal data")-->g1e:parallelgateway:{AND}
g1s:parallelgateway:{AND}-->a12:task:(Add "existence of the right to data portability")
a12:task:(Add "existence of the right to data portability")-->g1e:parallelgateway:{AND}
g1s:parallelgateway:{AND}-->a13:task:(Add "existence of the right to withdraw")
a13:task:(Add "existence of the right to withdraw")-->g1e:parallelgateway:{AND}
g1s:parallelgateway:{AND}-->a14:task:(Add "existence of the right to lodge a complaint to a supervisory authority")
a14:task:(Add "existence of the right to lodge a complaint to a supervisory authority")-->g1e:parallelgateway:{AND}
g1s:parallelgateway:{AND}-->a15:task:(Check if data has been obtained from Data Subject)
a15:task:(Check if data has been obtained from Data Subject)-->g3s:exclusivegateway:{x}
g3s:exclusivegateway:{x}-->g3e:exclusivegateway:{x}
g3s:exclusivegateway:{x}-->|"|"|a17:task:(Retrieve the source from which personal data are originated)
a17:task:(Retrieve the source from which personal data are originated)-->g3e:exclusivegateway:{x}
g3e:exclusivegateway:{x}-->g1e:parallelgateway:{AND}
g1s:parallelgateway:{AND}-->a19:task:(Check if personal data can be transferred internationally)
a19:task:(Check if personal data can be transferred internationally)-->g4s:exclusivegateway:{x}
g4s:exclusivegateway:{x}-->g4e:exclusivegateway:{x}
g4s:exclusivegateway:{x}-->|"|"|a21:task:(Add "personal data will be transferred internationally")
a21:task:(Add "personal data will be transferred internationally")-->g4e:exclusivegateway:{x}
g4e:exclusivegateway:{x}-->g1e:parallelgateway:{AND}
g1s:parallelgateway:{AND}-->a23:task:(Check if recipients are present)
a23:task:(Check if recipients are present)-->g5s:exclusivegateway:{x}
g5s:exclusivegateway:{x}-->g5e:exclusivegateway:{x}
g5s:exclusivegateway:{x}-->|"|"|a25:task:(Retrieve recipients)
a25:task:(Retrieve recipients)-->g5e:exclusivegateway:{x}
g5e:exclusivegateway:{x}-->g1e:parallelgateway:{AND}
g1s:parallelgateway:{AND}-->a27:task:(Check if legitimate interests are presents)
a27:task:(Check if legitimate interests are presents)-->g6s:exclusivegateway:{x}
g6s:exclusivegateway:{x}-->g6e:exclusivegateway:{x}
g6s:exclusivegateway:{x}-->|"|"|a29:task:(Retrieve legitimate interests)
a29:task:(Retrieve legitimate interests)-->g6e:exclusivegateway:{x}
g6e:exclusivegateway:{x}-->g1e:parallelgateway:{AND}
g1s:parallelgateway:{AND}-->a31:task:(Retrieve processing legal basis)
a31:task:(Retrieve processing legal basis)-->g1e:parallelgateway:{AND}
g1s:parallelgateway:{AND}-->a32:task:(Retrieve processing purposses)
a32:task:(Retrieve processing purposses)-->g1e:parallelgateway:{AND}
g1s:parallelgateway:{AND}-->g7s:parallelgateway:{AND}
g7s:parallelgateway:{AND}-->a33:task:(Retrieve identity and contact details)
a33:task:(Retrieve identity and contact details)-->g7e:parallelgateway:{AND}
g7s:parallelgateway:{AND}-->a35:task:(Ask DPO details)
a35:task:(Ask DPO details)-->a38:task:(Receive details From DPO)
a38:task:(Receive details From DPO)-->g7e:parallelgateway:{AND}
g7e:parallelgateway:{AND}-->g1e:parallelgateway:{AND}
g1e:parallelgateway:{AND}-->a39:task:(Collect consent information)
a39:task:(Collect consent information)-->a37:task:(Ask consent)
a37:task:(Ask consent)-->g8s:exclusivegateway:{x}
g8s:exclusivegateway:{x}-->a40:task:(Receive consent)
a40:task:(Receive consent)-->g8e:exclusivegateway:{x}
g8s:exclusivegateway:{x}-->|"|"|a41:task:(Receive negation)
a41:task:(Receive negation)-->g8e:exclusivegateway:{x}
g8e:exclusivegateway:{x}-->ee:endevent:((endevent))