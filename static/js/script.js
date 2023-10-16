const expandBouquet = document.querySelector(".expand-bouquet");
const selectBouquet = document.querySelector(".shape-value-wrapper-three");
expandBouquet.addEventListener('click', () => {
    selectBouquet.classList.toggle("open");
    if (expandBouquet.classList.contains("open")) {
        expandBouquet.innerHTML = " ∨";
    } else {
        expandBouquet.innerHTML = " ∧";
    }
    expandBouquet.classList.toggle("open");
});

const expandWine = document.querySelector(".expand-wine");
const selectWine = document.querySelector(".shape-value-wrapper-four");
expandWine.addEventListener('click', () => {
    selectWine.classList.toggle("open");
    if (expandWine.classList.contains("open")) {
        expandWine.innerHTML = " ∨";
    } else {
        expandWine.innerHTML = " ∧";
    }
    expandWine.classList.toggle("open");
});