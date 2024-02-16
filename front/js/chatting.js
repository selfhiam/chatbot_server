let cname = localStorage.getItem('name');
let changes = document.querySelector('.name');
changes.innerText = cname;

const char = localStorage.getItem('char');

const DEFAULT_HEIGHT = 5; // textarea 기본 height
const text = document.getElementById('textarea')
const btn = document.getElementById('btn')
const container = document.querySelector('.container');
let testResult = localStorage.getItem("score");
testResult = JSON.parse(testResult)
console.log(testResult)
//고집0/우유1/급함2/여유3/긍정4/불안5/이성6/감성7/외향8/내향9
emoList = []
for (let i = 0; i < 10; i = i + 2) {
    if (testResult[i] > testResult[i+1]) {
        emoList.push(i);
    }
    else if (testResult[i] < testResult[i+1]){
        emoList.push(i+1);
    }
}
console.log(emoList)

function choosing(emoList) {
    let choose;
    if(emoList.length == 0){
        num = Math.floor((Math.random() * 10));
        choose = num;
    }
    else{
        num = Math.floor((Math.random() * emoList.length));
        choose = emoList[num];
    }
    return choose;
}

let isModelRunning = false;

text.oninput = (event) => {
    const $target = event.target;
    if (text.value.length > 0 && !isModelRunning) {
        btn.classList.add('yellow')
    }
    $target.style.height = 0;
    $target.style.height = DEFAULT_HEIGHT + $target.scrollHeight + 'px';
    if (text.value.length == 0) {
        btn.classList.remove('yellow')
    }
};


async function submit() {
    if (text.value.length > 0 && !isModelRunning) {
        isModelRunning = true;

        let today = new Date();
        let hours = ('0' + today.getHours()).slice(-2);
        let minutes = ('0' + today.getMinutes()).slice(-2);
        let timeString = hours + ':' + minutes;

        // 입력값 화면에 띄우기
        container.innerHTML += `<span class="text">
            <div class="align">
                <span class="time">${timeString}</span>
                <div class="mytext">
                    <div>${text.value}</div>
                </div>
            </div>
        </span>`;

        // input, 버튼 초기화
        let context = text.value;
        text.value = null;
        text.style.height = 0;
        text.style.height = DEFAULT_HEIGHT + text.scrollHeight + 'px';
        btn.classList.remove('yellow');
        window.scrollTo(0, document.body.scrollHeight);

        choose = choosing(emoList);
        if (cname[cname.length - 1] == '이') {
            cname = cname.slice(0, -1);
        }
        const regex = new RegExp(`${cname}`, 'g');
        console.log(regex); // /JS/g
        context = context.replace(regex, "챗쪽")
        // model 함수 호출 (Promise 사용)
        console.log(context);
        await model(choose + context);

        // model 함수가 완료된 후에 실행될 코드
        console.log("model 함수 호출 완료");

        isModelRunning = false;
    }
}

function model(value) {
    return new Promise(resolve => {
        fetch('http://127.0.0.1/chatting.html', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'question': value
            })
        })
            .then((res) => res.json())
            .then((jsondata) => {
                console.log(jsondata)

                let today = new Date();
                let hours = ('0' + today.getHours()).slice(-2);
                let minutes = ('0' + today.getMinutes()).slice(-2);
                let timeString = hours + ':' + minutes;

                container.innerHTML += `<span class="text">
                            <div class="character">
                                <img src="../logo/${char}.png" alt="">
                            </div>
                            <div class="yourtext">
                                <div>${jsondata['message']}</div>
                                <span class="time">${timeString}</span>
                            </div>
                        </span>`;
                window.scrollTo(0, document.body.scrollHeight);

                // Promise를 통해 완료를 알림
                resolve();
            });
    })
}

$('textarea').on('keydown', function (event) {
    if (event.key == 'Enter')
        if (!event.shiftKey) {
            event.preventDefault();
            submit();
        }
});
