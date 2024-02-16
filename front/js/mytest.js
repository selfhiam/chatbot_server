/// python에서 뽑은 q, a 받아오기
fetch('http://127.0.0.1/mytest.html', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    }
})
.then(res => res.json())
.then((data) => {
    console.log(data)
    initialization(data)
})

let num = 0;
let alldata;
let score = {};

for(let i = 0; i < 10; i++)
{
    score[i] = 0;
}

console.log(score);

quest = document.querySelector('.question');
ans1 = document.querySelector('#ans1');
ans2 = document.querySelector('#ans2');
numbering = document.querySelector('.change');

/// 받은 값을 전역변수에 저장
function initialization(data) {
    alldata = data
    console.log(alldata);
    firstdata = JSON.parse(alldata[num])

    numbering.innerText = num + 1
    quest.innerText = firstdata['Q']
    ans1.innerText = firstdata['A1']
    ans2.innerText = firstdata['A2']
}

//고집0/우유1/급함2/여유3/불안4/긍정5/이성6/감성7/외향8/내향9
/// 해당 값으로 
function nextQuestion(i, ans) {
    num = num + i;

    if(num < 0){
        window.location.href = './index.html'
    }
    else if(num > 9){
        labeldata = JSON.parse(alldata[num - 1])
        label = labeldata['label']    
        score[label[ans]] += 1;
        localStorage.setItem("score", JSON.stringify(score))
        window.location.href = './middletest.html'
    }
    else {
        getdata = JSON.parse(alldata[num])

        numbering.innerText = num + 1
        quest.innerText = getdata['Q']
        ans1.innerText = getdata['A1']
        ans2.innerText = getdata['A2']

        labeldata = JSON.parse(alldata[num - 1])
        label = labeldata['label']

        score[label[ans]] += 1;
    }
} 
