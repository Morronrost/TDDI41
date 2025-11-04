;
; BIND data file for local loopback interface
;
$TTL	604800
@	IN	SOA	server.zorbak.com. root.zorbak.com. (
			2025072803	; Serial
			 604800		; Refresh
			  86400		; Retry
			2419200		; Expire
			 604800 )	; Negative Cache TTL
;
@	 IN	NS	server.zorbak.com.
@	 IN	A	10.0.0.4

zorbak.com.		IN	A	10.0.0.4
server			IN	A	10.0.0.4
gw			IN	A	10.0.0.1
client-1		IN	A	10.0.0.2
client-2		IN	A	10.0.0.3
