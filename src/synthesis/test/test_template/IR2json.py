import sys
import re
import json
import yaml

# Convert SmartIR to json for ease of synthesis

with open(sys.argv[1], "r", encoding="utf-8") as ifile:
    lines = ifile.readlines()
    ir = "".join(lines)
    ir = re.sub(r'([A-Za-z]+):', r'"\1":', ir)
    ir = re.sub(r'"Price":.+?"Amount":.+?(".+?").+?\};', r'"Price": \1;', ir, flags=re.DOTALL)
    ir = re.sub(r'\(.+?\).+?Payment.*?\{(.+?)\};', r'\1', ir, flags=re.DOTALL)
    ir = re.sub(r'("Termination":.+?)\(.+?\).+?\};', r'\1};', ir, flags=re.DOTALL)
    ir = re.sub(r';', r',', ir, flags=re.DOTALL)
    ir = re.sub(r': ([A-Z][a-zA-Z]+)', r': "\1"', ir, flags=re.DOTALL)
    ir = "{\n" + ir + "\n}"
    ir = re.sub(r'\n', r'', ir, flags=re.DOTALL)
    
    parsed = yaml.load(ir)
    # print(parsed)

    # Key rename
    parsed["CloseTime"] = [parsed["CloseTime"]]
    parsed["OutSideClosingDate"] = [parsed.pop("ExpiryTime")]
    parsed["EffectiveTime"] = [parsed["EffectiveTime"]]
    parsed["BuyerName"] = parsed["Entity"]["BuyerNames"]
    parsed["SellerName"] = parsed["Entity"]["SellerNames"]
    parsed.pop("Entity")
    parsed["Payments"] = []
    for x in parsed["OnlineStateTransfer"]:
        x["Transfer"] = x.pop("DeliveryConstraint")
        x["PurchasePrice"] = x.pop("Price")
        x["TimeLimit"] = x.pop("TimeConstraint")
        parsed["Payments"].append(x)
    parsed.pop("OnlineStateTransfer")
    if parsed["OfflineDelivery"]["DeliveryConstraint"] == "hash":
        parsed["OfflineDelivery"]["DeliveryConstraint"] = True
    else:
        parsed["OfflineDelivery"]["DeliveryConstraint"] = False
    parsed["Transfers"] = parsed.pop("OfflineDelivery")["DeliveryConstraint"]

    parsed["Terminations"] = {}
    if parsed["Termination"]["DeliveryConstraint"]:
        parsed["Terminations"]["TransferTermination"] = True
    else:
        parsed["Terminations"]["TransferTermination"] = False
    if parsed["Termination"]["TimeConstraint"]:
        parsed["Terminations"]["OutOfDateTermination"] = True
    else:
        parsed["Terminations"]["OutOfDateTermination"] = False
    if parsed["Termination"]["OtherConstraint"]:
        parsed["Terminations"]["OtherTermination"] = True
    else:
        parsed["Terminations"]["OtherTermination"] = False    
    parsed.pop("Termination")

    # Output SmartIR json
    formatted_ir = json.dumps(parsed, indent=4, sort_keys=True)
    # print(formatted_ir)
    with open(sys.argv[1] + ".json", "w", encoding='utf-8') as ofile:
        ofile.write(formatted_ir)