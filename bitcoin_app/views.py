import json

import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from bitcoin_app.forms import GenerateAddressForm, TransferAmount, TransferAmountForm
from bitcoin_app.models import GenerateAddress


rpcUser = "user"
rpcPassword = "pass"
rpcPort = 18443
url = 'http://' + rpcUser + ':' + rpcPassword + '@localhost:' + str(rpcPort)
payload = {"jsonrpc": 1, "id":"curltext"}


def hello(request):
    return HttpResponse("Hello Bitcoin App")


def generate_address(request, template_name="generate_address.html"):
    print(request.body)
    payload['method'] = "getnewaddress"
    payload['params'] = []

    if request.method == "GET":
        response = requests.post(url, data=json.dumps(payload))
        json_data = json.loads(response.text)
        generated_address = GenerateAddress.objects.create(bitcoin_address=json_data['result'])
        generated_address.save()
        return render(request, template_name, {'bitcoin_address': json_data['result']})
    else:
        return render(request, template_name)


def private_key_address(request, bitcoin_address, template_name="private_key_address.html"):
    payload['method'] = "dumpprivkey"
    payload['params'] = [bitcoin_address]

    if request.method == "GET":
        response = requests.post(url, data=json.dumps(payload))
        json_data = json.loads(response.text)
        GenerateAddress.objects.update(bitcoin_address=bitcoin_address, private_key_address=json_data['result'])
        return render(request, template_name, {"private_key_address": json_data['result']})


def public_key_address(request, bitcoin_address, template_name="public_key_address.html"):
    payload['method'] = "validateaddress"
    payload['params'] = [bitcoin_address]

    if request.method == "GET":
        response = requests.post(url, data=json.dumps(payload))
        json_data = json.loads(response.text)
        GenerateAddress.objects.update(bitcoin_address=bitcoin_address, public_key_address=json_data['result']['pubkey'])
        return render(request, template_name, {"public_key_address": json_data['result']['pubkey']})


def list_transactions(request , template_name= "list_transactions.html"):
    payload['method'] = "listtransactions"
    payload['params'] = []
    if request.method == "GET":

        response = requests.post(url, data=json.dumps(payload))
        json_data = json.loads(response.text)

        return render(request, template_name, {"list_transactions": json_data['result']})

def list_unspent():
    payload['method'] = "listunspent"
    payload['params'] = []

    response = requests.post(url, data=json.dumps(payload))
    json_data = json.loads(response.text)

    return json_data['result']


def transfer_amount(request, template_name = "transfer_amount.html"):

    if request.method == "POST":
        form = TransferAmountForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            to_address = cleaned_data['send_to_address']
            from_address = cleaned_data['from_address']
            amount_field = cleaned_data['amount_field']

            payload['method'] = "sendtoaddress"
            payload['params'] = [to_address, amount_field]
            response = requests.post(url, data=json.dumps(payload))
            json_data = json.loads(response.text)
            generate_block_txid = generate_block()
            unspent = list_unspent()
            raw_transaction = get_raw_transaction(json_data['result'])
            for tx in raw_transaction['vout'] :

                if not (tx['scriptPubKey']['addresses'] == to_address):
                    transferred_data_remaining = TransferAmount.objects.create(from_address=from_address,to_address=tx['scriptPubKey']['addresses'],
                                                                           amount_field=tx['value'])
                    transferred_data_remaining.save()

                else :
                    transferred_data_send = TransferAmount.objects.create(from_address=from_address, to_address=to_address,
                                                                     amount_field=amount_field)

                    transferred_data_send.save()

            return render(request, template_name, {"form": form,'list_unspent':unspent, 'generate_block_txid':generate_block_txid, "transaction": json_data['result']})

    else:
        form = TransferAmountForm()
        unspent = list_unspent()

        return render(request, template_name, {'form': form, 'list_unspent':unspent})


def get_raw_transaction(txid):
    payload['method']= "getrawtransaction"
    payload['params'] = [txid, 1]

    response = requests.post(url, data=json.dumps(payload))
    json_data = json.loads(response.text)
    return json_data['result']

def generate_block():
    payload["method"] = "generate"
    payload["params"] = [1]

    response = requests.post(url, data=json.dumps(payload))
    json_data = json.loads(response.text)

    return json_data['result']

def list_received_by_address():
    payload['method'] = "listreceivedbyaddress"
    payload["params"] = [1]

    response = requests.post(url, data=json.dumps(payload))
    json_data = json.loads(response.text)
    return json_data['result']