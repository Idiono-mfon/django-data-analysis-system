const navList = document.querySelector(".nav-list")
const navActivator = document.querySelector(".nav-icon")

const realFileBtn = document.querySelector(".custom-upload");
const customBtn = document.querySelector("#custom-button");
const customTxt = document.querySelector("#custom-text");
const slides = document.querySelectorAll('.slide');
const auto = true;
const intervalTime = 5000;
let slideInterval;

window.addEventListener('load', () => {
    navActivator.addEventListener('click', ()=>{
        navList.classList.toggle("show");
    })
    const slideShow = function(){
        const current = document.querySelector('.current');
        current.classList.remove('current');
        if (current.nextElementSibling) {
            current.nextElementSibling.classList.add('current');
        }else{
            slides[0].classList.add('current');
        }
        setTimeout( ()=>current.classList.remove('current') );
    }
    slideShow();
    if (auto) {
        clearInterval(slideInterval)
        slideInterval = setInterval(slideShow, intervalTime)
    }

    customBtn.addEventListener("click", function() {
    realFileBtn.click();
    });

    realFileBtn.addEventListener("change", function() {
    if (realFileBtn.value) {
        customTxt.innerHTML = realFileBtn.value.match(
        /[\/\\]([\w\d\s\.\-\(\)]+)$/
        )[1];
    } else {
        customTxt.innerHTML = "No file chosen, yet.";
    }
    });

})    
