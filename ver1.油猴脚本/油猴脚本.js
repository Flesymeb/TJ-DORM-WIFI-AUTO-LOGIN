// ==UserScript==
// @name         同济大学校园网自动登录
// @namespace    http://tampermonkey.net/
// @version      1.1
// @description  启动浏览器时自动检查网络状态并登录校园网
// @author       Hyoung Yan
// @license      https://github.com/yzlevol
// @match        *://*/*
// @run-at       document-start
// @grant        GM_xmlhttpRequest
// ==/UserScript==

(function () {
    'use strict';

    // 登录参数 (替换成你的学号和密码)
    const USERNAME = "你 的 学 号";
    const PASSWORD = "你 的 密 码";

    // 构造登录URL
    const loginUrl = `http://172.21.0.54/drcom/login?callback=dr1003&DDDDD=${USERNAME}&upass=${PASSWORD}&0MKKey=123456&R1=0&R2=&R3=0&R6=0&para=00&v6ip=&terminal_type=1&lang=zh-cn&jsVersion=4.1&v=2952&lang=zh`;

    // 检查网络连接
    function checkNetwork() {
        GM_xmlhttpRequest({
            method: "GET",
            url: "https://www.baidu.com/",
            onload: function (response) {
                if (response.status === 200 && response.responseText.includes("百度一下")) {
                    console.log("网络正常，无需登录。");
                    return; // 网络正常，无需登录
                } else {
                    console.log("网络连接异常，尝试登录...");
                    loginCampusNetwork();
                }
            },
            onerror: function (response) {
                console.log("无法访问网络，尝试登录...");
                loginCampusNetwork();
            }
        });
    }

    // 使用GET请求登录校园网
    function loginCampusNetwork() {
        GM_xmlhttpRequest({
            method: 'GET',
            url: loginUrl,
            onload: function (response) {
                console.log("校园网自动登录请求已发送");

                // 检查返回的内容，确定是否登录成功
                if (response.status === 200) {
                    console.log("登录请求成功");

                    // 从当前页面的 URL 中提取重定向 URL
                    const currentUrl = window.location.href;
                    const redirectUrlMatch = currentUrl.match(/url=([^&]+)/);
                    if (redirectUrlMatch && redirectUrlMatch[1]) {
                        const redirectUrl = decodeURIComponent(redirectUrlMatch[1]);
                        console.log("登录成功，重定向到:", redirectUrl);

                        // 跳转到重定向 URL
                        location.href = `http://${redirectUrl}`; // 确保是完整的URL
                    } else {
                        console.log("未找到重定向 URL，尝试刷新页面...");
                        setTimeout(() => {
                            location.reload(); // 刷新页面
                        }, 1000); // 等待1秒后刷新
                    }
                } else {
                    console.log("登录失败，状态码:", response.status);
                }
            },
            onerror: function (error) {
                console.error("校园网自动登录请求失败: ", error);
            }
        });
    }

    // 在浏览器启动时检查网络
    checkNetwork();
})();
