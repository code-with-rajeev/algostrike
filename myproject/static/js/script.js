console.log("AlgoTrading Platform")

let verified_users = 4000;
let premium_features = 27;
let duration = 3000; //3000ms

let steps = Math.floor(verified_users/premium_features);
let intervalTime = Math.floor(duration/premium_features);

let counter1 = 0;
let counter2 = 0;

let count1 = document.querySelector('#verified-users');
let count2 = document.querySelector('#premium-features');
const interval = setInterval(() =>{
    
    counter1 += steps;
    counter2 += 1;
    count1.textContent = `${counter1}+`;
    count2.textContent = `${counter2}+`;
    console.log(counter1,counter2);
    if(counter1>=verified_users || counter2>=premium_features){
        clearInterval(interval);
        count1.textContent = `${verified_users}+`;
        count2.textContent = `${premium_features}+`;
    }
}, intervalTime);


