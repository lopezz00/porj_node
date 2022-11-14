const app = document.getElementById('typewriter')
;

const typewriter = new Typewriter(app,{
    loop:true,
    delay:70
});

typewriter
    .typeString('Escola Politècnica Superior de Enginyeria de Manresa')
    .pauseFor(100)
    .start();