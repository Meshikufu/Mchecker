import json

def Refresh_ControlPanel_json():
    with open('save/control_panel.json') as f:
        json_control_panel = json.load(f)
        
    return {
        'testingPhase': json_control_panel['testingPhase'],
        'tts_ON': json_control_panel.get('tts_ON', False),
        'tts_NewSeller': json_control_panel['tts_NewSeller'],
        'tts_ChangeManually': json_control_panel['tts_ChangeManually'],
        'tts_Matched': json_control_panel['tts_Matched'],
        'tts_SlightyHigher': json_control_panel['tts_SlightyHigher'],
        'tts_SoldStock': json_control_panel['tts_SoldStock'],
        'tts_Pos2GotHigher': json_control_panel['tts_Pos2GotHigher'],
        'tts_Pos2LoweredPrice': json_control_panel['tts_Pos2LoweredPrice'],
        'tts_RaisedPrice': json_control_panel['tts_RaisedPrice'],
        'tts_LoweredPrice': json_control_panel['tts_LoweredPrice'],
        'tts_ChangingPrice': json_control_panel['tts_ChangingPrice'],
        'tts_ChangingPriceIN': json_control_panel['tts_ChangingPriceIN'],
        'tts_Done': json_control_panel['tts_Done'],
        'tts_RetringIn60': json_control_panel['tts_RetringIn60'],
        'autoChangePrice': json_control_panel['autoChangePrice'],
        'desktop_swap_wait_timer': json_control_panel['desktop_swap_wait_timer'],
        'IterationSleepTime': json_control_panel['IterationSleepTime'],
        'PriceChecker_loop_start_time': json_control_panel['PriceChecker_loop_start_time'],
        'msgClientWebpage': json_control_panel['msgClientWebpage']
    }