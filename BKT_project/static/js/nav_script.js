

const red = '#ff3b00';
const green = '#17ff40';
const ok_yellow = '#ffa500';
const status = document.querySelector("#status");
const logs = document.querySelector('#logs');
function delay(ms = 3000) {
    return new Promise(resolve => setTimeout(resolve, ms),
        reject => setTimeout(resolve, ms));
}

