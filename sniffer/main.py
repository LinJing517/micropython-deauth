
import wireless
import time

#可以指定信道1~13
sniffer=wireless.sniffer(6)
#0：表示从信道1开始 定时切换信道
#sniffer=wireless.sniffer(0)