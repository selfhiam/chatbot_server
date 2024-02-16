const popup = document.querySelector(".layer");
const randomNum = Math.floor(Math.random() * 3 + 1);
const char = document.querySelector(".char");
char.innerHTML = `<img src="./logo/${randomNum}.png" alt="character">`
localStorage.setItem('char', randomNum);
const cname = localStorage.getItem('name');
let subment = document.querySelector(".subment");

fetch('http://127.0.0.1/naming.html', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    }
})
.then((res) => res.json())
.then((data) => {
    // 이미 JavaScript 객체이므로 추가적인 JSON 파싱은 필요하지 않음
    let parsed = data[0];
    console.log(parsed)
    parsed = JSON.parse(parsed);
    parsed = parsed["C1"]
    parsed = parsed.replace("챗쪽", "<span class='cname'></span>")
    subment.innerHTML = parsed
    let changes = document.querySelector('.cname');
    changes.innerText = cname
})


let changes = document.querySelector('.name');
console.log(changes)
changes.innerText = cname


function select() {
    popup.style.display = 'block';
}

const x = document.querySelector(".xi-close-min");

x.addEventListener("click", () => {
    console.log('tkrwp!')
    popup.style.display = 'none';
})


function enter() {
    const parents = document.getElementsByName('parents')
    const selected = Array.from(parents).find(radio => radio.checked);
    console.log(selected.value)
    fetch('http://127.0.0.1/birth.html', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'parents': selected.value
        })
    })
        .then(() => {
            window.location.href = "./chatting.html";
        })
}
