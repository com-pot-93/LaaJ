flowchart LR
se:startevent:((startevent))-->a1:task:(Get temperature values)
a1:task:(Get temperature values)-->e1s:exclusivegateway:{x}
e1s:exclusivegateway:{x}-->|"Branch 1"|a5:task:(Generate standard notification)
a5:task:(Generate standard notification)-->e1e:exclusivegateway:{x}
e1s:exclusivegateway:{x}-->|"Branch 2"|e4s:parallelgateway:{AND}
e4s:parallelgateway:{AND}-->a9:task:(Get container status)
a9:task:(Get container status)-->a11:task:(Estimate container status)
a11:task:(Estimate container status)-->e6s:exclusivegateway:{x}
e6s:exclusivegateway:{x}-->|"Path A"|a15:task:(Generate container change request)
a15:task:(Generate container change request)-->e6e:exclusivegateway:{x}
e6s:exclusivegateway:{x}-->|"Path B"|a17:task:(Initialize container status)
a17:task:(Initialize container status)-->e6e:exclusivegateway:{x}
e6e:exclusivegateway:{x}-->e4e:parallelgateway:{AND}
e4s:parallelgateway:{AND}-->a23:task:(Get client location)
a23:task:(Get client location)-->a25:task:(Estimate distance)
a25:task:(Estimate distance)-->e10s:exclusivegateway:{x}
e10s:exclusivegateway:{x}-->|"Skip"|a31:task:(Initialize delivery time)
a31:task:(Initialize delivery time)-->e10e:exclusivegateway:{x}
e10s:exclusivegateway:{x}-->|"|"|a29:task:(Estimate delivery time)
a29:task:(Estimate delivery time)-->e12s:exclusivegateway:{x}
e12s:exclusivegateway:{x}-->|"Path A"|a35:task:(Generate route change request)
a35:task:(Generate route change request)-->e12e:exclusivegateway:{x}
e12s:exclusivegateway:{x}-->|"Path B"|a37:task:(Initialize route change)
a37:task:(Initialize route change)-->e12e:exclusivegateway:{x}
e12e:exclusivegateway:{x}-->e10e:exclusivegateway:{x}
e10e:exclusivegateway:{x}-->e4e:parallelgateway:{AND}
e4s:parallelgateway:{AND}-->a45:task:(Get goods status)
a45:task:(Get goods status)-->a47:task:(Estimate goods status)
a47:task:(Estimate goods status)-->e17s:exclusivegateway:{x}
e17s:exclusivegateway:{x}-->|"Skip"|a53:task:(Initialize damages)
a53:task:(Initialize damages)-->e17e:exclusivegateway:{x}
e17s:exclusivegateway:{x}-->|"|"|a51:task:(Evaluate damages)
a51:task:(Evaluate damages)-->e19s:exclusivegateway:{x}
e19s:exclusivegateway:{x}-->|"Path A"|a57:task:(Generate removal request)
a57:task:(Generate removal request)-->e19e:exclusivegateway:{x}
e19s:exclusivegateway:{x}-->|"Path B"|a59:task:(Generate price change request)
a59:task:(Generate price change request)-->e19e:exclusivegateway:{x}
e19e:exclusivegateway:{x}-->e17e:exclusivegateway:{x}
e17e:exclusivegateway:{x}-->e4e:parallelgateway:{AND}
e4e:parallelgateway:{AND}-->e1e:exclusivegateway:{x}
e1e:exclusivegateway:{x}-->a77:task:(Send generated messages)
a77:task:(Send generated messages)-->ee:endevent:((endevent))