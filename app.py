# -*- coding: utf-8 -*-
from flask import Flask, render_template, request,jsonify
from PortScanner import *
import os
app=Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=["get"])
def scan():
    # global Timeout
    # Timeout=request.args.get('timeout')
    nThread=request.args.get('thread')
    PortList = []

    ListTmp = request.args.get('port').split(',')
    for port in ListTmp:
        if port.find("-") < 0:
            if not port.isdigit():
                # print "输入错误"
                return False
            PortList.append(int(port))
        else:
            RangeLst = port.split("-")
            if not (RangeLst[0].isdigit() and RangeLst[1].isdigit()):
                raise ValueError
                exit()
            for i in range(int(RangeLst[0]), int(RangeLst[1])):
                PortList.append(i)
    if(request.args.get('scan')):
        ThreadList = []
        strIP = request.args.get('ip')
        SingleQueue = GetQueue(PortList)
        for i in range(0, int(nThread)):
            t = ScanThreadSingle(strIP, SingleQueue)
            ThreadList.append(t)
        for t in ThreadList:
            t.start()
        for t in ThreadList:
            t.join()
        openlist = []
        try:
            with open(strIP, 'r+') as f:
                openlist.append(f.read())
            os.remove(strIP)
        except:
            pass
    elif(request.args.get('search')):
        ThreadList = []
        ip = IPNetwork(request.args.get('ip'))
        ip_list = list(ip)
        for i in ip_list:
            t = ScanThreadMulti(str(i), PortList)
            ThreadList.append(t)
        for t in ThreadList:
            t.start()
        for t in ThreadList:
            t.join()
        openlist=[]
        for i in ip_list:
            try:
                with open(str(i),'r+') as f:
                    openlist.append(f.read())
                os.remove(str(i))
            except:
                pass
    else:
        pass
    if openlist != []:
        return jsonify(openlist[0].split("\n")[:-1])
    else:
        return jsonify(openlist)

if __name__=="__main__":
    app.run(debug=True)
