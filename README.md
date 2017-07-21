# micropython-deauth
通过修改micropython中esp8266的固件源码，调用ESP8266-SDK中wifi_send_pkt_freedom函数，
实现Deauth解除认证包的发送，从而达到WIFI干扰的效果。

ESP8266-SDK编译：
https://github.com/pfalcon/esp-open-sdk

micropython-esp8266编译：
https://github.com/micropython/micropython/tree/master/esp8266
