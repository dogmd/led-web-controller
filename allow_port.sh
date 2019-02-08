iptables -A INPUT -i wlp2s0 -p tcp --dport 8765 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o wlp2s0 -p tcp --sport 8765 -m state --state ESTABLISHED -j ACCEPT
