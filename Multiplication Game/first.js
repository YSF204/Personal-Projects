let timeRemaining = 60;
let play = false;
let score = 0;
let correctAnswer;

document.getElementById("startGameBtn").onclick = function() {
if (play == true ){
    location.reload();

}
else { 
    play = true;
    document.getElementById("ScoreValue").innerHTML=score;
    Show("time")
    StartCounter();
    generateQ();
    for ( let  i = 1 ; i <=4 ; i++){

        document.getElementById("box"+i).onclick=function() {
            if(parseInt(this.innerHTML)==correctAnswer){
                score++;
                generateQ();
                document.getElementById("ScoreValue").innerHTML=score;
                Show("Correct");
                Hide("Wrong");
                setTimeout(() => {
                    Hide("Correct");
                    

                },1000);
                
            }
            else {
                Show("Wrong");
                Hide("Correct");
                setTimeout (()=>{
                    Hide("Wrong");
                }, 1000);
            }
        }
    }
     }
}
 
function Show(id){
    document.getElementById(id).style.display="block";
}

function Hide(id){
    document.getElementById(id).style.display="none";
}

function StartCounter(){
    Time = setInterval(()=>{
        timeRemaining--;
        document.getElementById("timeRemainingValue").innerHTML=timeRemaining;
        if(timeRemaining==0){
            StopCounter();
            play=false;
            timeRemaining=60;
            location.reload();
        }
        
    } , 1000)

}

function StopCounter(){
    clearInterval(Time);
    Hide("time");
}

function generateQ(){
    let x;
    let y;
    x = 1+ Math.round(Math.random()*9);
    y = 1+ Math.round(Math.random()*9);
     correctAnswer = x * y;
    document.getElementById("question").innerHTML=x+"   X   "+y;
    let correctPos = Math.floor(Math.random() * 4) + 1;
    document.getElementById("box"+correctPos).innerHTML=correctAnswer;
    for (let i = 1; i <= 4; i++) {
        if (i !== correctPos) {
            let wrongAnswer;
            do {
                let xw = 1 + Math.round(Math.random() * 9);
                let yw = 1 + Math.round(Math.random() * 9);
                wrongAnswer = xw * yw;
            } while (wrongAnswer === correctAnswer);
            
            document.getElementById("box" + i).innerHTML = wrongAnswer;
        }
    }
}