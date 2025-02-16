import json

with open('sample.json') as file:
    json_data = json.load(file)
    print('''Interface Status
    ================================================================================
    DN                                                 Description       Speed   MTU  
    -------------------------------------------------- ---------------  ------  -----''')

    imdata = json_data['imdata']
    for item in imdata:
        o_item = item['l1PhysIf']
        attr = o_item['attributes']
        dn = attr['dn']
        speed = attr['speed']
        mtu = attr['mtu']

        print(f"{dn:<50} {'':<20} {speed:<7} {mtu:<6}")
