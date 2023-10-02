from xrpl.models import Transaction
from xrpl.core.keypairs import is_valid_message
from xrpl.core.binarycodec import encode_for_signing
from xrpl.core.binarycodec import decode
from re import sub

def camel_case(s):
  s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
  return ''.join([s[0].upper(), s[1:]])
def create_transaction_fromtx_blob(tx_blob):
    assert type(tx_blob) == str
    return Transaction.from_blob(tx_blob)

def fix_offer_obj_dict_naming(txn_dict):
    new_dict = {}
    for key in list(txn_dict.keys()):
        new_key = camel_case(key)
        new_dict[new_key] = txn_dict[key]
    return new_dict

def is_valid_transaction(tx_blob):
    transaction_dict = decode(tx_blob)
    is_valid = is_valid_message(
        bytes.fromhex(encode_for_signing(transaction_dict)),
        bytes.fromhex(transaction_dict['TxnSignature']),
        transaction_dict['SigningPubKey'],
    )
    return is_valid

tx_blob = "12001B2280000001240249B9F95A00080000B255658FC7DBD73C5A8CBAC930BA72488989E7FE0000099A0000000061400000000000000068400000000000000A7321EDC964C2CF0B0E9F781781566F7AB05042E1EBFD64AB8376DC1CF847FD4379DAE074403B56C35BE29C3B483794D725F548C901B998722F503FFB6D62E97B53025448B2AD1A6EB98766E609E196A08588AA845CAE01A002A2ED38A797B194F88C3477088114232BD6BD52989DFBA2375E7DBD940000E73B68C68314B255658FC7DBD73C5A8CBAC930BA72488989E7FE"
if __name__ == '__main__':
    tzac = create_transaction_fromtx_blob(tx_blob)
    valid = is_valid_transaction(tx_blob)