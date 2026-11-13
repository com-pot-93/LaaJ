import xml.etree.ElementTree as ET
import itertools

NAMESPACES = {'ns0': 'http://cpee.org/ns/description/1.0'}


def convert_cpee_json(xml_file):
    """Converts a cpee process model (xml file) into json. Returns the json as dict, or {"error": ...} if there is no model."""
    template = {
        "tasks":[],
        "events":[{ "id": "e", "name": "", "type": "EndNoneEvent" }, { "id": "s", "name": "", "type": "StartNoneEvent"}],
        "gateways":[],
        "pools":[],
        "sequenceFlows":[],
        "messageFlows":[]
    }

    general = []
    gcounter = 1
    pre = "s"
    flow_ids = itertools.count(1)    # unique sequence flow ids f1, f2, ...
    escape_ids = itertools.count(1)  # unique escape event ids esc1, esc2, ...

    def add_task(tag,element,eid):
        label = "task"
        if tag == "manipulate":
            label = element.get('label')
        elif tag == "stop":
            label = tag
        else:
            label_elems = element.findall('.//ns0:label', NAMESPACES)
            if label_elems and label_elems[0].text:  # calls without label keep "task"
                label = label_elems[0].text
        task = {'id': eid,'name': label,'type':'Task'}
        return task

    def add_sequence_flow(source,target):
        flow = {"id": "f{}".format(next(flow_ids)), "sourceRef":source, "targetRef":target}
        return flow

    def calculate(pre,gcounter,general,data):
        for element in data:
            eid = 0
            tag = element.tag.split("}")[1]
            if tag == "call" or tag == "manipulate" or tag == "stop":
                eid = element.attrib["id"]
                pair = "{}-->{}".format(pre,eid)
                if pair not in general:
                    general.append(pair)
                    flow = add_sequence_flow(pre,eid)
                    template["sequenceFlows"].append(flow)
                existing_ids = {task["id"] for task in template["tasks"]}
                if eid not in existing_ids:
                    task = add_task(tag,element,eid)
                    template["tasks"].append(task)
                pre = eid
            elif tag == "escape":
                eid = "esc{}".format(next(escape_ids))
                pair = "{}-->{}".format(pre,eid)
                if pair not in general:
                    general.append(pair)
                    flow = add_sequence_flow(pre,eid)
                    template["sequenceFlows"].append(flow)
                event = {'id': eid,'name': tag,'type':'IntermediateEscalationEventThrowing'}
                template["events"].append(event)
                pre = eid
            elif tag == "_probability":
                    continue
            else:
                last_list = []
                eid = "g" + str(gcounter)
                gcounter = gcounter + 1
                if tag == "choose" or tag == "parallel":
                    if tag == "choose":
                        mytype = element.attrib["mode"]
                        if mytype == "exclusive":
                            gateway = {'id': eid,'type':'Exclusive'}
                            template["gateways"].append(gateway)
                        elif mytype == "inclusive":
                            eid = eid.replace("g", "i")
                            gateway = {'id': eid,'type':'Inclusive'}
                            template["gateways"].append(gateway)
                    elif tag == "parallel":
                        eid = eid.replace("g", "p")
                        mytype = tag
                        gateway = {'id': eid,'type':'Parallel'}
                        template["gateways"].append(gateway)

                    pair = "{}-->{}".format(pre,eid)
                    if pair not in general:
                        general.append(pair)
                        flow = add_sequence_flow(pre,eid)
                        template["sequenceFlows"].append(flow)
                    pre = eid
                    for e in element:
                        eid,new_gcounter = calculate(pre,gcounter,general,e)
                        gcounter = new_gcounter
                        last_list.append(eid)
                    for l in last_list:
                        pair = "{}-->{}{}".format(l,"m",pre)
                        if pair not in general:
                            general.append(pair)
                            flow = add_sequence_flow(l,"m"+pre)
                            template["sequenceFlows"].append(flow)
                    pre = "{}{}".format("m",pre)
                    if "p" in pre:
                        gateway = {'id': pre,'type':'Parallel'}
                        template["gateways"].append(gateway)
                    elif "i" in pre:
                        gateway = {'id': pre,'type':'Inclusive'}
                        template["gateways"].append(gateway)
                    else:
                        gateway = {'id': pre,'type':'Exclusive'}
                        template["gateways"].append(gateway)
                elif tag == "loop":
                    mytype = element.attrib["mode"]
                    if mytype == "pre_test":
                        end = eid

                        pair = "{}-->{}".format(pre,eid)
                        if pair not in general:
                            general.append(pair)
                            flow = add_sequence_flow(pre,eid)
                            template["sequenceFlows"].append(flow)
                        pre = eid
                        pair = "{}-->{}{}".format(pre,"m",pre)
                        if pair not in general:
                            general.append(pair)
                            flow = add_sequence_flow(pre,"m"+pre)
                            template["sequenceFlows"].append(flow)
                        #------------------------
                        gateway = {'id': pre,'type':'Exclusive'}
                        template["gateways"].append(gateway)
                        gateway = {'id': "m"+pre,'type':'Exclusive'}
                        template["gateways"].append(gateway)
                        #---------------------------------
                        pre = "m"+pre
                        eid,new_gcounter = calculate(pre,gcounter,general,element)
                        pair = "{}-->{}".format(eid,end)
                        if pair not in general:
                            general.append(pair)
                            flow = add_sequence_flow(eid,end)
                            template["sequenceFlows"].append(flow)
                        gcounter = new_gcounter
                    elif mytype == "post_test":
                        pair = "{}-->{}".format(pre,eid)
                        if pair not in general:
                            general.append(pair)
                            flow = add_sequence_flow(pre,eid)
                            template["sequenceFlows"].append(flow)
                        pre = eid
                        eid,new_gcounter = calculate(pre,gcounter,general,element)
                        pair = "{}-->{}{}".format(eid,"m",pre)
                        if pair not in general:
                            general.append(pair)
                            flow = add_sequence_flow(eid,"m"+pre)
                            template["sequenceFlows"].append(flow)
                        pair = "{}{}-->{}".format('m',pre,pre)
                        if pair not in general:
                            general.append(pair)
                            flow = add_sequence_flow("m"+pre,pre)
                            template["sequenceFlows"].append(flow)
                        #------------------------
                        gateway = {'id': pre,'type':'Exclusive'}
                        template["gateways"].append(gateway)
                        gateway = {'id': "m"+pre,'type':'Exclusive'}
                        template["gateways"].append(gateway)
                        #---------------------------------
                        pre = "{}{}".format("m",pre)
                        gcounter = new_gcounter
        return pre,gcounter

    try:
        root = ET.parse(xml_file).getroot()
    except (ET.ParseError, OSError):
        print("The XML file {} is not well-formed or completely empty.".format(xml_file))
        return {"error":"no model is provided"}

    if len(root) == 0:
        return {"error":"no description is provided"}

    last,new_gcounter = calculate(pre,gcounter,general,root)
    general.append("{}-->{}".format(last,'e'))
    template["sequenceFlows"].append(add_sequence_flow(last,'e'))
    return template
