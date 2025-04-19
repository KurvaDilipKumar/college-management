



const cards = document.querySelectorAll(".flexgrow-card");
let flexgrowCard = document.querySelector(".flexgrow-card.active");

cards.forEach((card) => {
  card.addEventListener("mouseenter", () => {
    if (card === flexgrowCard) return;

    if (flexgrowCard) {
      flexgrowCard.classList.remove("active");
    }

    card.classList.add("active");
    flexgrowCard = card;
  });
});
