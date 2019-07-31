var default_content = [['这是', 0, 2], ['一段', 2, 4], ['默认', 4, 6], ['的', 6, 7], ['内容', 7, 9]];
var texts = null;
var textLabels = $('.display-text');

var speed = 400; // 单位: 词/分钟

function init(cut_arr) {
    texts = cut_arr;
    texts.unshift(["", -1, -1], ["", -1, -1]);
    texts.push(["over", -1, -1], ["...", -1, -1]);

    // 初始化显示内容
    for (i = 0; i < textLabels.length; i++) {
        textLabels[i].textContent = texts[i][0];
    }
}

init(default_content);

var runningInterval = null;
var paused = false;
var cnt = 0;

function start() {
    if (runningInterval != null) {
        // console.log('restart');
        clearInterval(runningInterval)
    }
    cnt = 0;
    // console.log('texts.length:', texts.length);
    run();
}

function run() {
    var interval = setInterval(function () {
        runningInterval = interval;
        for (i = 0; i < textLabels.length; i++) {
            textLabels[i].textContent = texts[cnt + i][0];
        }
        cnt += 1;
        // console.log(cnt);
        if (cnt >= texts.length - textLabels.length + 1) {
            // console.log('clear: ', cnt);
            clearInterval(interval)
        }
    }, 60 * 1000 / speed);
}

function pause() {
    if (paused) {
        run();
        paused = false;
        return
    }
    if (runningInterval) {
        paused = true;
        clearInterval(runningInterval)
    }
}

function get_cut_text() {
    var comment = $('#comment').val();
    $.ajax({
        url: '/cut',
        dataType: 'json',
        contentType: 'application/json; charset=UTF-8', // This is the money shot
        data: JSON.stringify({data: comment}),
        type: 'POST',
        success: function (data, state) {
            // console.log(data);
            init(data);
        }
    });
}


var bt_restart = $('#bt-restart');
var can_click = true;
bt_restart.on('click', function () {
    if (can_click) {
        can_click = false;
        setTimeout(function () {
            can_click = true;
        }, 500)
    } else {
        return
    }
    var bt = $('#bt-pause').children();
    if (paused) {
        paused = false
        bt.text('暂停');
    }
    start();
});

var bt_pause = $('#bt-pause');
bt_pause.on('click', function () {
    pause();
    var bt = bt_pause.children();
    if (paused) {
        bt.text('继续');
    } else {
        bt.text('暂停');
    }
});

var bt_submit = $('#submit');
bt_submit.on('click', function () {
    if ($('#comment').val() === '') {
        alert('请输入内容');
        return
    }
    get_cut_text();
});

var input_speed = $('#speed');
// input_speed.on('input', function () {
//
// });
input_speed.bind('input propertychange', function () {
    speed = input_speed.val();
    $('#test').text(speed)
});