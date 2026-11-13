flowchart LR
se:startevent:((startevent))-->a1:task:(Get temperature values)
a1:task:(Get temperature values)-->g1s:exclusivegateway:{x}
g1s:exclusivegateway:{x}-->a4:task:(Generate standard notification)
a4:task:(Generate standard notification)-->g1e:exclusivegateway:{x}
g1s:exclusivegateway:{x}-->g2s:parallelgateway:{AND}
g2s:parallelgateway:{AND}-->a5:task:(Get container status)
a5:task:(Get container status)-->a9:task:(Estimate container status)
a9:task:(Estimate container status)-->g3s:exclusivegateway:{x}
g3s:exclusivegateway:{x}-->g3e:exclusivegateway:{x}
g3s:exclusivegateway:{x}-->a7:task:(Generate container change request)
a7:task:(Generate container change request)-->g3e:exclusivegateway:{x}
g3e:exclusivegateway:{x}-->g2e:parallelgateway:{AND}
g2s:parallelgateway:{AND}-->a11:task:(Get client location)
a11:task:(Get client location)-->a16:task:(Estimate distance)
a16:task:(Estimate distance)-->g4s:exclusivegateway:{x}
g4s:exclusivegateway:{x}-->a12:task:(Estimate delivery time)
a12:task:(Estimate delivery time)-->g5s:exclusivegateway:{x}
g5s:exclusivegateway:{x}-->g5e:exclusivegateway:{x}
g5s:exclusivegateway:{x}-->a15:task:(Generate route change request)
a15:task:(Generate route change request)-->g5e:exclusivegateway:{x}
g5e:exclusivegateway:{x}-->g4e:exclusivegateway:{x}
g4s:exclusivegateway:{x}-->g4e:exclusivegateway:{x}
g4e:exclusivegateway:{x}-->g2e:parallelgateway:{AND}
g2s:parallelgateway:{AND}-->a19:task:(Get goods status)
a19:task:(Get goods status)-->a20:task:(Estimate goods status)
a20:task:(Estimate goods status)-->g6s:exclusivegateway:{x}
g6s:exclusivegateway:{x}-->a23:task:(Evaluate damages)
a23:task:(Evaluate damages)-->g7s:exclusivegateway:{x}
g7s:exclusivegateway:{x}-->a25:task:(Generate removal request)
a25:task:(Generate removal request)-->g7e:exclusivegateway:{x}
g7s:exclusivegateway:{x}-->a26:task:(Generate price change request)
a26:task:(Generate price change request)-->g7e:exclusivegateway:{x}
g7e:exclusivegateway:{x}-->g6e:exclusivegateway:{x}
g6s:exclusivegateway:{x}-->g6e:exclusivegateway:{x}
g6e:exclusivegateway:{x}-->g2e:parallelgateway:{AND}
g2e:parallelgateway:{AND}-->g1e:exclusivegateway:{x}
g1e:exclusivegateway:{x}-->a28:task:(Send generated messages)
a28:task:(Send generated messages)-->ee:endevent:((endevent))