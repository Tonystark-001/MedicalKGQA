function get_answer(){
        var start_time = get_time();
        var question = $("#question").get(0).value;

        if (question == ''){
            return false;
        }

       $.ajax({
            type:'post',
            data:{"question":question},
            url:'http://127.0.0.1:5000/',
            async:true,
            dataType:"json",
            // xhrFields: {withCredentials: true}, //加这个报错，暂时不知道为啥？？？
            success:function (data,status) {
                console.log("status : " + status);
                console.log("answer : " + data['answer']);
                console.log("valid answer : " + data['valid_answer'])

                $("#answer").text(data['answer']);
                var time_consume = get_time() - start_time;
                var valid_answer = data['valid_answer'];

                if (valid_answer == "true"){
                    console.log("valid answer true comes")
                    $("#card-header").text("查询成功").css("cssText","background-color:#28a745 !important;color:#fff;");
                }
                else {
                    console.log("valid answer false comes");
                    $("#card-header").text("查询失败").css("cssText","background-color:#dc3545 !important;color:#fff;");
                }

                $("#time_consume").text("用时: " + time_format(time_consume) + "s");


                console.log("花费时间 : " + time_consume.toString());
            },
           error:function(){
                console.log("Request error.")
                var err_msg = "请求服务器出错，请稍后尝试。"
                $("#answer").text(err_msg);
            }
        })
    }

function get_time() {
     return new Date().getTime();
}

function time_format(time) {
    var seconds = time / 1000;
    return seconds.toFixed(2); // 保留2位小数
}