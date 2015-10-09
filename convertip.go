package main

import (
	"fmt"
	"os"
	"strings"
)

// 粘贴GoAgent的ip到下面
var ip_goagent = `

|1.1.1.85|1.1.1.115|
1.1.1.112|

1.1.1.152|
1.1.1.92|1.1.1.68|1.1.1.197|1.1.1.203|
`

// 粘贴GoProxy的ip到下面
var ip_goproxy = `

 ,,"1.1.1.85","1.1.1.115","1.1.1.112","1.1.1.152",


"1.1.1.92","1.1.1.68","1.1.1.197",
"1.1.1.203"
`

var GOAGENT_TO_GOPROXY = 1
var GOPROXY_TO_GOAGENT = 2

func covert_ip(ip_goagent string, ip_goproxy string, action int) string {
	var temp []string
	var ip_list []string
	var ip_result string
	ip_goagent = strings.Replace(ip_goagent, "\n", "", -1)
	ip_goproxy = strings.Replace(ip_goproxy, "\n", "", -1)
	switch action {
	case GOAGENT_TO_GOPROXY:

		ip_list = strings.Split(ip_goagent, "|")

		for _, ip := range ip_list {
			if strings.Trim(ip, " ") != "" {
				temp = append(temp, "\""+ip+"\"")
			}
		}
		ip_result = strings.Join(temp, ",")

	case GOPROXY_TO_GOAGENT:
		ip_list = strings.Split(ip_goproxy, ",")
		for _, ip := range ip_list {
			if strings.Trim(ip, " ") != "" {
				temp = append(temp, strings.Replace(ip, "\"", "", -1))
			}
		}
		ip_result = strings.Join(temp, "|")
	}
	fmt.Println("转换完成")
	return ip_result
}

func main() {
	var prompt = `
    请指定转换方式:
    1. GoAgent --> GoProxy
    2. GoProxy --> GoAgent	
	`
	fmt.Println(prompt)
	var flag int
	var result string
	fmt.Scanf("%d", &flag)

	switch flag {
	case GOAGENT_TO_GOPROXY:
		result = covert_ip(ip_goagent, ip_goproxy, GOAGENT_TO_GOPROXY)
	case GOPROXY_TO_GOAGENT:
		result = covert_ip(ip_goagent, ip_goproxy, GOPROXY_TO_GOAGENT)
	default:
		fmt.Println("无效的方式, exit!")
		os.Exit(1)
	}

	fmt.Println("ip: ", result)
}
