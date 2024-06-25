import json

def Refresh_ControlPanel_json():
    with open('save/control_panel.json') as f:
        json_control_panel = json.load(f)
    
    return json_control_panel